# -*- coding: utf-8 -*-

from webdriverwrapper.webdriverwrapper import _WebElementWrapper

from webdriverwrapper_test import WebdriverWrapperBaseClassTest


class WebdriverWrapperBaseTest(WebdriverWrapperBaseClassTest):
    def test_returns_wrapped_element(self):
        self.driver.go_to('http://www.google.com')
        element = self.driver.find_element_by_id('gbqfq')
        self.assertTrue(isinstance(element, _WebElementWrapper), 'Element instance is not WebElementWrapper')

    def test_find_elements_by_text(self):
        self.go_to('file://%s/html/find_elements.html' % self.path)
        #  Check that text there is only one element - other elements are ignored
        #+ by attribute data-selenium-not-search.
        elms = self.find_elements_by_text('text')
        self.assertEqual(len(elms), 1)
