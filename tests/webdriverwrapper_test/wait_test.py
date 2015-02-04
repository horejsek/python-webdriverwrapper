# -*- coding: utf-8 -*-

from webdriverwrapper_test import WebdriverWrapperBaseClassTest


class WebdriverWaitTest(WebdriverWrapperBaseClassTest):
    def setUp(self):
        self.driver.get('file://%s/html/some_page.html' % self.path)

    def test_wait_for_element(self):
        elm = self.wait_for_element(id_='somepage')
        self.assertEqual(elm.tag_name, 'div')

    def test_wait_for_element_fail(self):
        with self.assertRaises(Exception):
            self.wait_for_element(id_='some_non_exist_id')
