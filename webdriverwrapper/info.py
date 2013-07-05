# -*- coding: utf-8 -*-

from functools import wraps
from selenium.common.exceptions import NoSuchElementException

__all__ = ('ShouldBeInfo',)


class ShouldBeInfo(object):
    """Decorator object for test method.
    If test method has this decorator, it must end with info message passed in
    `expected_info`."""
    def __init__(self, expected_info=None):
        self.expected_info = expected_info

    def __call__(self, func):
        self.func = func
        return self.create_wrapper()

    def create_wrapper(self):
        self.func.__should_be_info__ = True
        @wraps(self.func)
        def f(self_of_wrapped_method):
            self.func(self_of_wrapped_method)

            driver = self_of_wrapped_method.driver
            if not self.is_expected_info(driver):
                self_of_wrapped_method.fail('"%s" info expected, but found %s.' % (
                    self.expected_info or '*',
                    self.get_infos(driver),
                ))
        return f

    def is_expected_info(self, driver):
        infos = self.get_infos(driver)
        if self.expected_info is None:
            return bool(infos)
        return self.expected_info in infos

    def get_infos(self, driver):
        return get_info_messages(driver)


def get_info_messages(driver):
    try:
        info_elms = driver.get_elms(class_name='info')
    except NoSuchElementException:
        return []
    else:
        try:
            info_values = [info_elm.get_attribute('info') for info_elm in info_elms]
        except Exception:
            info_values = [info_elm.text for error_elm in info_elms]
        finally:
            return info_values
