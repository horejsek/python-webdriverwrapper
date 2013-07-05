# -*- coding: utf-8 -*-

from webdriverwrapper.wrapper import _WebElementWrapper

from webdriverwrapper_test import WebdriverWrapperBaseClassTest


class WebdriverWrapperBaseTest(WebdriverWrapperBaseClassTest):
    def test_returns_wrapped_element(self):
        self.driver.go_to('http://www.google.com')
        element = self.driver.find_element_by_id('gbqfq')
        self.assertTrue(isinstance(element, _WebElementWrapper), 'Element instance is not WebElementWrapper')
