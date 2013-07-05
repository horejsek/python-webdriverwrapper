# -*- coding: utf-8 -*-

import os

from webdriverwrapper import testcase, Chrome
from webdriverwrapper.decorators import *


class TestCaseDecoratorsTest(testcase.WebdriverTestCase):
    instances_of_driver = testcase.ONE_INSTANCE_PER_TESTCASE

    def _get_driver(self):
        return Chrome()

    @GoToPage('www.seznam.cz')
    def test_go_to_page(self):
        self.assertEquals(self.driver.current_url, 'http://www.seznam.cz/')

    @ShouldBeOnPage('http://www.youtube.com')
    def test_should_be_on_page(self):
        self.go_to('www.youtube.com')

    @ShouldBeError('some-error')
    def test_should_be_error(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.go_to('file://%s/html/error_message.html' % path)

    @ShouldBeInfo('some-info')
    def test_should_be_info(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.go_to('file://%s/html/info_message.html' % path)
