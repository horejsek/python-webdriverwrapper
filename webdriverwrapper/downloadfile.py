# -*- coding: utf-8 -*-

import urllib
import urllib2

__all__ = ('DownloadFile',)


class DownloadFile(object):
    def __init__(self, elm):
        self._elm = elm
        self._make_request()

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
        self._method = request.get_method().lower()
        self._result = urllib2.urlopen(request)
        self._data = self._result.read()

    def _create_request(self):
        url = self._get_url()
        post_data = self._get_post_data()
        request = urllib2.Request(url, post_data)
        for name, value in self._iter_cookies():
            request.add_header('cookie', '%s=%s' % (name, value))
        return request

    def _get_url(self):
        elm = self._elm
        url = elm.get_attribute('href')
        #  If not, element can by some form button. Then use attribute action
        #+ of that form.
        if not url:
            try:
                form_elm = elm.get_elm(xpath='.//ancestor::form')
            except:
                pass
            else:
                url = form_elm.get_attribute('action')
        #  If form has no action defined or it is not form, just use current url.
        if not url:
            url = elm.current_url
        return url

    def _get_post_data(self):
        elm = self._elm
        post_data = None

        try:
            form_elm = elm.get_elm(xpath='.//ancestor::form')
        except:
            pass
        else:
            if form_elm.get_attribute('method') == 'post':
                post_data = {
                    elm.get_attribute('name'): elm.get_attribute('value'),
                }

        if post_data:
            post_data = urllib.urlencode(post_data)
        return post_data

    def _iter_cookies(self):
        all_cookies = self._elm._parent.get_cookies()
        for cookie in all_cookies:
            yield cookie['name'], cookie['value']
