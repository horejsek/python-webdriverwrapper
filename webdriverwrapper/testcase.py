# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
import unittest
import sys
from selenium.common.exceptions import NoSuchElementException

import exceptions
from webdriverwrapper import Firefox
from errors import get_error_messages

__all__ = ('WebdriverTestCase',)


ONE_INSTANCE_FOR_ALL_TESTS = 0
ONE_INSTANCE_PER_TESTCASE = 1
ONE_INSTANCE_PER_TEST = 2


class WebdriverTestCase(unittest.TestCase):
    domain = None
    instances_of_driver = ONE_INSTANCE_FOR_ALL_TESTS
    wait_after_test = False

    def __init__(self, *args, **kwds):
        super(WebdriverTestCase, self).__init__(*args, **kwds)
        self.__class__._number_of_test = 0
        self.__class__._count_of_tests = len(filter(lambda m: m.startswith('test'), dir(self)))

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        test_method = getattr(self, self._testMethodName)
        self.__test_method = test_method
        try:
            self._set_up()

            try:
                self.setUp()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
                return

            ok = False
            try:
                test_method()
                ok = True
            except self.failureException:
                result.addFailure(self, sys.exc_info())
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())

            try:
                self._check_errors()
            except:
                ok = False
                result.addError(self, sys.exc_info())

            try:
                self.tearDown()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
                ok = False

            if ok:
                result.addSuccess(self)

            # Is nice to see at break point if test passed or not.
            # So this call have to be after all addError/addSuccess calls.
            self._tear_down()
        finally:
            result.stopTest(self)

    def _set_up(self):
        self.__class__._number_of_test += 1
        if not hasattr(WebdriverTestCase, 'driver'):
            WebdriverTestCase.driver = self._get_driver()

    def _get_driver(self):
        return Firefox()

    def _tear_down(self):
        if self.wait_after_test:
            self.break_point()

        if self.instances_of_driver == ONE_INSTANCE_PER_TEST or (
            self.instances_of_driver == ONE_INSTANCE_PER_TESTCASE and
            self._number_of_test == self._count_of_tests
        ):
            del WebdriverTestCase.driver

    def break_point(self):
        logging.info('Break point. Type enter to continue.')
        raw_input()

    def debug(self, msg):
        logging.info(msg)

    def _check_errors(self):
        self._check_js_errors()
        #  Check for any error message only if there isn't decorator which
        #+ already checked it.
        if not getattr(self.__test_method, '__should_be_error__', False):
            self._check_error_messages()

    def _check_js_errors(self):
        """Check for JS errors. This method is called after each test.
        For that you have to add to your page this JavaScript:

            <script type="text/javascript">
                window.jsErrors = [];
                window.onerror = function(errorMessage) {
                    window.jsErrors[window.jsErrors.length] = errorMessage;
                }
            </script>
        """
        js_errors = self.driver.execute_script('return window.jsErrors')
        if js_errors:
            raise exceptions.JSErrorsException(self.driver.current_url, js_errors)

    def _check_error_messages(self):
        """There should be tests for error messages on page. This 
        method is called after each test.
        By default it looks for elements with class `error`.
        """
        errors = get_error_messages(self.driver)
        if errors:
            raise exceptions.ErrorsException(self.driver.current_url, errors)


    ### Aliases to driver.

    def find_elements_by_text(self, text):
        return self.driver.find_elements_by_text(text)

    def contains_text(self, text):
        return self.driver.contains_text(text)

    def get_elm(self, *args, **kwds):
        return self.driver.get_elm(*args, **kwds)

    def get_elms(self, *args, **kwds):
        return self.driver.get_elms(*args, **kwds)

    def click(self, *args, **kwds):
        self.driver.click(*args, **kwds)

    def wait_for_element(self, *args, **kwds):
        self.driver.wait_for_element(*args, **kwds)

    def go_to(self, *args, **kwds):
        self.driver.go_to(*args, **kwds)
