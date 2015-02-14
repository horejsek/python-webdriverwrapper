# -*- coding: utf-8 -*-

from selenium.common.exceptions import *


def _create_exception_msg(
    id_=None, class_name=None, name=None, tag_name=None,
    parent_id=None, parent_class_name=None, parent_name=None, parent_tag_name=None,
    xpath=None, css_selector=None, url=None,
):
    elm_text = _create_exception_msg_tag(
        id_, class_name, name, tag_name,
        parent_id, parent_class_name, parent_name, parent_tag_name,
        xpath, css_selector,
    )
    msg = 'No element {} found'.format(elm_text)
    if url:
        msg += ' at {}'.format(url)
    return msg


def _create_exception_msg_tag(
    id_=None, class_name=None, name=None, tag_name=None,
    parent_id=None, parent_class_name=None, parent_name=None, parent_tag_name=None,
    xpath=None, css_selector=None,
):
    elm_text = _create_exception_msg_tag_element(id_, class_name, name, tag_name, xpath, css_selector)
    parent_text = _create_exception_msg_tag_element(parent_id, parent_class_name, parent_name, parent_tag_name)

    if parent_text:
        return '{} in parent element {}'.format(elm_text, parent_text)
    return elm_text


def _create_exception_msg_tag_element(id_=None, class_name=None, name=None, tag_name=None, xpath=None, css_selector=None):
    if xpath:
        return xpath
    elif css_selector:
        return css_selector
    elif id_ or class_name or tag_name or name:
        msg = '<{}'.format(tag_name or '*')
        if id_:
            msg += ' id={}'.format(id_)
        if class_name:
            msg += ' class={}'.format(class_name)
        if name:
            msg += ' name={}'.format(name)
        msg += '>'
        return msg
    return ''


class WebdriverWrapperException(Exception):
    """
    Base exception of WebDriver Wrapper.
    """

    def __init__(self, url, msg):
        self.url = url
        self.msg = msg

    def __str__(self):
        return '{} [at {}]'.format(self.msg, self.url)

    def __repr__(self):
        return self.__str__()


class ErrorPageException(WebdriverWrapperException):
    """
    Exception raised when there is some unexpected error page. Like page 404,
    500 and so on.
    """

    def __init__(self, url, error_page, expected_error_page, allowed_error_pages, traceback=None):
        if expected_error_page:
            msg = 'Expected error page "{}", but found "{}" instead.'.format(expected_error_page, error_page)
        else:
            msg = 'Unexpected error page "{}".'.format(error_page)
        if allowed_error_pages:
            msg += ' Allowed error pages: "{}"'.format(allowed_error_pages)
        if traceback:
            msg += '\n\nTraceback:\n{}'.format(traceback)
        super(ErrorPageException, self).__init__(url, msg)


class ErrorMessagesException(WebdriverWrapperException):
    """
    Exception raised when there is some unexpected error message. Like "some
    field is mandatory", "wrong e-mail" and so on.
    """

    def __init__(self, url, error_messages, expected_error_messages, allowed_error_messages):
        if expected_error_messages:
            msg = 'Expected error messages "{}", but found "{}" instead.'.format(expected_error_messages, error_messages)
        else:
            msg = 'Unexpected error messages "{}".'.format(error_messages)
        if allowed_error_messages:
            msg += ' Allowed error messages: "{}"'.format(allowed_error_messages)
        super(ErrorMessagesException, self).__init__(url, msg)


class JSErrorsException(WebdriverWrapperException):
    """
    Exception raised when there is some JS error.

    See :py:meth:`get_js_errors <webdriverwrapper.errors.WebdriverWrapperErrorMixin.get_js_errors>`
    for more information.
    """

    def __init__(self, url, js_errors):
        msg = 'Unexpected JavaScript errors "{}".'.format(js_errors)
        super(JSErrorsException, self).__init__(url, msg)


class InfoMessagesException(WebdriverWrapperException):
    """
    Exception raised when there is missing some expected info message. Like
    "sucessfully saved" and so on.
    """

    def __init__(self, url, info_messages, expected_info_messages, allowed_info_messages):
        msg = 'Expected info messages "{}", but found "{}" instead.'.format(expected_info_messages, info_messages)
        if allowed_info_messages:
            msg += ' Allowed info messages: "{}"'.format(allowed_info_messages)
        super(InfoMessagesException, self).__init__(url, msg)
