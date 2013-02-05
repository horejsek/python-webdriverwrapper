# -*- coding: utf-8 -*-

from webdriverwrapper import WebdriverTestCase, GoToPage, ShouldBeOnPage


class TestCase(WebdriverTestCase):
    @GoToPage('http://www.google.com')
    @ShouldBeOnPage('doodles/finder/2013/All%20doodles')
    def test(self):
        self.click('gbqfsb')
        self.contains_text('Doodles')


import unittest
unittest.main()
