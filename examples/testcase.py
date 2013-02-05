# -*- coding: utf-8 -*-

from webdriverwrapper import WebdriverTestCase


class TestCase(WebdriverTestCase):
    def test(self):
        self.driver.get('http://www.google.com')
        self.click('gbqfsb')
        self.contains_text('Doodles')


import unittest
unittest.main()
