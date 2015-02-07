# -*- coding: utf-8 -*-

import os

from webdriverwrapper import unittest, Chrome
from webdriverwrapper.decorators import *
from webdriverwrapper.exceptions import ErrorMessagesException


class TestCaseTest(unittest.WebdriverTestCase):
    instances_of_driver = unittest.ONE_INSTANCE_PER_TESTCASE

    def init(self):
        self.path = os.path.dirname(os.path.realpath(__file__))

    def _get_driver(self):
        return Chrome()

    # This test will be OK. Error in the middle Selenium do not see.
    def test_not_check_errors_in_middle_of_test(self):
        self.driver.get('file://%s/html/error_messages.html' % self.path)
        self.driver.get('file://%s/html/some_page.html' % self.path)

    # There is explicit call of check_errors, therefor this test fails.
    def test_check_errors_in_middle_of_test(self):
        self.driver.get('file://%s/html/error_messages.html' % self.path)
        try:
            self.check_errors()
        except ErrorMessagesException:
            pass  # ok
        except Exception as exc:
            self.fail('Wrong exception! %s' % str(exc))
        else:
            self.fail('Exception not raised!')
        self.driver.get('file://%s/html/some_page.html' % self.path)

    def test_make_screenshot(self):
        self.driver.get('file://%s/html/some_page.html' % self.path)
        self.make_screenshot('/tmp/test-screenshot.png')
