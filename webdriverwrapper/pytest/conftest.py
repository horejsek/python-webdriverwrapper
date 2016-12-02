# -*- coding: utf-8 -*-

import os

import pytest

__all__ = ('pytest_report_header', 'pytest_runtest_makereport', 'set_driver_to_test_for_failed_screenshot', 'driver')


def pytest_report_header(config):
    """
    Pytest hook, see :py:func:`_pytest.hookspec.pytest_report_header` (:ref:`pytest:plugins`).

    It's important to see which URL is testing with which user and where are
    stored screenshots. It will be displayed before run of tests if you set
    some config values like that:

    .. code-block:: python

        def pytest_configure(config):
            config.webdriverwrapper_screenshot_path = os.path.join('/', 'tmp', 'testresults')
            config.webdriverwrapper_testing_url = 'http://example.com'
            config.webdriverwrapper_testing_username = 'testing_username'

    If your web app does not need any user, just don't set it.
    """
    screenshot_path = getattr(config, 'webdriverwrapper_screenshot_path', None)
    testing_url = getattr(config, 'webdriverwrapper_testing_url', None)
    testing_username = getattr(config, 'webdriverwrapper_testing_username', None)

    lines = []

    if screenshot_path:
        lines.append('| Screenshot path: {}'.format(screenshot_path))
    if testing_url:
        lines.append('| Testing URL: {}'.format(testing_url))
    if testing_username:
        lines.append('| Testing username: {}'.format(testing_username))

    if lines:
        wrap_line = '+' + '-' * 75
        lines.insert(0, wrap_line)
        lines.append(wrap_line)

    return lines


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    """
    Pytest hook, see :py:func:`_pytest.hookspec.pytest_runtest_makereport`.

    After each failed test will be generated screenshot if you specify where to
    save these screenshots.

    .. code-block:: python

        def pytest_configure(config):
            config.webdriverwrapper_screenshot_path = os.path.join('/', 'tmp', 'testresults')
    """
    # Execute all other hooks to obtain the report object.
    report = __multicall__.execute()

    if report.when in ('call', 'teardown') and report.failed:
        test_func = _get_test_func(item.obj)
        make_screenshot_of_failed_tests(test_func.driver, item.config, item.nodeid)

    return report


@pytest.fixture(scope='function', autouse=True)
def set_driver_to_test_for_failed_screenshot(request, driver):
    _get_test_func(request.node.obj).driver = driver


def _get_test_func(obj):
    # Test function may be method. But attributes can be set only to functions.
    if hasattr(obj, 'im_func'):  # Python 2
        return obj.im_func
    if hasattr(obj, '__func__'):  # Python 3
        return obj.__func__
    return obj


def make_screenshot_of_failed_tests(driver, config, nodeid):
    screenshot_path = getattr(config, 'webdriverwrapper_screenshot_path', None)
    if not screenshot_path:
        return

    driver.close_alert(ignore_exception=True)
    name = nodeid.replace('/', '.').replace(':', '.')
    driver.get_screenshot_as_file(os.path.join(screenshot_path, '{}.png'.format(name)))


@pytest.yield_fixture(scope='function')
def driver(request, _driver):
    """
    Fixture for testing. This fixture just take your driver by fixture called
    ``_driver`` and after each test call
    :py:meth:`~webdriverwrapper.errors.WebdriverWrapperErrorMixin.check_expected_errors`
    and :py:meth:`~webdriverwrapper.info.WebdriverWrapperInfoMixin.check_expected_infos`.
    You have to just implement creating of your browser.

    .. code-block:: python

        @pytest.yield_fixture(scope='session')
        def _driver():
            driver = Chrome()
            yield driver
            driver.quit()
    """
    _driver.screenshot_path = getattr(request.config, 'webdriverwrapper_screenshot_path', None)
    _driver.close_other_windows()
    yield _driver
    _driver.check_expected_errors(test_method=request.function)
    _driver.check_expected_infos(test_method=request.function)
