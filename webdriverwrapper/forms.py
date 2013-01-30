# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

from webdriverwrapper import _WebElementWrapper


class Form(_WebElementWrapper):
    def fill_out_and_submit(self, data):
        self.fill_out(data)
        self.submit()

    def fill_out(self, data):
        for elm_name, value in data.iteritems():
            FormElement(self, elm_name).fill_out(value)

    def submit(self):
        elm_name = '%s_submit' % self.id
        try:
            self.click(elm_name)
        except NoSuchElementException:
            super(Form, self).submit()

    def reset(self):
        elm_name = '%s_reset' % self.id
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
        raise NoSuchElementException()

    def fill_input_checkbox(self, value):
        if isinstance(value, (list, tuple)):
            self.fillOut_input_checkbox_multiple(value)
        self.fillOut_input_checkbox_single(value)

    def fill_input_checkbox_single(self, value):
        elm = self.formElm.find_element_by_xpath('//input[@type="checkbox"][@name="%s"]' % self.elmName)
        if bool(value) != elm.is_selected():
            elm.click()

    def fill_input_checkbox_multiple(self, value):
        for item in value:
            elm = self.formElm.find_element_by_xpath('//input[@type="checkbox"][@name="%s"][@value="%s"]' %  (self.elmName, self.convertValue(item)))
            elm.click()

    def fill_input_radio(self, value):
        elm = self.form_elm.find_element_by_xpath('//input[@type="radio"][@name="%s"][@value="%s"]' % (self.elm_name, self.convert_value(value)))
        elm.click()

    def fill_input_file(self, value):
        elm = self.form_elm.find_element_by_name(self.elm_name)
        elm.send_keys(self.convert_value(value))

    def fill_select_selectone(self, value):
        self._fillout_select(self.convert_value(value))

    def fill_select_selectmultiple(self, value):
        if not isinstance(value, (list, tuple)):
            self._fill_select(self.convert_value(value))
            return

        for item in self.convert_value(value):
            self._fill_select(item)

        # In multiselect I have to unselected already selected options.
        not_values = ''.join('[@value!="%s"]' % v for v in self.convert_value(value))
        elms = self.form_elm.find_elements_by_xpath('//select[@name="%s"]/descendant::option%s' % (self.elm_name, not_values))
        for elm in elms:
            if elm.is_selected():
                elm.click()

    def _fill_select(self, value):
        elm = self.form_elm.find_element_by_xpath('//select[@name="%s"]/descendant::option[@value="%s"]' % (self.elm_name, value))
        if not elm.is_selected():
            elm.click()

    def fill_common(self, value):
        elm = self.form_elm.find_element_by_name(self.elm_name)
        elm.clear()
        elm.send_keys(self.convert_value(value))
