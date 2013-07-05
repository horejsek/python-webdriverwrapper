# -*- coding: utf-8 -*-

from webdriverwrapper import Chrome
from webdriverwrapper import fuzzytestcase
from webdriverwrapper.errors import CanBeError
from webdriverwrapper.testcase import WebdriverTestCase


class ProjectBaseTestCase(WebdriverTestCase):
    domain = 'http://www.google.com'

    def _get_driver(self):
        return Chrome()


class FuzzyTestCaseType(fuzzytestcase.FuzzyTestCaseType):
    count_of_clicks = 5
    can_be_error_decorator = CanBeError


class FuzzyTest(ProjectBaseTestCase, fuzzytestcase.FuzzyTestCase):
    __metaclass__ = FuzzyTestCaseType

    def is_error_page(self):
        return super(FuzzyTest, self).is_error_page()

    def reset_after_page_error(self):
        super(FuzzyTest, self).reset_after_page_error()

    def get_clickable_elements(self):
        return super(FuzzyTest, self).get_clickable_elements()


import unittest
unittest.main()
