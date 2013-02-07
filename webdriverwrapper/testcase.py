# -*- coding: utf-8 -*-

import unittest
import sys
from selenium.common.exceptions import NoSuchElementException

import exceptions
from webdriverwrapper import Chrome

__all__ = ('WebdriverTestCase',)


class WebdriverTestCase(unittest.TestCase):
    domain = None

    def setUp(self):
        self.driver = self._get_driver()

    def _get_driver(self):
        return Chrome()

    def tearDown(self):
        self.driver.quit()

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        testMethod = getattr(self, self._testMethodName)
        try:
            try:
                self.setUp()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
                return

            ok = False
            try:
                testMethod()
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
        finally:
            result.stopTest(self)

    def _check_errors(self):
        self._check_js_errors()
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
        errors = None

        try:
            error_elms = self.driver.get_elms(class_name='error')
        except NoSuchElementException:
            pass
        else:
            errors = [error_elm.text for error_elm in error_elms]

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
