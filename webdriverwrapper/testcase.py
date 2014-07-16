# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
logging.basicConfig(level=logging.INFO)
import unittest
import sys

import webdriverwrapper.exceptions as exceptions
from webdriverwrapper.wrapper import Firefox, Chrome, ChromeOptions
from webdriverwrapper.errors import get_error_page, get_error_messages

__all__ = (
    'WebdriverTestCase',
    'ONE_INSTANCE_FOR_ALL_TESTS',
    'ONE_INSTANCE_PER_TESTCASE',
    'ONE_INSTANCE_PER_TEST',
)


ONE_INSTANCE_FOR_ALL_TESTS = 0
ONE_INSTANCE_PER_TESTCASE = 1
ONE_INSTANCE_PER_TEST = 2


class WebdriverTestCase(unittest.TestCase):
    domain = None
    instances_of_driver = ONE_INSTANCE_FOR_ALL_TESTS
    wait_after_test = False
    screenshot_path = ''

    def __init__(self, *args, **kwds):
        super(WebdriverTestCase, self).__init__(*args, **kwds)
        self.__class__._number_of_test = 0
        self.__class__._count_of_tests = len([m for m in dir(self) if m.startswith('test')])
        self.init()

    def init(self):
        pass

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        test_method = getattr(self, self._testMethodName)
        self._test_method = test_method
        try:
            ok = False
            self._set_up()

            try:
                self.setUp()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
                #  setUp can fail because of app in some state returns internal
                #+ server error. It's good to know about it - it can say more
                #+ than that some element couldn't be found.
                try:
                    self._check_errors()
                except:
                    result.addError(self, sys.exc_info())
                return

            try:
                test_method()
                ok = True
            except self.failureException:
                self.make_screenshot()
                result.addFailure(self, sys.exc_info())
            except KeyboardInterrupt:
                raise
            except:
                self.make_screenshot()
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
            if not ok:
                self.make_screenshot()

            result.stopTest(self)
            # Is nice to see at break point if test passed or not.
            # So this call have to be after stopTest which print result of test.
            self._tear_down()

    def make_screenshot(self, screenshot_name=None):
        """
        Save screenshot to `self.screenshot_path` with given name `screenshot_name`.
        If name is not given, then the name is name of current test (`self.id()`).
        """
        if not screenshot_name:
            # Without name (and possibly path) we cannot make screenshot. Don't
            # know where to store it.
            if not self.screenshot_path:
                return
            screenshot_name = self.id()

        # Close unexpected alerts (it's blocking and then tests fails completely).
        self.driver.close_alert(ignore_exception=True)

        self.driver.get_screenshot_as_file('%s/%s.png' % (self.screenshot_path, screenshot_name))

    def _set_up(self):
        self.__class__._number_of_test += 1
        if not hasattr(WebdriverTestCase, 'driver'):
            WebdriverTestCase.driver = self._get_driver()
            WebdriverTestCase._main_window = WebdriverTestCase.driver.current_window_handle
            if self.domain:
                WebdriverTestCase.driver.go_to(self.domain)

        # Ensure that test starts in main window.
        if self.driver.current_window_handle != self._main_window:
            self.driver.switch_to_window(self._main_window)

    def _get_driver(self):
        return Firefox()

    def _get_driver_with_proxy(self):
        opt = ChromeOptions()
        opt.add_argument('--proxy-auto-detect')
        return Chrome(chrome_options=opt)

    def _tear_down(self):
        if self.wait_after_test:
            self.break_point()

        if self.instances_of_driver == ONE_INSTANCE_PER_TEST or (
            self.instances_of_driver == ONE_INSTANCE_PER_TESTCASE and
            self._number_of_test == self._count_of_tests
        ):
            self.quit_driver()

    @staticmethod
    def quit_driver():
        if hasattr(WebdriverTestCase, 'driver'):
            WebdriverTestCase.driver.quit()
            del WebdriverTestCase.driver

    def break_point(self):
        logging.info('Break point. Type enter to continue.')
        raw_input()

    def debug(self, msg):
        logging.info(msg)

    def check_errors(self):
        self._check_errors(force_check=True)

    def _check_errors(self, force_check=False):
        # Close unexpected alerts (it's blocking and then tests fails completely).
        self.driver.close_alert(ignore_exception=True)

        self._check_js_errors()
        #  Check for any error message only if there isn't decorator which
        #+ already checked it.
        if force_check or not getattr(self._test_method, '__should_be_error_page__', False):
            self._check_error_page()
        if force_check or not getattr(self._test_method, '__should_be_error__', False):
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

    def _check_error_page(self):
        """There should be tests for error page. This method is called after each
        test. By default it looks for elements with class `error-page`.
        """
        error_page = get_error_page(self.driver)
        if error_page:
            raise exceptions.ErrorPageException(self.driver.current_url, error_page)

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
        return self.driver.wait_for_element(*args, **kwds)

    def wait(self, timeout=10):
        return self.driver.wait(timeout)

    def go_to(self, *args, **kwds):
        self.driver.go_to(*args, **kwds)

    def switch_to_window(self, window_name=None, title=None, url=None):
        self.driver.switch_to_window(window_name, title, url)

    def close_window(self, window_name=None, title=None, url=None):
        self.driver.close_window(window_name, title, url)

    def close_other_windows(self):
        self.driver.close_other_windows()
