WebDriver Wrapper documentation
###############################

What is WebDriver Wrapper? Better interface of WebDriver in Python. WebDriver
is great for testing whole web apps, but it's pain using available API. This
wrapper wraps it and handle following for you:

* Adds messages into WebDriver's exceptions. By default there is no information
  about which element is missing and where and so on.
* Adds usefull method to :py:class:`selenium.WebDriver <selenium.webdriver.remote.webdriver.WebDriver>`
  and :py:class:`selenium.WebElement <selenium.webdriver.remote.webelement.WebElement>` such as

  * :py:meth:`find_elements_by_text <webdriverwrapper.wrapper._WebdriverBaseWrapper.find_elements_by_text>`,
  * :py:meth:`contains_text <webdriverwrapper.wrapper._WebdriverBaseWrapper.contains_text>`,
  * :py:meth:`wait_for_element <webdriverwrapper.wrapper._WebdriverWrapper.wait_for_element>`,
  * :py:meth:`go_to <webdriverwrapper.wrapper._WebdriverWrapper.go_to>`,
  * :py:meth:`download_file <webdriverwrapper.wrapper._WebElementWrapper.download_file>`
  * and more.

* Simplifys filling out of forms.

  * There is method :py:meth:`fill_out <webdriverwrapper.forms.Form.fill_out>` when
    ``WebElement`` is ``form`` to which you can pass Pythonic data.
  * ``WebElement`` is automatically instance of
    :py:obj:`Select <selenium.webdriver.support.select.Select>` if it is ``select``.

* Provide :py:obj:`TestCase <webdriverwrapper.unittest.WebdriverTestCase>` for unittesting.
* Provide pytest fixtures for testing with pytest.

Installation
************

.. code-block:: bash

    pip install webdriverwrapper

If you want also suggestions, then also install extra requirements:

.. code-block:: bash

    pip install webdriverwrapper[seggestions]

Then you will see something like this:

.. code-block:: python

    driver.get_elm('qbdfq')
    NoSuchElementException: Message: No element <* id=qbdfq> found at https://www.google.com, did you mean id=gbsfw?

Hello World!
============

.. code-block:: python

    driver = Chrome()
    driver.get('http://www.google.com')
    form_elm = driver.get_elm('gbqf')
    form_elm.fill_out_and_submit({
        'q': 'Hello World!',
    })
    driver.wait_for_element(id_='search')
    driver.quit()

Documentation
*************

Wrapper
=======

.. autoclass:: webdriverwrapper.wrapper._WebdriverBaseWrapper
    :members:

.. autoclass:: webdriverwrapper.wrapper._WebdriverWrapper
    :members:

.. autoclass:: webdriverwrapper.wrapper._WebElementWrapper
    :members:

Forms
=====

.. autoclass:: webdriverwrapper.forms.Form
    :members:

Downloading
===========

.. autoclass:: webdriverwrapper.download._Download
    :members:

Testing
=======

Supported are both UnitTest and PyTest tests. Each of them have own section
bellow, but first you have to know something about "expecting decorators".

After each test is called method
:py:meth:`check_expected_errors <webdriverwrapper.errors.WebdriverWrapperErrorMixin.check_expected_errors>`
and :py:meth:`check_expected_infos <webdriverwrapper.info.WebdriverWrapperInfoMixin.check_expected_infos>`
which will raise exception if there is some unexpected error. By default you
doesn't have to check everytime presence of some error - ``TestCase`` or PyTest
fixtures does that for you automatically. But sometimes you want to test that
something fail - that something ends with some error message or info message.
For that there are several decorators.

.. code-block:: python

    # Following test go to relative page "settings" and fill out and submit form.
    # Test have to ends on page where is info message to user with key sucessfuly_saved.
    @expected_info_message('sucesfully_saved')
    def test_save_data(driver):
        driver.go_to('settings')
        driver.fill_out_and_submit({
            'name': 'Michael',
        })

    # Test have to ends on page indicating that user doesn't have permission.
    @expected_error_page('403')
    def test_access_admin_page(driver):
        driver.go_to('admin')

When you need some changes in method
:py:meth:`get_error_page <webdriverwrapper.errors.WebdriverWrapperErrorMixin.get_error_page>`,
:py:meth:`get_error_traceback <webdriverwrapper.errors.WebdriverWrapperErrorMixin.get_error_traceback>`,
:py:meth:`get_error_messages <webdriverwrapper.errors.WebdriverWrapperErrorMixin.get_error_messages>`
or :py:meth:`get_info_messages <webdriverwrapper.info.WebdriverWrapperInfoMixin.get_info_messages>`,
feel free to change it like that:

.. code-block:: python

    from webdriverwrapper import Chrome

    driver = Chrome()

    # Better to set it on instance, so you can change browser without changing this code.
    dirver.__class__.get_error_page = your_method
    dirver.__class__.get_error_traceback = your_method
    dirver.__class__.get_error_messages = your_method
    dirver.__class__.get_info_messages = your_method

Decorators
----------

.. autofunction:: webdriverwrapper.decorators.expected_error_page
.. autofunction:: webdriverwrapper.decorators.allowed_error_pages
.. autofunction:: webdriverwrapper.decorators.expected_error_messages
.. autofunction:: webdriverwrapper.decorators.allowed_error_messages
.. autofunction:: webdriverwrapper.decorators.allowed_any_error_message
.. autofunction:: webdriverwrapper.decorators.expected_info_messages
.. autofunction:: webdriverwrapper.decorators.allowed_info_messages

Example
^^^^^^^

.. code-block:: python

    @expected_info_messages('Your information was updated.')
    def test_save(driver):
        driver.fill_out_and_submit({
            'name': 'Michael',
        })

Error and info messages
-----------------------

.. autoclass:: webdriverwrapper.errors.WebdriverWrapperErrorMixin
    :members:

.. autoclass:: webdriverwrapper.info.WebdriverWrapperInfoMixin
    :members:

PyTest
------

Import whole module in your main ``conftest.py`` and define fixture ``_driver``:

.. code-block:: python

    import pytest
    from webdriverwrapper import Chrome
    from webdriverwrapper.pytest import *


    # Create browser once for all tests.
    @pytest.yield_fixture(scope='session')
    def session_driver():
        driver = Chrome()
        yield driver
        driver.quit()


    # Before every test go to homepage.
    @pytest.fixture(scope='function')
    def _driver(session_driver):
        session_driver.get('http://www.google.com')
        return session_driver

Then you can write tests really simply:

.. code-block:: python

    def test_doodle(driver):
        driver.click('gbqfsb')
        assert driver.contains_text('Doodles')


    def test_search(driver):
        driver.get_elm('gbqf').fill_out_and_submit({
            'q': 'hello',
        })
        driver.wait_for_element(id_='resultStats')

.. automodule:: webdriverwrapper.pytest.conftest
    :members:

UnitTest
--------

.. autoattribute:: webdriverwrapper.unittest.ONE_INSTANCE_FOR_ALL_TESTS
.. autoattribute:: webdriverwrapper.unittest.ONE_INSTANCE_PER_TESTCASE
.. autoattribute:: webdriverwrapper.unittest.ONE_INSTANCE_PER_TEST

.. autoclass:: webdriverwrapper.unittest.WebdriverTestCase
    :members:
    :private-members:

Exceptions
==========

You doesn't have to care about some exception. In test result you will get some
exception with clear message. But if you need something special or is there some
confusion, these are all exceptions defined by this wrapper.

.. automodule:: webdriverwrapper.exceptions
    :members:
