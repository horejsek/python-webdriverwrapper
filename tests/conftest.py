# -*- coding: utf-8 -*-

import os
import sys

TEST_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(TEST_PATH, '..'))


import pytest
from pyvirtualdisplay import Display

import webdriverwrapper
from webdriverwrapper.pytest import *


@pytest.yield_fixture(scope='session', autouse=True)
def display():
    d = Display(visible=0, size=(1280, 700))
    d.start()
    yield
    d.stop()


@pytest.fixture(scope='session')
def session_driver():
    opt = webdriverwrapper.ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--proxy-auto-detect')

    driver = webdriverwrapper.Chrome(chrome_options=opt)
    return driver


@pytest.fixture(scope='function')
def _driver(session_driver):
    session_driver.get('file://{}/html/some_page.html'.format(TEST_PATH))
    return session_driver


@pytest.fixture
def driver_form(driver):
    driver.get('file://{}/html/form.html'.format(TEST_PATH))
    return driver


@pytest.fixture
def driver_error_page(driver):
    driver.get('file://{}/html/error_page.html'.format(TEST_PATH))
    return driver


@pytest.fixture
def driver_error_msgs(driver):
    driver.get('file://{}/html/error_messages.html'.format(TEST_PATH))
    return driver


@pytest.fixture
def driver_info_msgs(driver):
    driver.get('file://{}/html/info_messages.html'.format(TEST_PATH))
    return driver


@pytest.fixture
def driver_windows(driver):
    driver.get('file://{}/html/windows.html'.format(TEST_PATH))
    return driver


@pytest.fixture
def new_window_path():
    return '{}/html/new_window.html'.format(TEST_PATH)
