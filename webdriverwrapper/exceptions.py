# -*- coding: utf-8 -*-

__all__ = ('WebdriverWrapperException', 'ErrorsException', 'JSErrorsException')


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
