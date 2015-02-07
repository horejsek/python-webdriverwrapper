# -*- coding: utf-8 -*-

import pytest

from webdriverwrapper.exceptions import InfoMessagesException


def test_check_info_messages(driver_info_msgs):
    with pytest.raises(InfoMessagesException) as excinfo:
        driver_info_msgs.check_infos(expected_info_messages=('some-info',))


def test_check_expected_info_messages(driver_info_msgs):
    driver_info_msgs.check_infos(expected_info_messages=('some-info', 'another-info'))


def test_check_allowed_info_messages(driver_info_msgs):
    driver_info_msgs.check_infos(allowed_info_messages=('some-info', 'another-info'))


def test_check_expected_and_allowed_info_messages(driver_info_msgs):
    driver_info_msgs.check_infos(expected_info_messages=('some-info',), allowed_info_messages=('another-info',))
