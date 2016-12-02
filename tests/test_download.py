# -*- coding: utf-8 -*-


def test_download_page_by_url(driver):
    result = driver.download_url('http://www.google.com')
    assert 'Google' in result.data


def test_download_page_by_url_path(driver):
    driver.get('http://www.google.com')
    result = driver.download_url('doodles')
    assert 'Doodles' in result.data


def test_download_current_page(driver):
    driver.get('http://www.google.com')
    result = driver.download_url()
    assert 'Google' in result.data


def test_download_file_by_link(driver):
    driver.get('http://www.google.com')
    result = driver.get_elm(xpath='//a[contains(@href, "about")]').download_file()
    assert 'about' in result.data


def test_download_file_by_form(driver):
    driver.get('http://www.google.com')
    form = driver.get_elm(tag_name='form')
    form.fill_out({'q': 'selenium'})
    result = form.download_file()
    assert 'selenium' in result.data
