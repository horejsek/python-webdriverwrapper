# -*- coding: utf-8 -*-

from webdriverwrapper import Chrome


driver = Chrome()
driver.get('http://www.google.com')
form_elm = driver.get_elm('gbqf')
form_elm.fill_out_and_submit({
    'q': 'hello world!',
})
driver.wait_for_element(id_='search')
driver.quit()
