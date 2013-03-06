# -*- coding: utf-8 -*-

from webdriverwrapper import Chrome
from webdriverwrapper.testcase import WebdriverTestCase
from webdriverwrapper.decorators import GoToPage, ShouldBeOnPage


class TestCase(WebdriverTestCase):
    domain = 'www.google.com'

    def _get_driver(self):
        return Chrome()

    @GoToPage('')
    @ShouldBeOnPage('doodles/finder/2013/All%20doodles')
    def testDoodle(self):
        self.click('gbqfsb')
        self.contains_text('Doodles')

    @GoToPage('')
    def testSearch(self):
        self.get_elm('gbqf').fill_out_and_submit({
            'q': 'hello',
        })
        self.wait_for_element(id_='resultStats')


import unittest
unittest.main()
