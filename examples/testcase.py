# -*- coding: utf-8 -*-

from webdriverwrapper import WebdriverTestCase, GoToPage, ShouldBeOnPage


class TestCase(WebdriverTestCase):
    domain = 'http://www.google.com'

    @GoToPage('')
    @ShouldBeOnPage('doodles/finder/2013/All%20doodles')
    def test(self):
        self.click('gbqfsb')
        self.contains_text('Doodles')


import unittest
unittest.main()

