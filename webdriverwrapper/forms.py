# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from webdriverwrapper import _WebElementWrapper
from exceptions import _create_exception_msg

__all__ = ('Form',)


class Form(_WebElementWrapper):
    def fill_out_and_submit(self, data, prefix=''):
        self.fill_out(data, prefix)
        self.submit()

    def fill_out(self, data, prefix=''):
        for elm_name, value in data.iteritems():
            FormElement(self, prefix + elm_name).fill_out(value)

    def submit(self):
        elm_name = '%s_submit' % self.get_attribute('id')
        try:
            self.click(elm_name)
        except NoSuchElementException:
            super(Form, self).submit()

    def reset(self):
        elm_name = '%s_reset' % self.get_attribute('id')
        self.click(elm_name)


class FormElement(object):
    def __init__(self, form_elm, elm_name):
        self.form_elm = form_elm
        self.elm_name = elm_name

    def convert_value(self, value):
        if not isinstance(value, (list, tuple)):
            return self._convert_value_to_string(value)

        values = []
        for item in value:
            values.append(self._convert_value_to_string(item))
        return values

    def _convert_value_to_string(self, value):
        if isinstance(value, bool):
            value = int(value)
        elif value is None:
            value = ''
        return str(value)

    def fill_out(self, value):
        tag_name, elm_type = self.analyze_element()
        method_name = ('fill_%s_%s' % (tag_name, elm_type)).replace('-', '')
        getattr(self, method_name, self.fill_common)(value)

    def analyze_element(self):
        elms = self.form_elm.get_elms(name=self.elm_name)
        for elm in elms:
            elm_type = elm.get_attribute('type')
            if elm_type == 'hidden':
                continue
            return elm.tag_name, elm_type
        raise NoSuchElementException(_create_exception_msg(name=self.elm_name))

    def fill_input_checkbox(self, value):
        if isinstance(value, (list, tuple)):
            self.fill_input_checkbox_multiple(value)
        self.fill_input_checkbox_single(value)

    def fill_input_checkbox_single(self, value):
        elm = self.form_elm.get_elm(xpath='//input[@type="checkbox"][@name="%s"]' % self.elm_name)
        if bool(value) != elm.is_selected():
            elm.click()

    def fill_input_checkbox_multiple(self, value):
        for item in value:
            elm = self.form_elm.get_elm(xpath='//input[@type="checkbox"][@name="%s"][@value="%s"]' %  (
                self.elm_name,
                self.convert_value(item),
            ))
            elm.click()

    def fill_input_radio(self, value):
        elm = self.form_elm.get_elm(xpath='//input[@type="radio"][@name="%s"][@value="%s"]' % (
            self.elm_name,
            self.convert_value(value),
        ))
        elm.click()

    def fill_input_file(self, value):
        elm = self.form_elm.get_elm(name=self.elm_name)
        elm.send_keys(self.convert_value(value))

    def fill_select_selectone(self, value):
        select = self.form_elm.get_elm(name=self.elm_name)
        select.select_by_value(self.convert_value(value))

    def fill_select_selectmultiple(self, value):
        if not isinstance(value, (list, tuple)):
            value = [value]

        select = self.form_elm.get_elm(name=self.elm_name)
        select.deselect_all()
        for item in self.convert_value(value):
            select.select_by_value(item)

    def fill_common(self, value):
        elm = self.form_elm.get_elm(name=self.elm_name)
        elm.clear()
        elm.send_keys(self.convert_value(value))
        elm.send_keys(Keys.TAB)  # Send TAB for losing focus. (Trigger change events.)

