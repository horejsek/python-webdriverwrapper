import pytest

from webdriverwrapper.exceptions import NoSuchElementException, TimeoutException
from webdriverwrapper.wrapper import _WebElementWrapper


def test_returns_wrapped_element(driver):
    elm = driver.find_element_by_id('somepage')
    assert isinstance(elm, _WebElementWrapper)


def test_find_elements_by_integer(driver):
    elms = driver.get_elms(text=42)
    assert len(elms) == 1


def test_find_elements_by_str(driver):
    assert driver.get_elms(text='ěščřž')


def test_find_elements_by_unicode(driver):
    # six.u is safe only with ASCII, so I need some hack.
    text = 'ěščřž'
    if hasattr(text, 'decode'):
        text = text.decode('utf8')

    assert driver.get_elms(text=text)


def test_find_elements_selenium_not_search(driver):
    elms = driver.get_elms(text='text')
    assert len(elms) == 2


def test_contains_text(driver):
    assert driver.contains_text('text')


def test_find_element_by_text(driver):
    assert driver.get_elm(text='text')


def test_find_element_by_text_fail(driver):
    with pytest.raises(NoSuchElementException) as excinfo:
        driver.get_elm(text='notextatpage')


def test_wait_for_element(driver):
    assert driver.wait_for_element(timeout=0.5, id_='somepage')


def test_wait_for_element_on_element(driver):
    with pytest.raises(TimeoutException):
        assert driver.get_elm(id_='somepage').wait_for_element(timeout=0.5, tag_name='p')


def test_wait_for_element_fail(driver):
    with pytest.raises(TimeoutException) as excinfo:
        driver.wait_for_element(timeout=0.5, id_='nosuchelement', parent_tag_name='body')


def test_wait_for_element_hide(driver):
    driver.wait_for_element_hide(timeout=0.5, id_='nosuchelement')


def test_wait_for_element_hide_fail(driver):
    with pytest.raises(TimeoutException) as excinfo:
        driver.wait_for_element_hide(timeout=0.5, id_='somepage', parent_tag_name='body')
