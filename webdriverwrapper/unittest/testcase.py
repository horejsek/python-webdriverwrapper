# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
logging.basicConfig(level=logging.INFO)
import unittest
import sys

import webdriverwrapper.exceptions as exceptions
from webdriverwrapper.wrapper import Firefox, Chrome, ChromeOptions

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
    """
    Base ``TestCase`` used for testing with :py:mod:`unittest`.

    Example:

    .. code-block:: python

        class TestCase(webdriverwrapper.unittest.WebdriverTestCase):
            domain = 'www.google.com'
            instances_of_driver = webdriverwrapper.unittest.ONE_INSTANCE_PER_TESTCASE
            screenshot_path = os.path.join('/', 'tmp', 'testreport')

            def _get_driver(self):
                return Chrome()

            def test_doodle(self):
                self.click('gbqfsb')
                self.assertTrue(self.contains_text('Doodles'))

            def test_search(self):
                self.get_elm('gbqf').fill_out_and_submit({
                    'q': 'hello',
                })
                self.wait_for_element(id_='resultStats')
    """

    domain = None
    """
    If you want working relative :py:meth:`go_to <webdriverwrapper.wrapper._WebdriverWrapper.go_to>`
    without having to call for first time
    :py:meth:`get <selenium.webdriver.remote.webdriver.WebDriver.get>` (because
    before that you can't use relative path), set this attribute.
    """

    instances_of_driver = ONE_INSTANCE_FOR_ALL_TESTS
    """
    Specify when you want to create *fresh* driver. By default there is one
    driver for all tests (:py:attr:`.ONE_INSTANCE_FOR_ALL_TESTS`) and you have
    to close it by yourself by calling :py:meth:`.quit_driver`.

    If you need clear cookies, local storage and everything, then consider to use
    new driver for every ``TestCase`` or even every test method.
    """

    wait_after_test = False
    """
    For debug only. When you set to ``True``, it will wait for pressing enter
    after each test before moving to next test. Ideal when you need to check
    out for example Chrome console.

    But maybe better debuging is with :py:meth:`.break_point`.
    """

    screenshot_path = ''
    """
    When you set this path, it will make automatically screenshots of failed
    tests and saved them to this path.
    """

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
                    self.driver.check_expected_errors(test_method)
                    self.driver.check_expected_infos(test_method)
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
                self.driver.check_expected_errors(test_method)
                self.driver.check_expected_infos(test_method)
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
        Save screenshot to :py:attr:`.screenshot_path` with given name
        ``screenshot_name``. If name is not given, then the name is name of
        current test (``self.id()``).

        .. versionchanged:: 2.2
            Use ``make_screenshot`` directly on ``driver`` instead. This method
            is used for making screenshot of failed tests and therefor does
            nothing if ``screenshot_path`` is not configured. It stays there
            only for compatibility.
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
            WebdriverTestCase.screenshot_path = self.screenshot_path
            WebdriverTestCase._main_window = WebdriverTestCase.driver.current_window_handle
            if self.domain:
                WebdriverTestCase.driver.get(self.domain)

        # Ensure that test starts in main window.
        if self.driver.current_window_handle != self._main_window:
            self.driver.switch_to_window(self._main_window)

    def _get_driver(self):
        """
        Create driver. By default it creates Firefox. Change it to your needs.
        """
        return Firefox()

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
        """
        When you set :py:attr:`.instances_of_driver` to
        :py:attr:`.ONE_INSTANCE_FOR_ALL_TESTS` (which is default), then you
        have to quit driver by yourself by this method.
        """
        if hasattr(WebdriverTestCase, 'driver'):
            WebdriverTestCase.driver.quit()
            del WebdriverTestCase.driver

    def debug(self, msg):
        logging.info(msg)

    ### Aliases to driver.

    def break_point(self):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverWrapper.break_point`.
        """
        self.driver.break_point()

    def check_errors(self, expected_error_page=None, allowed_error_pages=[], expected_error_messages=[], allowed_error_messages=[]):
        """
        Alias for :py:meth:`~webdriverwrapper.errors.WebdriverWrapperErrorMixin.check_errors`.

        .. versionchanged:: 2.0
            Only alias. Code moved to wrapper so it could be used also by pytest.
        """
        self.driver.check_errors(expected_error_page, allowed_error_pages, expected_error_messages, allowed_error_messages)

    def find_element_by_text(self, text):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverBaseWrapper.find_element_by_text`.

        .. versionadded:: 2.0
        """
        return self.driver.find_element_by_text(text)

    def find_elements_by_text(self, text):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverBaseWrapper.find_elements_by_text`.
        """
        return self.driver.find_elements_by_text(text)

    def contains_text(self, text):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverBaseWrapper.contains_text`.
        """
        return self.driver.contains_text(text)

    def get_elm(self, *args, **kwds):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverBaseWrapper.get_elm`.
        """
        return self.driver.get_elm(*args, **kwds)

    def get_elms(self, *args, **kwds):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverBaseWrapper.get_elms`.
        """
        return self.driver.get_elms(*args, **kwds)

    def click(self, *args, **kwds):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverBaseWrapper.click`.
        """
        self.driver.click(*args, **kwds)

    def wait_for_element(self, *args, **kwds):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverWrapper.wait_for_element`.
        """
        return self.driver.wait_for_element(*args, **kwds)

    def wait(self, timeout=10):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverWrapper.wait`.
        """
        return self.driver.wait(timeout)

    def go_to(self, *args, **kwds):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverWrapper.go_to`.
        """
        self.driver.go_to(*args, **kwds)

    def switch_to_window(self, window_name=None, title=None, url=None):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverWrapper.switch_to_window`.
        """
        self.driver.switch_to_window(window_name, title, url)

    def close_window(self, window_name=None, title=None, url=None):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverWrapper.close_window`.
        """
        self.driver.close_window(window_name, title, url)

    def close_other_windows(self):
        """
        Alias for :py:meth:`~webdriverwrapper.wrapper._WebdriverWrapper.close_other_windows`.
        """
        self.driver.close_other_windows()
