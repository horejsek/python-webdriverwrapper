# -*- coding: utf-8 -*-

from webdriverwrapper import WebdriverTestCase


class TestCase(WebdriverTestCase):
    def test(self):
        self.driver.get('http://www.google.com')
        self.driver.click('gbqfsb')
        self.driver.contains_text('Doodles')


import unittest
unittest.main()
