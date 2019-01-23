from selenium.common.exceptions import NoSuchElementException

from .exceptions import ErrorPageException, ErrorMessagesException, JSErrorsException

__all__ = (
    'expected_error_page',
    'allowed_error_pages',
    'expected_error_messages',
    'allowed_error_messages',
    'allowed_any_error_message',
)

EXPECTED_ERROR_PAGE = '__expected_error_page__'
ALLOWED_ERROR_PAGES = '__allowed_error_pages__'
EXPECTED_ERROR_MESSAGES = '__expected_error_messages__'
ALLOWED_ERROR_MESSAGES = '__allowed_error_messages__'


def expected_error_page(error_page):
    """
    Decorator expecting defined error page at the end of test method. As param
    use what :py:meth:`~.WebdriverWrapperErrorMixin.get_error_page`
    returns.

    .. versionadded:: 2.0
        Before this decorator was called ``ShouldBeErrorPage``.
    """
    def wrapper(func):
        setattr(func, EXPECTED_ERROR_PAGE, error_page)
        return func
    return wrapper


def allowed_error_pages(*error_pages):
    """
    Decorator ignoring defined error pages at the end of test method. As param
    use what :py:meth:`~.WebdriverWrapperErrorMixin.get_error_page`
    returns.

    .. versionadded:: 2.0
    """
    def wrapper(func):
        setattr(func, ALLOWED_ERROR_PAGES, error_pages)
        return func
    return wrapper


def expected_error_messages(*error_messages):
    """
    Decorator expecting defined error messages at the end of test method. As
    param use what
    :py:meth:`~.WebdriverWrapperErrorMixin.get_error_messages`
    returns.

    .. versionadded:: 2.0
        Before this decorator was called ``ShouldBeError``.
    """
    def wrapper(func):
        setattr(func, EXPECTED_ERROR_MESSAGES, error_messages)
        return func
    return wrapper


def allowed_error_messages(*error_messages):
    """
    Decorator ignoring defined error messages at the end of test method. As
    param use what
    :py:meth:`~.WebdriverWrapperErrorMixin.get_error_messages`
    returns.

    .. versionadded:: 2.0
        Before this decorator was called ``CanBeError``.
    """
    def wrapper(func):
        setattr(func, ALLOWED_ERROR_MESSAGES, error_messages)
        return func
    return wrapper


def allowed_any_error_message(func):
    """
    Decorator ignoring any error messages at the end of test method. If you want
    allow only specific error message, use :py:func:`.allowed_error_messages`
    instead.

    .. versionadded:: 2.0
    """
    setattr(func, ALLOWED_ERROR_MESSAGES, ANY)
    return func


class ANY:
    pass


