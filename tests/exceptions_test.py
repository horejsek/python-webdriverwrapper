# -*- coding: utf-8 -*-

from mock import Mock, call
import unittest

from webdriverwrapper.exceptions import NoSuchElementException


class NoSuchElementExceptionTest(unittest.TestCase):
    def test_make_msg_id(self):
        msg = NoSuchElementException._create_text_elm(id_='id')
        self.assertEquals(msg, '<* id=id>')

    def test_make_msg_class_name(self):
        msg = NoSuchElementException._create_text_elm(class_name='class')
        self.assertEquals(msg, '<* class=class>')

    def test_make_msg_tag_name(self):
        msg = NoSuchElementException._create_text_elm(tag_name='div')
        self.assertEquals(msg, '<div>')

    def test_make_msg_all(self):
        msg = NoSuchElementException._create_text_elm(tag_name='div', id_='id', class_name='class')
        self.assertEquals(msg, '<div id=id class=class>')

    def test_make_msg_xpath(self):
        msg = NoSuchElementException._create_text_elm(xpath='//*')
        self.assertEquals(msg, '//*')
