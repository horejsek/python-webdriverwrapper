# -*- coding: utf-8 -*-

import pytest

from webdriverwrapper.exceptions import NoSuchElementException


def test_fill_out(driver_form):
    driver_form.get_elm('form').fill_out({
        'text': 'text',
        'textarea': 'text',
        'checkbox_1': True,
        'checkbox_2': False,
        'radio': 'value1',
        'select': 'value1',
        'multiselect': ['value1', 'value2'],
    })


def test_nosuchelement(driver_form):
    with pytest.raises(NoSuchElementException) as excinfo:
        driver_form.get_elm('form').fill_out({
            'nosuchelement': 'text',
        })
    assert 'nosuchelement' in excinfo.value.msg


def test_hidden_checkbox(driver_form):
    chbox = driver_form.get_elm(name='hidden_checkbox_inside_label')
    assert not chbox.is_selected()
    driver_form.get_elm('form').fill_out({
        'hidden_checkbox_inside_label': True,
    })
    assert chbox.is_selected()


def test_str(driver_form):
    driver_form.get_elm('form').fill_out({
        'text': 'ěřžčřž',
    })


def test_unicode(driver_form):
    driver_form.get_elm('form').fill_out({
        'text': u'ěřžčřž',
    })
