# -*- coding: utf-8 -*-

from webdriverwrapper_test import WebdriverWrapperBaseClassTest


class ContainsTextTest(WebdriverWrapperBaseClassTest):
    def setUp(self):
        self.go_to('file://%s/html/find_elements.html' % self.path)

    def test_selenium_not_search(self):
        #  Check that text there is only one element - other elements are ignored
        #+ by attribute data-selenium-not-search.
        elms = self.find_elements_by_text('text')
        self.assertEqual(len(elms), 1)

    def test_find_by_integer(self):
        elms = self.find_elements_by_text(42)
        self.assertEqual(len(elms), 1)

    def test_not_unicode(self):
        elms = self.find_elements_by_text('ěščřž')
        self.assertEqual(len(elms), 1)

    def test_unicode(self):
        # six.u is safe only with ASCII, so I need some hack.
        text = 'ěščřž'
        if hasattr(text, 'decode'):
            text = text.decode('utf8')

        elms = self.find_elements_by_text(text)
        self.assertEqual(len(elms), 1)
