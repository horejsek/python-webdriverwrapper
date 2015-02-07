# -*- coding: utf-8 -*-

from webdriverwrapper import Chrome
from webdriverwrapper.testcase import WebdriverTestCase


class TestCase(WebdriverTestCase):
    domain = 'www.google.com'

    def _get_driver(self):
        return Chrome()

    def testDoodle(self):
        self.click('gbqfsb')
        self.assertTrue(self.contains_text('Doodles'))

    def testSearch(self):
        self.get_elm('gbqf').fill_out_and_submit({
            'q': 'hello',
        })
        self.wait_for_element(id_='resultStats')


import unittest
unittest.main()
