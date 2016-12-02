# -*- coding: utf-8 -*-


def test_switch_to_window_by_title(driver_windows):
    _test_switch_to_window(driver_windows, lambda: driver_windows.switch_to_window(title='New window'))


def test_switch_to_window_by_url(driver_windows, new_window_path):
    _test_switch_to_window(driver_windows, lambda: driver_windows.switch_to_window(url=new_window_path))


def _test_switch_to_window(driver, callback):
    main_window_handle = driver.current_window_handle
    assert len(driver.window_handles) == 1
    driver.click('link')
    assert len(driver.window_handles) == 2
    assert driver.current_window_handle == main_window_handle
    callback()
    assert driver.current_window_handle != main_window_handle


def test_close_window_by_title(driver_windows):
    _test_close_window(driver_windows, lambda: driver_windows.close_window(title='New window'))


def test_close_window_by_url(driver_windows, new_window_path):
    _test_close_window(driver_windows, lambda: driver_windows.close_window(url=new_window_path))


def _test_close_window(driver, callback):
    main_window_handle = driver.current_window_handle
    driver.click('link')
    assert len(driver.window_handles) == 2
    callback()
    assert len(driver.window_handles) == 1
    assert driver.current_window_handle == main_window_handle


def test_close_other_windows(driver_windows):
    main_window_handle = driver_windows.current_window_handle
    driver_windows.click('link')
    driver_windows.click('link')
    assert len(driver_windows.window_handles) == 3
    driver_windows.close_other_windows()
    assert len(driver_windows.window_handles) == 1
    assert driver_windows.current_window_handle == main_window_handle
