# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

__all__ = ('WebdriverWrapperException', 'ErrorsException', 'JSErrorsException')


class NoSuchElementException(NoSuchElementException):
    def __init__(self, id_=None, class_name=None, name=None, tag_name=None, xpath=None, parent_id=None, parent_class_name=None, parent_name=None, parent_tag_name=None):
        elm_text = self._create_text_elm(id_, class_name, name, tag_name, xpath)
        parent_text = self._create_text_elm(parent_id, parent_class_name, parent_name, parent_tag_name)

        msg = 'No element %s found' % elm_text
        if parent_text:
            msg += ' in parent element %s' % parent_text
        super(NoSuchElementException, self).__init__(msg)

    @classmethod
    def _create_text_elm(cls, id_=None, class_name=None, name=None, tag_name=None, xpath=None):
        if xpath:
            return xpath
        elif id_ or class_name or tag_name:
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


class ErrorsException(WebdriverWrapperException):
    def __init__(self, url, errors=[]):
        msg = 'Page %s has these unexpected errors: %s' % (url, errors)
        super(ErrorsException, self).__init__(msg)


class JSErrorsException(WebdriverWrapperException):
    def __init__(self, url, errors=[]):
        msg = 'Page %s has these unexpected JavaScript errors: %s' % (url, errors)
        super(JSErrorsException, self).__init__(msg)
