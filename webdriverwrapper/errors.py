# -*- coding: utf-8 -*-

from functools import wraps
from selenium.common.exceptions import NoSuchElementException

__all__ = ('ShouldBeError',)


class ShouldBeErrorPage(object):
    """Decorator object for test method.

    If test method has this decorator, it must end with error page with error
    code passed in `expected_error_page`. It can raise some exception - exceptions
    are ignored. `expected_error_page` can be - 403, 404, "Not Found" etc.
    """
    def __init__(self, expected_error_page):
        self.expected_error_page = str(expected_error_page)

    def __call__(self, func):
        self.func = func
        return self.create_wrapper()

    def create_wrapper(self):
        self.func.__should_be_error_page__ = True
        @wraps(self.func)
        def f(self_of_wrapped_method):
            try:
                self.func(self_of_wrapped_method)
            except:
                pass
            finally:
                if not self.is_expected_error_page(self_of_wrapped_method.driver):
                    self_of_wrapped_method.fail('Expected error page "%s", but isn\'t.' % self.expected_error_page)
        return f

    def is_expected_error_page(self, driver):
        error_page = self.get_error_page(driver)
        return bool(error_page and self.expected_error_page in error_page)

    def get_error_page(self, driver):
        return get_error_page(driver)


def get_error_page(driver):
    try:
        error_page = driver.get_elm(class_name='error-page')
    except NoSuchElementException:
        pass
    else:
        header = error_page.get_elm(tag_name='h1')
        return header.text


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


class CanBeError(ShouldBeError):
    """Same as ShouldBeError, but no error is OK."""
    def is_expected_error(self, driver):
        errors = self.get_errors(driver)
        if not errors:
            return True
        return super(CanBeError, self).is_expected_error(driver)


def get_error_messages(driver):
    try:
        error_elms = driver.get_elms(class_name='error')
    except NoSuchElementException:
        return []
    else:
        try:
            error_values = [error_elm.get_attribute('error') for error_elm in error_elms]
        except Exception:
            error_values = [error_elm.text for error_elm in error_elms]
        finally:
            return error_values
