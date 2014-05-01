# -*- coding: utf-8 -*-

import os

from webdriverwrapper import testcase, Chrome
from webdriverwrapper.decorators import *
from webdriverwrapper.exceptions import ErrorsException


class TestCaseTest(testcase.WebdriverTestCase):
    instances_of_driver = testcase.ONE_INSTANCE_PER_TESTCASE

    def init(self):
        self.path = os.path.dirname(os.path.realpath(__file__))

    def _get_driver(self):
        return Chrome()

    # This test will be OK. Error in the middle Selenium do not see.
    def test_not_check_errors_in_middle_of_test(self):
        self.go_to('file://%s/html/error_message.html' % self.path)
        self.go_to('file://%s/html/some_page.html' % self.path)

    # There is explicit call of check_errors, therefor this test fails.
    def test_check_errors_in_middle_of_test(self):
        self.go_to('file://%s/html/error_message.html' % self.path)
        try:
            self.check_errors()
        except ErrorsException:
            pass  # ok
        except Exception as exc:
            self.fail('Wrong exception! %s' % str(exc))
        else:
            self.fail('Exception not raised!')
        self.go_to('file://%s/html/some_page.html' % self.path)

    def test_make_screenshot(self):
        self.go_to('file://%s/html/some_page.html' % self.path)
        self.make_screenshot('/tmp/test-screenshot.png')
