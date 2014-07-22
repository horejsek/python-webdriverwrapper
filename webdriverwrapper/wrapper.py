# -*- coding: utf-8 -*-

from __future__ import absolute_import

import functools

import selenium.common.exceptions as selenium_exc
from selenium.webdriver import *
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select, WebDriverWait

from webdriverwrapper.utils import force_text
from webdriverwrapper.exceptions import NoSuchWindowException, _create_exception_msg
import webdriverwrapper.gotopage as gotopage
from webdriverwrapper.download import DownloadUrl, DownloadFile

__all__ = (
    'Firefox',
    'FirefoxProfile',
    'Chrome',
    'ChromeOptions',
    'Ie',
    'Opera',
    'PhantomJS',
    'Remote',
    'DesiredCapabilities',
    'ActionChains',
    'TouchActions',
    'Proxy',
)


class _ConvertToWebelementWrapper(object):
    def __call__(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwds):
            res = f(*args, **kwds)
            res = self._convert_result(res)
            return res
        return wrapper

    @classmethod
    def _convert_result(cls, res):
        if type(res) is WebElement:
            res = cls._convert_into_webelementwrapper(res)
        elif isinstance(res, (list, tuple)):
            for index, item in enumerate(res):
                res[index] = cls._convert_result(item)
        return res

    @classmethod
    def _convert_into_webelementwrapper(cls, webelement):
        try:
            if webelement.tag_name == 'form':
                from webdriverwrapper.forms import Form
                wrapped = Form(webelement)
            elif webelement.tag_name == 'select':
                wrapped = _SelectWrapper(webelement)
            else:
                wrapped = _WebElementWrapper(webelement)
        except selenium_exc.StaleElementReferenceException:
            return webelement
        else:
            return wrapped


class _WebdriverBaseWrapper(object):
    def contains_text(self, text):
        """Does page contains `text`?"""
        return bool(self.find_elements_by_text(text))

    def find_elements_by_text(self, text):
        """Find every element in page which contain `text`."""
        text = force_text(text)
        elms = self.find_elements_by_xpath(
            './/*[contains(text(), "%s") and not(ancestor-or-self::*[@data-selenium-not-search])]' % text
        )
        return elms

    def click(self, *args, **kwds):
        if args or kwds:
            elm = self.get_elm(*args, **kwds)
            elm.click()
        else:
            super(_WebdriverBaseWrapper, self).click()

    def get_elm(
        self,
        id_=None, class_name=None, name=None, tag_name=None, xpath=None,
        parent_id=None, parent_class_name=None, parent_name=None, parent_tag_name=None,
        css_selector=None
    ):
        elms = self.get_elms(
            id_, class_name, name, tag_name, xpath,
            parent_id, parent_class_name, parent_name, parent_tag_name,
            css_selector
        )
        if not elms:
            raise selenium_exc.NoSuchElementException(_create_exception_msg(
                id_, class_name, name, tag_name, xpath,
                parent_id, parent_class_name, parent_name, parent_tag_name,
                self.current_url,
            ))
        return elms[0]

    def get_elms(
        self,
        id_=None, class_name=None, name=None, tag_name=None, xpath=None,
        parent_id=None, parent_class_name=None, parent_name=None, parent_tag_name=None,
        css_selector=None
    ):
        if parent_id or parent_class_name or parent_name or parent_tag_name:
            parent = self.get_elm(parent_id, parent_class_name, parent_name, parent_tag_name)
        else:
            parent = self

        if len([x for x in (id_, class_name, tag_name, xpath) if x is not None]) > 1:
            raise Exception('You can find element only by one param.')

        if id_ is not None:
            return parent.find_elements_by_id(id_)
        elif class_name is not None:
            return parent.find_elements_by_class_name(class_name)
        elif name is not None:
            return parent.find_elements_by_name(name)
        elif tag_name is not None:
            return parent.find_elements_by_tag_name(tag_name)
        elif xpath is not None:
            return parent.find_elements_by_xpath(xpath)
        elif css_selector is not None:
            return parent.find_elements_by_css_selector(css_selector)
        else:
            raise Exception('You must specify id or name of element on which you want to click.')

    def find_element(self, by=By.ID, value=None):
        callback = self._get_seleniums_driver_class().find_element
        return self._find_element_or_elements(callback, by, value)

    def find_elements(self, by=By.ID, value=None):
        callback = self._get_seleniums_driver_class().find_elements
        return self._find_element_or_elements(callback, by, value)

    def _get_seleniums_driver_class(self):
        next_is_selenium_driver_class = False
        driver_class = None
        for cls in self.__class__.mro():
            if next_is_selenium_driver_class:
                driver_class = cls
                break
            if cls is _WebdriverBaseWrapper:
                next_is_selenium_driver_class = True
        if not driver_class:
            raise Exception('WebDriver class not found')
        return driver_class

    #  Map from selenium's By class to name of params used in this wrapper. It's
    #+ used for making helpful messages.
    #  Commented lines are not supported.
    _by_to_string_param_map = {
        By.ID: 'id_',
        By.XPATH: 'xpath',
        #By.LINK_TEXT: 'link_text',
        #By.PARTIAL_LINK_TEXT: 'partial_link_text',
        By.NAME: 'name',
        By.TAG_NAME: 'tag_name',
        By.CLASS_NAME: 'class_name',
        #By.CSS_SELECTOR: 'css_selector',
    }

    @_ConvertToWebelementWrapper()
    def _find_element_or_elements(self, callback, by, value):
        if by in self._by_to_string_param_map:
            msg = _create_exception_msg(**{
                self._by_to_string_param_map[by]: value,
                'url': self.current_url,
            })
        else:
            msg = ''
        try:
            return callback(self, by, value)
        except (
            selenium_exc.NoSuchElementException,
            selenium_exc.StaleElementReferenceException,
            selenium_exc.InvalidElementStateException,
            selenium_exc.ElementNotVisibleException,
            selenium_exc.ElementNotSelectableException,
        ) as exc:
            raise exc.__class__(msg)


