# -*- coding: utf-8 -*-

from mock import Mock, call
import unittest

from webdriverwrapper.gotopage import go_to_page, _make_url


class MakeUrlTest(unittest.TestCase):
    def test_make_url(self):
        url = _make_url('path', 'qu=ery', 'example.com')
        self.assertEquals(url, 'http://example.com/path?qu=ery')

    def test_make_url_query_as_string(self):
        url = _make_url(query='qu=ery')
        self.assertEquals(url, 'http://?qu=ery')

    def test_make_url_query_as_dictionary(self):
        url = _make_url(query={'qu': 'ery'})
        self.assertEquals(url, 'http://?qu=ery')

    def test_make_url_pass_protocol(self):
        url = _make_url(domain='https://example.com')
        self.assertEquals(url, 'https://example.com')

    def test_make_url_not_pass_protocol(self):
        url = _make_url(domain='example.com')
        self.assertEquals(url, 'http://example.com')


class GoToPageTest(unittest.TestCase):
    def test_go_to_page(self):
        driver = Mock()
        go_to_page(driver, 'path', {'qu': 'ery'}, 'example.com')
        self.assertEquals(driver.get.call_args, call('http://example.com/path?qu=ery'))

    def test_go_to_page_whole_url_in_path(self):
        driver = Mock()
        go_to_page(driver, 'http://example.com/path?qu=ery')
        self.assertEquals(driver.get.call_args, call('http://example.com/path?qu=ery'))
