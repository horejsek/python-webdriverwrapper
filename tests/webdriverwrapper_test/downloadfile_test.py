# -*- coding: utf-8 -*-

from webdriverwrapper_test import WebdriverWrapperBaseClassTest


class DownloadFileTest(WebdriverWrapperBaseClassTest):
    def init(self):
        super(DownloadFileTest, self).init()
        self.file_data = open('/%s/files/some_file.txt' % self.path, 'rb').read()
        self.html_data = open('/%s/html/download_file.html' % self.path, 'rb').read()

    def setUp(self):
        self.go_to('file://%s/html/download_file.html' % self.path)

    def test_download_file_by_link(self):
        self._test_download_file('link', self.file_data)

    def test_download_file_by_form_with_action(self):
        self._test_download_file('btn-action', self.file_data)

    def test_download_file_by_form_by_get(self):
        self._test_download_file('btn-get', self.html_data)

    def test_download_file_by_form_by_post(self):
        self._test_download_file('btn-post', self.html_data, 'post')

    def _test_download_file(self, elm_id, file_data, method='get'):
        f = self.get_elm(elm_id).download_file()
        self.assertEqual(f.method, method)
        self.assertEqual(f.data, file_data)
