# -*- coding: utf-8 -*-

#  In this test is not used TestCase's aliases, because it's not target of this
#+ test. There is testing mainly driver instance.
#  WebdriverTestCase is used because of creating of driver.

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
        self._test_exception(lambda: self.driver.get_elm('some_non_exist_id'))

    def test_exception_from_find_methods(self):
        self._test_exception(lambda: self.driver.find_element_by_id('some_non_exist_id'))

    def _test_exception(self, callback):
        try:
            callback()
        except NoSuchElementException, e:
            self.assertTrue(
                e.msg and 'some_non_exist_id' in e.msg and 'http://' in e.msg,
                'Exception has bad message (%s)' % e.msg,
            )
        except Exception, e:
            self.fail('Excepted NoSuchElementException, but raised %s instead' % e.__class__)
        else:
            self.fail('NoSuchElementException not raised')

    def test_returns_wrapped_element(self):
        element = self.driver.find_element_by_id('gbqfq')
        self.assertTrue(isinstance(element, _WebElementWrapper), 'Element instance is not WebElementWrapper')

    def test_find_elements_by_text(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.go_to('file://%s/html/find_elements.html' % path)

        #  Check that text there is only one element - other elements are ignored
        #+ by attribute data-selenium-not-search.
        elms = self.find_elements_by_text('text')
        self.assertEqual(len(elms), 1)
