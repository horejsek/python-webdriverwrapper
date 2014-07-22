# -*- coding: utf-8 -*-

try:
    from urllib import urlencode
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

from webdriverwrapper.utils import force_text
from webdriverwrapper.gotopage import _get_domain_from_driver, _make_url

__all__ = ('DownloadUrl', 'DownloadFile')


class _Download(object):

    @property
    def method(self):
        return self._method

    @property
    def status_code(self):
        return self._result.code

    @property
    def headers(self):
        return dict(self._result.headers.items())

    @property
    def data(self):
        return self._data

    def _make_request(self):
        request = self._create_request()
        self._request = request
        self._method = request.get_method().lower()
        self._result = urlopen(request)
        self._data = self._result.read()

    def _create_request(self):
        url, data = self._get_url_and_data()
        request = Request(url, data)

        cookie = '; '.join('%s=%s' % (name, value) for name, value in self._iter_cookies())
        request.add_header('cookie', cookie)

        return request


class DownloadUrl(_Download):

    def __init__(self, driver, url):
        self._driver = driver

        if not url:
            url = self._driver.current_url
        self._url = url
        self._make_request()

    def _get_url_and_data(self):
        domain = _get_domain_from_driver(self._driver)
        url = _make_url(path=self._url, domain=domain)
        return url, None

    def _iter_cookies(self):
        all_cookies = self._driver.get_cookies()
        for cookie in all_cookies:
            yield cookie['name'], cookie['value']


class DownloadFile(_Download):

    def __init__(self, elm):
        self._elm = elm
        self._make_request()

    def _get_url_and_data(self):
        elm = self._elm
        data = None
        is_post = False
        url = elm.get_attribute('href')
        #  If not, element can by some form button. Then use attribute action
        #+ of that form.
        if not url:
            form_elm = self._get_form_elm()
            if form_elm:
                url = form_elm.get_attribute('action')
                data = self._get_form_data()
                is_post = form_elm.get_attribute('method') == 'post'
        #  If form has no action defined or it is not form, just use current url.
        if not url:
            url = elm.current_url

        if not is_post:
            if data:
                url = '%(url)s%(mark)s%(data)s' % {
                    'url': url,
                    'mark': '?' if '?' not in url else '&',
                    'data': data,
                }
            data = None

        return url, data

    def _get_form_data(self):
        form_elm = self._get_form_elm()
        if not form_elm:
            return None

        elms = form_elm.get_elms(xpath='.//*[@name]')
        data = dict((
            force_text(elm.get_attribute('name')).encode('utf8'),
            force_text(elm.get_attribute('value')).encode('utf8'),
        ) for elm in elms)
        data = urlencode(data)
        return data

    def _get_form_elm(self):
        try:
            form_elm = self._elm.get_elm(xpath='.//ancestor::form')
        except Exception:
            return None
        else:
            return form_elm

    def _iter_cookies(self):
        all_cookies = self._elm._parent.get_cookies()
        for cookie in all_cookies:
            yield cookie['name'], cookie['value']
