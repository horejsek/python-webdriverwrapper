# -*- coding: utf-8 -*-

#  In this test is not used TestCase's aliases, because it's not target of this
#+ test. There is testing mainly driver instance.
#  WebdriverTestCase is used because of creating of driver.

import os
from webdriverwrapper import unittest, Chrome


class WebdriverWrapperBaseClassTest(unittest.WebdriverTestCase):
    instances_of_driver = unittest.ONE_INSTANCE_PER_TESTCASE

    def init(self):
        self.path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

    def _get_driver(self):
        return Chrome()
