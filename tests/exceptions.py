# -*- coding: utf-8 -*-

import pytest

from webdriverwrapper.exceptions import (
    _create_exception_msg,
    _create_exception_msg_tag_element,
    _find_best_suggestion,
    NoSuchElementException,
)


def test_make_msg_id():
    assert '<* id=id>' == _create_exception_msg_tag_element(id_='id')


def test_make_msg_class_name():
    assert '<* class=class>' == _create_exception_msg_tag_element(class_name='class')


def test_make_msg_tag_name():
    assert '<div>' == _create_exception_msg_tag_element(tag_name='div')


def test_make_msg_name():
    assert '<* name=xx>' == _create_exception_msg_tag_element(name='xx')


def test_make_msg_combined():
    assert '<div id=id name=xx>' == _create_exception_msg_tag_element(tag_name='div', id_='id', name='xx')


def test_make_msg_xpath():
    assert '//*' == _create_exception_msg_tag_element(xpath='//*')


def test_make_msg_css_selector():
    assert 'div.class' == _create_exception_msg_tag_element(css_selector='div.class')


def test_make_msg_with_url():
    assert 'No element <* id=id> found at http://example.com' == _create_exception_msg(id_='id', url='http://example.com')


def test_raises_exception_with_msg(driver):
    with pytest.raises(NoSuchElementException) as excinfo:
        driver.get_elm('some_non_exists_id')
    assert 'some_non_exists_id' in str(excinfo.value)


def test_raises_exception_with_msg_origin_find_methods(driver):
    with pytest.raises(NoSuchElementException) as excinfo:
        driver.find_element_by_id('some_non_exists_id')
    assert 'some_non_exists_id' in str(excinfo.value)


def test_suggestions(driver):
    with pytest.raises(NoSuchElementException) as excinfo:
        driver.find_element_by_id('some_non_exists_id')
    assert 'did you mean id=somepage?' in str(excinfo.value)


def test_find_best_suggestions():
    suggestion = _find_best_suggestion('idx', ['id', 'anotherid', 'someid'])
    assert suggestion == 'id'
