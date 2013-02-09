# -*- coding: utf-8 -*-

from functools import wraps

from selenium.common.exceptions import NoSuchElementException

__all__ = ('ShouldBeError',)


class ShouldBeError(object):
    """Decorator object for test method.
    If test method has this decorator, it must end with error message passed in
    `expected_error`."""
    def __init__(self, expected_error=None):
        self.expected_error = expected_error

    def __call__(self, func):
        self.func = func
        return self.create_wrapper()

    def create_wrapper(self):
        self.func.__should_be_error__ = True
        @wraps(self.func)
        def f(self_of_wrapped_method):
            self.func(self_of_wrapped_method)

            driver = self_of_wrapped_method.driver
            if not self.is_expected_error(driver):
                self_of_wrapped_method.fail('"%s" error expected, but found %s.' % (
                    self.expected_error or '*',
                    self.get_errors(driver),
                ))
        return f

    def is_expected_error(self, driver):
        errors = self.get_errors(driver)
        if self.expected_error is None:
            return bool(errors)
        return self.expected_error in errors

    def get_errors(self, driver):
        return get_error_messages(driver)


def get_error_messages(driver):
    try:
        error_elms = driver.get_elms(class_name='error')
    except NoSuchElementException:
        return []
    else:
        try:
            error_values = [error_elm.get_attribute('error') for error_elm in error_elms]
        except:
            error_values = [error_elm.text for error_elm in error_elms]
        finally:
            return error_values
