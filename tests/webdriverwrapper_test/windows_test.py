# -*- coding: utf-8 -*-

from webdriverwrapper_test import WebdriverWrapperBaseClassTest
from webdriverwrapper.exceptions import NoSuchWindowException


class WindowsTest(WebdriverWrapperBaseClassTest):
    def setUp(self):
        self.go_to('file://%s/html/windows.html' % self.path)
        self.new_window_path = 'file://%s/html/new_window.html' % self.path
        self.close_other_windows()

    def test_switch_to_window_by_title(self):
        self._test_swith_to_window(lambda: self.switch_to_window(title='New window'))

    def test_switch_to_window_by_url(self):
        self._test_swith_to_window(lambda: self.switch_to_window(url=self.new_window_path))

    def test_switch_to_window_by_url_args(self):
        try:
            self._test_swith_to_window(lambda: self.switch_to_window(url={'path': 'aa', 'domain': 'example.com'}))
        except NoSuchWindowException, e:
            self.assertTrue('http://example.com/aa' in e.msg)
        except Exception, e:
            self.fail('Wrong exception: %s' % str(e))
        else:
            self.fail('Window should be not found!')

    def _test_swith_to_window(self, callback):
        main_window_handle = self.driver.current_window_handle
        self.assertEqual(len(self.driver.window_handles), 1)
        self.click('link')
        self.assertEqual(len(self.driver.window_handles), 2)
        self.assertEqual(self.driver.current_window_handle, main_window_handle)
        callback()
        self.assertNotEqual(self.driver.current_window_handle, main_window_handle)

    def test_close_window_by_title(self):
        self._test_close_window(lambda: self.close_window(title='New window'))

    def test_close_window_by_url(self):
        self._test_close_window(lambda: self.close_window(url=self.new_window_path))

    def _test_close_window(self, callback):
        main_window_handle = self.driver.current_window_handle
        self.click('link')
        self.assertEqual(len(self.driver.window_handles), 2)
        callback()
        self.assertEqual(len(self.driver.window_handles), 1)
        self.assertEqual(self.driver.current_window_handle, main_window_handle)

    def test_close_other_widnows(self):
        main_window_handle = self.driver.current_window_handle
        self.assertEqual(len(self.driver.window_handles), 1)
        self.click('link')
        self.assertEqual(len(self.driver.window_handles), 2)
        self.click('link')
        self.assertEqual(len(self.driver.window_handles), 3)
        self.close_other_windows()
        self.assertEqual(len(self.driver.window_handles), 1)
        self.assertEqual(self.driver.current_window_handle, main_window_handle)
