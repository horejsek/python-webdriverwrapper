# -*- coding: utf-8 -*-

import requests

from webdriverwrapper.utils import force_text
from webdriverwrapper.gotopage import _get_domain_from_driver, _make_url

__all__ = ('DownloadUrl', 'DownloadFile')


class _Download(object):

    @property
    def method(self):
        return self._response.request.method.lower()

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def encoding(self):
        return self._response.encoding

    @property
    def headers(self):
        return self._response.headers

    @property
    def data(self):
        return self._response.text

    def _make_request(self):
        is_post, url, data = self._get_url_and_data()
        cookies = self._get_cookies()

        if is_post:
            self._response = requests.post(url, data=data, cookies=cookies)
        else:
            self._response = requests.get(url, params=data, cookies=cookies)

    def _get_cookies(self):
        all_cookies = self._driver.get_cookies()
        return dict((cookie['name'], cookie['value']) for cookie in all_cookies)


class DownloadUrl(_Download):

    def __init__(self, driver, url):
        self._driver = driver

        if not url:
            url = self._driver.current_url
        self._url = url
        self._make_request()

    def _get_url_and_data(self):
        domain = _get_domain_from_driver(self._driver)
        is_post = False
        url = _make_url(path=self._url, domain=domain)
        data = None
        return is_post, url, data


class DownloadFile(_Download):

    def __init__(self, elm):
        self._elm = elm
        self._driver = elm._parent
        self._make_request()

    def _get_url_and_data(self):
        is_post = False
        data = None

        url = self._elm.get_attribute('href')
        # If no href, element can be some form button. Then use attribute action
        # of that form.
        if not url:
            form_elm = self._get_form_elm()
            if form_elm:
                url = form_elm.get_attribute('action')
                data = self._get_form_data()
                is_post = form_elm.get_attribute('method') == 'post'
        # If form has no action defined or it is not form, just use current url.
        if not url:
            url = self._elm.current_url

        return is_post, url, data

    def _get_form_data(self):
        form_elm = self._get_form_elm()
        if not form_elm:
            return None

        elms = form_elm.get_elms(xpath='.//*[@name]')
        data = dict((
            force_text(elm.get_attribute('name')).encode('utf8'),
            force_text(elm.get_attribute('value')).encode('utf8'),
        ) for elm in elms)
        return data

    def _get_form_elm(self):
        try:
            form_elm = self._elm.get_elm(xpath='.//ancestor::form')
        except Exception:
            return None
        else:
            return form_elm
