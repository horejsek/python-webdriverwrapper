# -*- coding: utf-8 -*-

import os

from webdriverwrapper import unittest, Chrome
from webdriverwrapper.exceptions import NoSuchElementException


class FormTest(unittest.WebdriverTestCase):
    instances_of_driver = unittest.ONE_INSTANCE_PER_TESTCASE

    def _get_driver(self):
        return Chrome()

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.driver.get('file://%s/html/form.html' % path)

    def test_ok(self):
        self.get_elm('form').fill_out({
            'text': 'text',
            'textarea': 'text',
            'checkbox_1': True,
            'checkbox_2': False,
            'radio': 'value1',
            'select': 'value1',
            'multiselect': ['value1', 'value2'],
        })

    def test_nosuchelement(self):
        try:
            self.get_elm('form').fill_out({
                'nosuchelement': 'text',
            })
        except NoSuchElementException as exc:
            self.assertTrue(exc.msg and 'nosuchelement' in exc.msg, 'Bad msg: "%s"' % exc.msg)

    def test_hidden_checkbox(self):
        chbox = self.get_elm(name='hidden_checkbox_inside_label')
        self.assertFalse(chbox.is_selected())
        self.get_elm('form').fill_out({
            'hidden_checkbox_inside_label': True,
        })
        self.assertTrue(chbox.is_selected())

    def test_str(self):
        self.get_elm('form').fill_out({
            'text': 'ěřžčřž',
        })

    def test_unicode(self):
        self.get_elm('form').fill_out({
            'text': u'ěřžčřž',
        })
