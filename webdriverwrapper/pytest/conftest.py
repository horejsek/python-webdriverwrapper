# -*- coding: utf-8 -*-

import os

import pytest

__all__ = ('pytest_report_header', 'pytest_runtest_makereport', 'set_driver_to_test_for_failed_screenshot', 'driver')


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

    if report.when in ('call', 'teardown') and report.failed:
        make_screenshot_of_failed_tests(item.obj.driver, item.config, item.nodeid)

    return report


@pytest.fixture(scope='function', autouse=True)
def set_driver_to_test_for_failed_screenshot(request, driver):
    request.node.obj.driver = driver


def make_screenshot_of_failed_tests(driver, config, nodeid):
    screenshot_path = getattr(config, 'webdriverwrapper_screenshot_path', None)
    if not screenshot_path:
        return

    driver.close_alert(ignore_exception=True)
    name = nodeid.replace('/', '.').replace(':', '.')
    driver.get_screenshot_as_file(os.path.join(screenshot_path, '{}.png'.format(name)))


@pytest.yield_fixture(scope='function')
def driver(request, _driver):
    _driver.close_other_windows()
    yield _driver
    _driver.check_expected_errors(test_method=request.function)
    _driver.check_expected_infos(test_method=request.function)
