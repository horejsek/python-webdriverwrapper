# -*- coding: utf-8 -*-

from selenium.common.exceptions import *


class WebdriverWrapperException(Exception):
    def __init__(self, msg='', traceback=''):
        self.msg = msg
        self.traceback = traceback

    def __str__(self):
        if not self.traceback:
            return self._to_string(self.msg)
        return '%s\n\nTraceback:\n%s' % (
            self._to_string(self.msg),
            self._to_string(self.traceback),
        )

    def __repr__(self):
        return self.__str__()

    def _to_string(self, msg):
        return msg.encode('utf-8') if isinstance(msg, unicode) else str(msg)


class ErrorPageException(WebdriverWrapperException):
    def __init__(self, url, error_page, traceback=''):
        msg = 'Page %s has unexpected error page: %s' % (url, error_page)
        super(ErrorPageException, self).__init__(msg, traceback)


class ErrorsException(WebdriverWrapperException):
    def __init__(self, url, errors=[]):
        msg = 'Page %s has these unexpected errors: %s' % (url, errors)
        super(ErrorsException, self).__init__(msg)


class JSErrorsException(WebdriverWrapperException):
    def __init__(self, url, errors=[]):
        msg = 'Page %s has these unexpected JavaScript errors: %s' % (url, errors)
        super(JSErrorsException, self).__init__(msg)


def _create_exception_msg(
    id_=None, class_name=None, name=None, tag_name=None, xpath=None,
    parent_id=None, parent_class_name=None, parent_name=None, parent_tag_name=None,
    url=None, css_selector=None
):
    elm_text = _create_exception_msg_tag(id_, class_name, name, tag_name, xpath, css_selector)
    parent_text = _create_exception_msg_tag(parent_id, parent_class_name, parent_name, parent_tag_name)

    msg = 'No element %s found' % elm_text
    if parent_text:
        msg += ' in parent element %s' % parent_text
    if url:
        msg += ' at %s' % url
    return msg


def _create_exception_msg_tag(id_=None, class_name=None, name=None, tag_name=None, xpath=None, css_selector=None):
    if xpath:
        return xpath
    elif css_selector:
        return css_selector
    elif id_ or class_name or tag_name or name:
        msg = '<%s' % (tag_name or '*')
        if id_:
            msg += ' id=%s' % id_
        if class_name:
            msg += ' class=%s' % class_name
        if name:
            msg += ' name=%s' % name
        msg += '>'
        return msg
    return ''
