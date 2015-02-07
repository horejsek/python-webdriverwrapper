# -*- coding: utf-8 -*-

import pytest
from webdriverwrapper import Chrome
from webdriverwrapper.pytest import *


@pytest.fixture(scope='session')
def _driver():
    driver = Chrome()
    driver.get('http://www.google.com')
    return driver


def test_doodle(driver):
    driver.click('gbqfsb')
    assert driver.contains_text('Doodles')


def test_search(driver):
    driver.get_elm('gbqf').fill_out_and_submit({
        'q': 'hello',
    })
    driver.wait_for_element(id_='resultStats')
