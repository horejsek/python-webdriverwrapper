# -*- coding: utf-8 -*-

import pytest

from webdriverwrapper.decorators import (
    expected_error_page, allowed_error_pages,
    expected_error_messages, allowed_error_messages, allowed_any_error_message,
    expected_info_messages, allowed_info_messages,
)


@pytest.fixture
def func():
    def dynamic_func():
        pass
    return dynamic_func


def test_expected_error_page(func):
    value = 'error_page'
    assert not hasattr(func, '__expected_error_page__')
    assert expected_error_page(value)(func) is func
    assert func.__expected_error_page__ == value


def test_allowed_error_pages(func):
    value = ('error_page1', 'error_page2')
    assert not hasattr(func, '__allowed_error_pages__')
    assert allowed_error_pages(*value)(func) is func
    assert func.__allowed_error_pages__ == value


def test_expected_error_messages(func):
    value = ('error_msg1', 'error_msg2')
    assert not hasattr(func, '__expected_error_messages__')
    assert expected_error_messages(*value)(func) is func
    assert func.__expected_error_messages__ == value


def test_allowed_error_messages(func):
    value = ('error_msg1', 'error_msg2')
    assert not hasattr(func, '__allowed_error_messages__')
    assert allowed_error_messages(*value)(func) is func
    assert func.__allowed_error_messages__ == value


def test_allowed_any_error_message(func):
    assert not hasattr(func, '__allowed_error_messages__')
    assert allowed_any_error_message(func) is func
    assert func.__allowed_error_messages__.__name__ == 'ANY'


def test_expected_info_messages(func):
    value = ('info_msg1', 'info_msg2')
    assert not hasattr(func, '__expected_info_messages__')
    assert expected_info_messages(*value)(func) is func
    assert func.__expected_info_messages__ == value


def test_allowed_info_messages(func):
    value = ('info_msg1', 'info_msg2')
    assert not hasattr(func, '__allowed_info_messages__')
    assert allowed_info_messages(*value)(func) is func
    assert func.__allowed_info_messages__ == value
