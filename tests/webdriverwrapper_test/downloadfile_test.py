# -*- coding: utf-8 -*-

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from webdriverwrapper_test import WebdriverWrapperBaseClassTest


class DownloadUrlTest(WebdriverWrapperBaseClassTest):
    def init(self):
        super(DownloadUrlTest, self).init()
        self.file_data = open('/%s/files/some_file.txt' % self.path, 'rb').read()
        self.html_data = open('/%s/html/download_file.html' % self.path, 'rb').read()

    def test_by_url(self):
        downloaded_data = self.driver.download_url('file://%s/html/download_file.html' % self.path)
        self.assertEqual(self.html_data, downloaded_data.data)

        downloaded_data2 = self.driver.download_url('file://%s/files/some_file.txt' % self.path)
        self.assertEqual(self.file_data, downloaded_data2.data)

    def test_by_current(self):
        self.go_to('file://%s/html/download_file.html' % self.path)
        downloaded_data = self.driver.download_url()
        self.assertEqual(self.html_data, downloaded_data.data)


class DownloadFileTest(WebdriverWrapperBaseClassTest):
    def init(self):
        super(DownloadFileTest, self).init()
        self.file_data = open('/%s/files/some_file.txt' % self.path, 'rb').read()
        self.html_data = open('/%s/html/download_file.html' % self.path, 'rb').read()

    def setUp(self):
        self.go_to('file://%s/html/download_file.html' % self.path)

    def test_by_link(self):
        self._test_download_file('link', self.file_data)

    def test_by_form_with_action(self):
        self._test_download_file('btn-action', self.file_data)

    def test_by_form_by_get(self):
        self._test_download_file('btn-get', self.html_data)

    def test_by_form_by_post(self):
        self._test_download_file('btn-post', self.html_data, 'post')

    def test_by_form_by_get_with_data(self):
        f = self._test_download_file('btn-get-with-data')
        self.assertEqual(f._request.get_full_url(), 'http://www.google.com/?q=search')

    def test_by_form_by_post_with_data(self):
        f = self._test_download_file('btn-post-with-data', self.html_data, 'post')
        self.assertEqual(f._request.data, urlencode({
            'btn': 'Method POST & data',
            'key': 'val',
        }))

    def _test_download_file(self, elm_id, file_data=None, method='get'):
        f = self.get_elm(elm_id).download_file()
        self.assertEqual(f.method, method)
        if file_data is not None:
            self.assertEqual(f.data, file_data)
        return f
