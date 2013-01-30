# -*- coding: utf-8 -*-

import inspect
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


class _WebdriverBaseWrapper(object):
    def find_elements_by_text_in_page(self, text):
        """Find every element in page which contain `text`."""
        elms = self.find_elements_by_xpath('.//*[contains(text(), "%s")]' % text)
        return elms

    def contains_text(self, text):
        """Does page contains `text`?"""
        return bool(self.find_elements_by_text_in_page(text))

    def get_elm(self, id_=None, class_=None, name=None, xpath=None, parent_id=None, parent_class=None, parent_name=None):
        elms = self.get_elms(id_, class_, name, xpath, parent_id, parent_class, parent_name)
        if not elms:
            raise NoSuchElementException(
                'No element [id=%s, class=%s, name=%s, xpath=%s] found in parent element [id=%s, class=%s, name=%s].' % (
                    id_, class_, name, xpath, parent_id, parent_class, parent_name,
                )
            )
        return elms[0]

    def get_elms(self, id_=None, class_=None, name=None, xpath=None, parent_id=None, parent_class=None, parent_name=None):
        if parent_id or parent_class or parent_name:
            parent = self.get_elm(parent_id, parent_class, parent_name)
        else:
            parent = self

        if len(filter(lambda x: x is not None, (id_, class_, name, xpath))) > 1:
            raise Exception('You can find element only by one param.')

        if id_ is not None:
            return parent.find_elements_by_id(id_)
        elif class_ is not None:
            return parent.find_elements_by_class_name(class_)
        elif name is not None:
            return parent.find_elements_by_name(name)
        elif xpath is not None:
            return parent.find_elements_by_xpath(xpath)
        else:
            raise Exception('You must specify id or name of element on which you want to click.')

    def click(self, *args, **kwds):
        if args or kwds:
            elm = self.get_elm(*args, **kwds)
            elm.click()
        else:
            super(_WebdriverBaseWrapper, self).click()


class _WebdriverWrapper(_WebdriverBaseWrapper):
    def wait_for_element(self, timeout=10, *args, **kwds):
        """Alias for WebDriverWait(driver, timeout).until(lambda driver: driver.get_elm(...))."""
        return WebDriverWait(self, timeout).until(lambda driver: driver.get_elm(*args, **kwds))


class _WebElementWrapper(_WebdriverBaseWrapper, WebElement):
    def __new__(cls, webelement):
        instance = super(_WebElementWrapper, cls).__new__(cls)
        instance.__dict__.update(webelement.__dict__)
        return instance

    def __init__(self, webelement):
        pass


def _webdriver_wrapper_decorator(cls):
    for name, method in inspect.getmembers(cls, inspect.ismethod):
        setattr(cls, name, _webelement_wrapper_decorator(method))
    return cls


def _webelement_wrapper_decorator(f):
    def wrapper(*args, **kwds):
        res = f(*args, **kwds)
        if type(res) is WebElement:
            if res.tag_name == 'form':
                res = Form(res)
            else:
                res = _WebElementWrapper(res)
        return res
    return wrapper


@_webdriver_wrapper_decorator
class Chrome(Chrome, _WebdriverWrapper):
    pass


@_webdriver_wrapper_decorator
class Firefox(Firefox, _WebdriverWrapper):
    pass


@_webdriver_wrapper_decorator
class Ie(Ie, _WebdriverWrapper):
    pass


@_webdriver_wrapper_decorator
class Opera(Opera, _WebdriverWrapper):
    pass


@_webdriver_wrapper_decorator
class Remote(Remote, _WebdriverWrapper):
    pass


from forms import Form

