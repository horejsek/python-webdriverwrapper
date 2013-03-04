# -*- coding: utf-8 -*-

#  In this test is not used TestCase's aliases, because it's not target of this
#+ test. There is testing mainly driver instance.
#  WebdriverTestCase is used because of creating of driver.

from mock import Mock, call
import os

from webdriverwrapper import testcase, Chrome
from webdriverwrapper.webdriverwrapper import _WebElementWrapper
from webdriverwrapper.exceptions import NoSuchElementException


class WebdriverWrapperTest(testcase.WebdriverTestCase):
    instances_of_driver = testcase.ONE_INSTANCE_PER_TESTCASE

    def setUp(self):
        self.driver.go_to('http://www.google.com')

    def _get_driver(self):
        return Chrome()

    def test_exception(self):
        try:
            self.driver.get_elm('some_non_exist_id')
        except NoSuchElementException, e:
            self.assertTrue(
                e.msg and 'some_non_exist_id' in e.msg, 
                'Exception has bad message (%s)' % e.msg,
            )
        except Exception, e:
            self.fail('Excepted NoSuchElementException, but raised %s instead' % e.__class__)
        else:
            self.fail('NoSuchElementException not raised')

    def test_exception_from_find_methods(self):
        try:
            self.driver.find_element_by_id('some_non_exist_id')
        except NoSuchElementException, e:
            self.assertTrue(
                e.msg and 'some_non_exist_id' in e.msg, 
                'Exception has bad message (%s)' % e.msg,
            )
        except Exception, e:
            self.fail('Excepted NoSuchElementException, but raised %s instead' % e.__class__)
        else:
            self.fail('NoSuchElementException not raised')

    def test_returns_wrapped_element(self):
        element = self.driver.find_element_by_id('gbqfq')
        self.assertTrue(isinstance(element, _WebElementWrapper), 'Element instance is not WebElementWrapper')
