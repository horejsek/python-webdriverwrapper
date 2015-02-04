# -*- coding: utf-8 -*-

import os

import pytest

__all__ = ('pytest_report_header', 'pytest_runtest_makereport', 'make_screenshot_of_failed_tests', 'driver')


def pytest_report_header(config):
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
    # execute all other hooks to obtain the report object
    report = __multicall__.execute()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, 'report_' + report.when, report)
    return report


@pytest.yield_fixture(scope='function', autouse=True)
def make_screenshot_of_failed_tests(request, driver):
    yield
    screenshot_path = getattr(request.config, 'webdriverwrapper_screenshot_path', None)
    if screenshot_path and request.node.report_call.failed:
        driver.close_alert(ignore_exception=True)
        name = request.node.nodeid.replace('/', '.').replace(':', '.')
        driver.get_screenshot_as_file(os.path.join(screenshot_path, '{}.png'.format(name)))


@pytest.yield_fixture(scope='function')
def driver(request, _driver):
    _driver.close_other_windows()
    yield _driver
    _driver.check_expected_errors(test_method=request.function)
    _driver.check_expected_infos(test_method=request.function)
