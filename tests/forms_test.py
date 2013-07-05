# -*- coding: utf-8 -*-

import os

from webdriverwrapper import testcase, Chrome
from webdriverwrapper.exceptions import NoSuchElementException


class FormTest(testcase.WebdriverTestCase):
    instances_of_driver = testcase.ONE_INSTANCE_PER_TESTCASE

    def _get_driver(self):
        return Chrome()

    def setUp(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.go_to('file://%s/html/form.html' % path)

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
        except NoSuchElementException, e:
            self.assertTrue(e.msg and 'nosuchelement' in e.msg, 'Bad msg: "%s"' % e.msg)

