# -*- coding: utf-8 -*-

import os

from webdriverwrapper import unittest, Chrome
from webdriverwrapper.decorators import *


class TestCaseDecoratorsTest(unittest.WebdriverTestCase):
    instances_of_driver = unittest.ONE_INSTANCE_PER_TESTCASE

    def _get_driver(self):
        return Chrome()

    @expected_error_messages('some-error')
    def test_should_be_error(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.driver.get('file://%s/html/error_message.html' % path)

    @expected_info_messages('some-info')
    def test_should_be_info(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.driver.get('file://%s/html/info_message.html' % path)
