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
        except NoSuchElementException, e:
            self.assertTrue(
                e.msg and 'some_non_exist_id' in e.msg and 'file://' in e.msg,
                'Exception has bad message (%s)' % e.msg,
            )
        except Exception, e:
            self.fail('Excepted NoSuchElementException, but raised %s instead' % e.__class__)
        else:
            self.fail('NoSuchElementException not raised')
