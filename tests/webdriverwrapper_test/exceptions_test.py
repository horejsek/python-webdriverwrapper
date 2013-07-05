# -*- coding: utf-8 -*-

from webdriverwrapper.exceptions import NoSuchElementException

from webdriverwrapper_test import WebdriverWrapperBaseClassTest


class WebdriverExceptionsTest(WebdriverWrapperBaseClassTest):
    def setUp(self):
        self.go_to('file://%s/html/some_page.html' % self.path)

    def test_exception(self):
        self._test_exception(lambda: self.driver.get_elm('some_non_exist_id'))

    def test_exception_from_find_methods(self):
        self._test_exception(lambda: self.driver.find_element_by_id('some_non_exist_id'))

    def _test_exception(self, callback):
        try:
            callback()
        except NoSuchElementException as exc:
            self.assertTrue(
                exc.msg and 'some_non_exist_id' in exc.msg and 'file://' in exc.msg,
                'Exception has bad message (%s)' % exc.msg,
            )
        except Exception as exc:
            self.fail('Excepted NoSuchElementException, but raised %s instead' % exc.__class__)
        else:
            self.fail('NoSuchElementException not raised')
