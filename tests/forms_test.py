# -*- coding: utf-8 -*-

from mock import Mock, call
import os

from webdriverwrapper import testcase, Chrome


class FormTest(testcase.WebdriverTestCase):
    instances_of_driver = testcase.ONE_INSTANCE_PER_TESTCASE

    def _get_driver(self):
        return Chrome()

    def test(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.go_to('file://%s/html/form.html' % path)

        self.get_elm('form').fill_out({
            'text': 'text',
            'textarea': 'text',
            'checkbox_1': True,
            'checkbox_2': False,
            'radio': 'value1',
            'select': 'value1',
            'multiselect': ['value1', 'value2'],
        })
