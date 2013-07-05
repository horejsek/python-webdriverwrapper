# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random
from selenium.common.exceptions import WebDriverException, NoAlertPresentException

from webdriverwrapper.errors import CanBeError, get_error_page
from webdriverwrapper.testcase import WebdriverTestCase

__all__ = ('FuzzyTestCaseType', 'FuzzyTest')


class FuzzyTestCaseType(type):
    count_of_clicks = 50
    can_be_error_decorator = CanBeError

    def __new__(mcs, name, bases, attrs):
        mcs.create_test_methods(attrs)
        return type.__new__(mcs, name, bases, attrs)

    @classmethod
    def create_test_methods(mcs, attrs):
        for index in range(mcs.count_of_clicks):
            test_method = mcs.create_test_method()
            if mcs.can_be_error_decorator:
                # Fuzzy tests can see error messages, but not error pages like 500.
                test_method = mcs.can_be_error_decorator()(test_method)
            attrs['test_%03d' % index] = test_method

    @classmethod
    def create_test_method(mcs):
        return lambda self: self._test()


class FuzzyTestCase(WebdriverTestCase):
    # Do this in inherited class.
    #__metaclass__ = FuzzyTestCaseType

    def _test(self):
        #  If this page is some error page, we need go back to homepage and start
        #+ again. Error page doesn't need to have some clickable elment...
        if self.is_error_page():
            self.reset_after_page_error()

        clickable_clements = self.get_clickable_elements()
        element = self._choose_element(clickable_clements)
        if not element:
            return

        #  When fuzzy test find some error, it's good to have possibility to find
        #+ how it happened. Therefor there is logging of clicking.
        self.debug('<%(tagName)s id=%(id)s class=%(className)s>%(text)s</%(tagName)s>' % {
            'tagName': element.tag_name,
            'id': element.get_attribute('id'),
            'className': element.get_attribute('class'),
            'text': element.text,
        })
        self._process_click(element)

    def is_error_page(self):
        return bool(get_error_page(self.driver))

    def reset_after_page_error(self):
        self.go_to('/')

    def get_clickable_elements(self):
        clicable_element_types = tuple('%s[not(contains(@class, "selenium_donotclick"))]' % i for i in (
            'a', 'submit', 'input[@type="submit"]',
        ))
        xpath = '|'.join('//%s' % item for item in clicable_element_types)
        return self.get_elms(xpath=xpath)

    def _choose_element(self, clickable_elements):
        if not len(clickable_elements):
            raise Exception('No clickable element.')
        return self._choose_visible_element(clickable_elements)

    def _choose_visible_element(self, clickable_elements):
        # Hope that there will be something clickable in 10 attempts...
        for _ in range(10):
            element_index = random.randint(0, len(clickable_elements) - 1)
            element = clickable_elements[element_index]
            if element.is_displayed() and element.is_enabled():
                return element
        return element

    def _process_click(self, element):
        try:
            element.click()
        except WebDriverException:
            #  Some element doesn't need to be visible. Maybe some JS was slow
            #+ so element few ms ago was visible, but not now. Or some bug in
            #+ chromedriver and so on.
            #  Don't care about these errors.
            pass
        except Exception as exc:
            self.fail('Fail during click on element <%s id="%s" class="%s">: %s' % (
                element.tag_name,
                element.get_attribute('id'),
                element.get_attribute('class'),
                str(exc),
            ))

        #  Some action have to be confirmed (Do you want really to delete this?).
        #  In selenium isn't method 'is_alert_present?', so just try to
        #+ confirm it and pass it when occurs NoAlertPresentException.
        try:
            alert = self.driver.switch_to_alert()
            alert.accept()
        except NoAlertPresentException:
            pass