class WebdriverWrapperErrorMixin:
    """
    Mixin used in :py:obj:`~webdriverwrapper.wrapper._WebdriverWrapper`.

    .. versionadded:: 2.0
        Before you had to change decorators ``ShouldByError``, ``CanBeError``
        and ``ShouldBeErrorPage`` which are gone. Now you can use original
        decorators and just change one of these methods. For more information
        check out section testing.
    """

    def check_expected_errors(self, test_method):
        """
        This method is called after each test. It will read decorated
        informations and check if there are expected errors.

        You can set expected errors by decorators :py:func:`.expected_error_page`,
        :py:func:`.allowed_error_pages`, :py:func:`.expected_error_messages`,
        :py:func:`.allowed_error_messages` and :py:func:`.allowed_any_error_message`.
        """
        f = lambda key, default=[]: getattr(test_method, key, default)
        expected_error_page = f(EXPECTED_ERROR_PAGE, default=None)
        allowed_error_pages = f(ALLOWED_ERROR_PAGES)
        expected_error_messages = f(EXPECTED_ERROR_MESSAGES)
        allowed_error_messages = f(ALLOWED_ERROR_MESSAGES)
        self.check_errors(
            expected_error_page,
            allowed_error_pages,
            expected_error_messages,
            allowed_error_messages,
        )

    def check_errors(self, expected_error_page=None, allowed_error_pages=[], expected_error_messages=[], allowed_error_messages=[]):
        """
        This method should be called whenever you need to check if there is some
        error. Normally you need only ``check_expected_errors`` called after each
        test (which you specify only once), but it will check errors only at the
        end of test. When you have big use case and you need to be sure that on
        every step is not any error, use this.

        To parameters you should pass same values like to decorators
        :py:func:`.expected_error_page`, :py:func:`.allowed_error_pages`,
        :py:func:`.expected_error_messages` and :py:func:`.allowed_error_messages`.
        """
        # Close unexpected alerts (it's blocking).
        self.close_alert(ignore_exception=True)

        expected_error_pages = set([expected_error_page]) if expected_error_page else set()
        allowed_error_pages = set(allowed_error_pages)
        error_page = self.get_error_page()
        error_pages = set([error_page]) if error_page else set()
        if (
                error_pages & expected_error_pages != expected_error_pages
                or
                error_pages - (expected_error_pages | allowed_error_pages)
        ):
            traceback = self.get_error_traceback()
            raise ErrorPageException(self.current_url, error_page, expected_error_page, allowed_error_pages, traceback)

        error_messages = set(self.get_error_messages())
        expected_error_messages = set(expected_error_messages)
        allowed_error_messages = error_messages if allowed_error_messages is ANY else set(allowed_error_messages)
        if (
                error_messages & expected_error_messages != expected_error_messages
                or
                error_messages - (expected_error_messages | allowed_error_messages)
        ):
            raise ErrorMessagesException(self.current_url, error_messages, expected_error_messages, allowed_error_messages)

        js_errors = self.get_js_errors()
        if js_errors:
            raise JSErrorsException(self.current_url, js_errors)

    def get_error_page(self):
        """
        Method returning error page. Should return string.

        By default it find element with class ``error-page`` and returns text
        of ``h1`` header. You can change this method accordingly to your app.

        Error page returned from this method is used in decorators
        :py:func:`.expected_error_page` and :py:func:`.allowed_error_pages`.
        """
        try:
            error_page = self.get_elm(class_name='error-page')
        except NoSuchElementException:
            pass
        else:
            header = error_page.get_elm(tag_name='h1')
            return header.text

    def get_error_traceback(self):
        """
        Method returning traceback of error page.

        By default it find element with class ``error-page`` and returns text
        of element with class ``traceback``. You can change this method
        accordingly to your app.
        """
        try:
            error_page = self.get_elm(class_name='error-page')
            traceback = error_page.get_elm(class_name='traceback')
        except NoSuchElementException:
            pass
        else:
            return traceback.text

    def get_error_messages(self):
        """
        Method returning error messages. Should return list of messages.

        By default it find element with class ``error`` and theirs value in
        attribute ``error`` or text if that attribute is missing. You can change
        this method accordingly to your app.

        Error messages returned from this method are used in decorators
        :py:func:`.expected_error_messages` and :py:func:`.allowed_error_messages`.
        """
        try:
            error_elms = self.get_elms(class_name='error')
        except NoSuchElementException:
            return []
        else:
            try:
                error_values = [error_elm.get_attribute('error') for error_elm in error_elms]
            except Exception:
                error_values = [error_elm.text for error_elm in error_elms]
            finally:
                return error_values

    def get_js_errors(self):
        """
        Method returning JS errors. Should return list of errors.

        You have to include following JS snippet to your web app which will
        record all JS errors and this method will automatically read them.

        .. code-block:: html

            <script type="text/javascript">
                window.jsErrors = [];
                window.onerror = function(errorMessage) {
                    window.jsErrors[window.jsErrors.length] = errorMessage;
                }
            </script>
        """
        return self.execute_script('return window.jsErrors')