class _WebdriverWrapper(_WebdriverBaseWrapper):
    def wait_for_element(self, timeout=10, message='', *args, **kwds):
        """
        Same as WebDriverWait(driver, timeout).until(lambda driver: driver.get_elm(...)),
        but appends useful message if it's not provided.
        """
        if not message:
            message = _create_exception_msg(*args, **kwds)
        self.wait(timeout).until(lambda driver: driver.get_elm(*args, **kwds), message=message)

        # Also return that element for which is waiting.
        elm = self.get_elm(*args, **kwds)
        return elm

    def wait(self, timeout=10):
        """Alias for WebDriverWait(driver, timeout).
        Returns instance which has method until which takes function.

        Example:
        self.wait().until(lambda driver: len(driver.find_element_by_id('elm')) > 10)
        """
        return WebDriverWait(self, timeout)

    def go_to(self, path=None, query=None, domain=None):
        """
        Go to page. You can pass only `path`, because this
        method can get domain from current_url from driver
        instance. But you can force your own domain by `domain`.
        `query` can be dictionary.
        """
        if not domain:
            domain = gotopage._get_domain_from_driver(self)
        gotopage.go_to_page(self, path, query, domain)

    def switch_to_window(self, window_name=None, title=None, url=None):
        if window_name:
            self._get_seleniums_driver_class().switch_to_window(self, window_name)
            return

        if url:
            if not isinstance(url, dict):
                url = {'path': url}
            url.setdefault('domain', gotopage._get_domain_from_driver(self))
            url = gotopage._make_url(**url)

        for window_handle in self.window_handles:
            self._get_seleniums_driver_class().switch_to_window(self, window_handle)
            if title and self.title == title:
                return
            if url and self.current_url == url:
                return
        raise NoSuchWindowException('Window (title=%s, url=%s) not found.' % (title, url))

    def close_window(self, window_name=None, title=None, url=None):
        main_window_handle = self.current_window_handle
        self.switch_to_window(window_name, title, url)
        self.close()
        self.switch_to_window(main_window_handle)

    def close_other_windows(self):
        main_window_handle = self.current_window_handle
        for window_handle in self.window_handles:
            if window_handle == main_window_handle:
                continue
            self.switch_to_window(window_handle)
            self.close()
        self.switch_to_window(main_window_handle)

    def close_alert(self, ignore_exception=False):
        try:
            alert = self.get_alert()
            alert.accept()
        except:
            if not ignore_exception:
                raise

    def get_alert(self):
        """Returns instance of selenium.webdriver.common.alert.Alert"""
        return Alert(self)

    def download_url(self, url=None):
        """
        With Selenium you can't check staus code or headers. So this method will
        download `url` or `self.current_url` by urllib and you can check status
        code, headers and data as with `download_file`.
        You could download it by yourself, but this handle also cookies.
        """
        return DownloadUrl(self, url)


class _WebElementWrapper(_WebdriverBaseWrapper, WebElement):
    def __new__(cls, webelement):
        instance = super(_WebElementWrapper, cls).__new__(cls)
        instance.__dict__.update(webelement.__dict__)
        return instance

    def __init__(self, webelement):
        #  Nothing to do because whole __dict__ of original WebElement was
        #+ copied during creation of instance.
        pass

    @property
    def current_url(self):
        try:
            current_url = self._parent.current_url
        except Exception:
            current_url = 'unknown'
        finally:
            return current_url

    def download_file(self):
        """
        With Selenium you can't download file by browser. So this method will
        download link's href or form's action by urllib and you can check
        status code, headers and data.
        You could download it by yourself, but this handle also cookies and
        form's data.
        """
        return DownloadFile(self)


class _SelectWrapper(_WebElementWrapper, Select):
    def __init__(self, webelement):
        #  WebElementWrapper is created by coping __dict__ of WebElement instance
        #+ in method __new__ of _WebElementWrapper. So there have to be called
        #+ only init method of Select.
        Select.__init__(self, webelement)


class Chrome(_WebdriverWrapper, Chrome):
    pass


class Firefox(_WebdriverWrapper, Firefox):
    pass


class Ie(_WebdriverWrapper, Ie):
    pass


class Opera(_WebdriverWrapper, Opera):
    pass


class PhantomJS(_WebdriverWrapper, PhantomJS):
    pass


class Remote(_WebdriverWrapper, Remote):
    pass
