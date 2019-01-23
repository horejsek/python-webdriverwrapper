from selenium.common.exceptions import NoSuchElementException

from .exceptions import InfoMessagesException

__all__ = ('expected_info_messages', 'allowed_info_messages')

EXPECTED_INFO_MESSAGES = '__expected_info_messages__'
ALLOWED_INFO_MESSAGES = '__allowed_info_messages__'


def expected_info_messages(*info_messages):
    """
    Decorator expecting defined info messages at the end of test method. As
    param use what
    :py:meth:`~.WebdriverWrapperInfoMixin.get_info_messages`
    returns.

    .. versionadded:: 2.0
        Before this decorator was called ``ShouldBeInfo``.
    """
    def wrapper(func):
        setattr(func, EXPECTED_INFO_MESSAGES, info_messages)
        return func
    return wrapper


def allowed_info_messages(*info_messages):
    """
    Decorator ignoring defined info messages at the end of test method. As
    param use what
    :py:meth:`~.WebdriverWrapperInfoMixin.get_info_messages`
    returns.

    .. versionadded:: 2.0
    """
    def wrapper(func):
        setattr(func, ALLOWED_INFO_MESSAGES, info_messages)
        return func
    return wrapper


class WebdriverWrapperInfoMixin:
    """
    Mixin used in :py:obj:`~webdriverwrapper.wrapper._WebdriverWrapper`.

    .. versionadded:: 2.0
        Before you had to change decorator ``ShouldBeInfo`` which is gone. Now
        you can use original decorators and just change one of these methods.
        For more information check out section testing.
    """

    def check_expected_infos(self, test_method):
        """
        This method is called after each test. It will read decorated
        informations and check if there are expected infos.

        You can set expected infos by decorators :py:func:`.expected_info_messages`
        and :py:func:`.allowed_info_messages`.
        """
        f = lambda key, default=[]: getattr(test_method, key, default)
        expected_info_messages = f(EXPECTED_INFO_MESSAGES)
        allowed_info_messages = f(ALLOWED_INFO_MESSAGES)
        self.check_infos(expected_info_messages, allowed_info_messages)

    def check_infos(self, expected_info_messages=[], allowed_info_messages=[]):
        """
        This method should be called whenever you need to check if there is some
        info. Normally you need only ``check_expected_infos`` called after each
        test (which you specify only once), but it will check infos only at the
        end of test. When you have big use case and you need to check messages
        on every step, use this.

        To parameters you should pass same values like to decorators
        :py:func:`.expected_info_messages` and :py:func:`.allowed_info_messages`.
        """
        # Close unexpected alerts (it's blocking).
        self.close_alert(ignore_exception=True)

        expected_info_messages = set(expected_info_messages)
        allowed_info_messages = set(allowed_info_messages)
        info_messages = set(self.get_info_messages())
        if (
                info_messages & expected_info_messages != expected_info_messages
                or
                (expected_info_messages and info_messages - (expected_info_messages | allowed_info_messages))
        ):
            raise InfoMessagesException(self.current_url, info_messages, expected_info_messages, allowed_info_messages)

    def get_info_messages(self):
        """
        Method returning info messages. Should return list of messages.

        By default it find element with class ``info`` and theirs value in
        attribute ``info`` or text if that attribute is missing. You can change
        this method accordingly to your app.

        Info messages returned from this method are used in decorators
        :py:func:`.expected_info_messages` and :py:func:`.allowed_info_messages`.
        """
        try:
            info_elms = self.get_elms(class_name='info')
        except NoSuchElementException:
            return []
        else:
            try:
                info_values = [info_elm.get_attribute('info') for info_elm in info_elms]
            except Exception:  # pylint: disable=broad-except
                info_values = [info_elm.text for info_elm in info_elms]
            finally:
                return info_values
