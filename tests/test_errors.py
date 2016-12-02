# -*- coding: utf-8 -*-

import pytest

from webdriverwrapper.decorators import allowed_error_pages, allowed_any_error_message
from webdriverwrapper.exceptions import ErrorPageException, ErrorMessagesException


@allowed_error_pages('403')
def test_check_error_page(driver_error_page):
    with pytest.raises(ErrorPageException) as excinfo:
        driver_error_page.check_errors()


@allowed_error_pages('403')
def test_check_errors_expected_error_page(driver_error_page):
    driver_error_page.check_errors(expected_error_page='403')


@allowed_error_pages('403')
def test_check_errors_allowed_error_pages(driver_error_page):
    driver_error_page.check_errors(allowed_error_pages=('403',))


@allowed_any_error_message
def test_check_error_messages(driver_error_msgs):
    with pytest.raises(ErrorMessagesException) as excinfo:
        driver_error_msgs.check_errors()


@allowed_any_error_message
def test_check_errors_expected_error_messages(driver_error_msgs):
    driver_error_msgs.check_errors(expected_error_messages=('some-error', 'another-error'))


@allowed_any_error_message
def test_check_errors_not_all_expected_error_messages(driver_error_msgs):
    with pytest.raises(ErrorMessagesException) as excinfo:
        driver_error_msgs.check_errors(expected_error_messages=('some-error',))


@allowed_any_error_message
def test_check_errors_allowed_error_messages(driver_error_msgs):
    driver_error_msgs.check_errors(allowed_error_messages=('some-error', 'another-error'))


@allowed_any_error_message
def test_check_errors_not_all_allowed_error_messages(driver_error_msgs):
    with pytest.raises(ErrorMessagesException) as excinfo:
        driver_error_msgs.check_errors(expected_error_messages=('some-error',))


@allowed_any_error_message
def test_check_errors_expected_and_allowed_error_messages(driver_error_msgs):
    driver_error_msgs.check_errors(expected_error_messages=('some-error',), allowed_error_messages=('another-error',))
