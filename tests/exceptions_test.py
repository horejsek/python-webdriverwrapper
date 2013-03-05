# -*- coding: utf-8 -*-

from mock import Mock, call
import unittest

from webdriverwrapper.exceptions import _create_exception_msg, _create_exception_msg_tag


class CreateElmTextTagTest(unittest.TestCase):
    def test_make_msg_id(self):
        msg = _create_exception_msg_tag(id_='id')
        self.assertEquals(msg, '<* id=id>')

    def test_make_msg_class_name(self):
        msg = _create_exception_msg_tag(class_name='class')
        self.assertEquals(msg, '<* class=class>')

    def test_make_msg_tag_name(self):
        msg = _create_exception_msg_tag(tag_name='div')
        self.assertEquals(msg, '<div>')

    def test_make_msg_all(self):
        msg = _create_exception_msg_tag(tag_name='div', id_='id', class_name='class')
        self.assertEquals(msg, '<div id=id class=class>')

    def test_make_msg_xpath(self):
        msg = _create_exception_msg_tag(xpath='//*')
        self.assertEquals(msg, '//*')


class CreateElmTextTest(unittest.TestCase):
    def test_make_msg_with_url(self):
        msg = _create_exception_msg(id_='id', url='http://example.com')
        self.assertEquals(msg, 'No element <* id=id> found at http://example.com')
