# Better interface for WebDriver in Python

## Install

`pip install webdriverwrapper`

Support for Python 2.6 and higher (including Python 3).

## What this wrapper do

* Adds messges into webdriver's exceptions (by default there is no information about which element is missing etc.).
* Adds some usefull methods to WebDriver and WebElement. Such as
 * `find_element_by_text`,
 * `contains_text`,
 * `wait_for_element`,
 * or `go_to` (explained below).
* Makes filling out forms easier.
 * If some WebElement is also form element, you can call method `fill_out` with dictionary as parameter. More info below.
 * If some WebElement is also Select, you can call methods from webdriver's Select class.
* Provide TestCase.

## How to install chromedriver

Just install Chrome/ium and put [chromedriver](https://code.google.com/p/chromedriver/downloads/list) into `/bin`.

## Documentation

This is documentation of wrapper. Documentation of Selenium is on [googlecode.com](http://selenium.googlecode.com/svn/trunk/docs/api/py/index.html).

```python
from webdriverwrapper import Firefox
driver = Firefox()
```

### Method added to `WebDriver` and `WebElement`

#### `find_elements_by_text(text)`

```python
elements = driver.find_elements_by_text('hello')
another_elements = elements[0].find_element_by_text('world')
```

If you want to ignore some elements (for example some debug texts in development), add to these elements attribute `data-selenium-not-search`.

#### `contains_text(text)`

```python
if driver.contains_text(text):
    print 'good'
```

#### `get_elm(id_|class_name|name|tag_name|xpath[, parent_id|parent_class_name|parent_name|parent_tag_name])`

Returns first element from list of found elements.

```python
elm = driver.find_element_by_id('someid')
elm.find_elements_by_class_name('someclasss')

# or with webdriverwrapper

elm = driver.get_elm(class_name='someclass', parent_id='someid')
```

#### `get_elms(id_|class_name|name|tag_name|xpath[, parent_id|parent_class_name|parent_name|parent_tag_name])`

Same as `get_elm` but it returns all found elements.

#### `click([id_|class_name|name|tag_name|xpath[, parent_id|parent_class_name|parent_name|parent_tag_name]])`

Clicks on first found element if you pass some arguments. Otherwise it calls webdriver's click method.

```python
elm = driver.find_element_by_id('someid')
elm = elm.find_elements_by_class_name('someclasss')[0]
elm.click()

# or with webdriverwrapper

elm = driver.get_elm(class_name='someclass', parent_id='someid')
elm.click()

# or

driver.get_elm('someid').click(class_name='someclass')

# or

driver.click(class_name='someclass', parent_id='someid')
```

### `WebDriverWrapper` specific methods

#### `wait_for_element(timeout=10, message='', id_|class_name|name|tag_name|xpath[, parent_id|parent_class_name|parent_name|parent_tag_name])`

Alias for `WebDriverWait(driver, timeout).until(lambda driver: driver.get_elm(...), message)`.

```python
driver.wait_for_element(id_='someid')
```

#### `wait(timeout=10)`

Alias for `WebDriverWait(driver, timeout)`.

```python
driver.wait().until_not(lambda driver: len(driver.get_elms('id')) > 10)
```

#### `go_to([path[, query[, domain]]])`

Go to page. It uses `driver.get` method.

When domain is not supplied, it is parsed from `current_url`, so you can define domain only once. Query can be string or dictionary. `path` can be whole URL.

```python
driver.go_to(domain='google.com')
driver.go_to('search')  # See, I do not need to write again google.com.
driver.go_to(query={'q': 'hello from cool webdriverwrapper'})
```

#### `switch_to_window(window_name|title|url)`

Switch to window with `window_name` (Selenium's classic way) or `title` or `url`.

```python
driver.click('some-link-which-opens-popup')
driver.switch_to_window(title='New popup window')
# make some work in popup
```

Param `url` can be dictionary and this dictionary can have three keys: `path`, `query` and `domain`. It's the same as for method `go_to`. If you don't specify `domain`, it will be recognized from current url.

```python
driver.switch_to_window(url='http://www.example.com/path')
# or
driver.switch_to_window(url={'path': 'path'})
```

#### `close_window(window_name|title|url)`

Close window and stay in current window. Params are same as in `switch_to_window`.

#### `close_other_windows()`

Close all windows except the current window.

#### `get_alert()`

Returns instance of `selenium.webdriver.common.alert.Alert`. It's just alias, because it's hard to remember where that class is.

```python
driver.get_alert().accept()
driver.get_alert().dismiss()
```

### `download_url(url=None)`

Downloads page from `url` or `current_url` if not supplied. Works the same way as `download_file()`.

```python
f = driver.download_url('http://myurl.com')
f.status_code
f.headers  # Dictionary of all response headers.
f.data
```

### `WebElement` specific methods

#### `download_file()`

It is not a good idea to download file by clicking on a link using Selenium. With Chrome it's working thanks to no save dialog by default, but still you can't check status code, data, headers, etc. For that purpose there is special method `download_file`. You can call it will try download file using Python's `urllib2`. Method returns special object (not response or file data) which hold some useful information.

```python
f = driver.get_elm('some-link').download_file()
f.method  # You can check if method was GET or POST (returns in lowercase).
f.status_code
f.headers  # Dictionary of all response headers.
f.data
```

This method supports downloading from link (use attribute href) or from button in a form (use action or current URL). It looks for attribute method of a form, so is used correctly GET or POST. Method collects all data from form and pass it to URL (in case of method GET) or to data request (in case of method POST).

### Forms

If some element is form, it provides some more methods.

```python
form = driver.get_elm('formid')
```

#### `fill_out(data)`

```python
form.fill_out({
    'name': 'WebdriverWrapper',  # Normal input
    'type': 'testing-tool',  # Selectbox
    'is_awesome': True,  # Checkbox
    'whatever': [1, 2, 3],  # Multicheckbox
})
```

Method will send key TAB if element is input of type text or textarea. Purpose of this is because of onchange event - JS function registred on that event will be called after losing of focus.

If checkbox is hidden, then webdriverwrapper will click on ancestor label. It's a way how to make nice checkboxes in bootstrap and so.

#### `fill_out_and_submit(data)`

Same as `fill_out`, but after that calls `submit`.

#### `submit()`

Some forms have more buttons than one. Simple example is: one for submit and one for reset. This method firstly look for element with id "`form id`_submit" and click on it. Otherwise it calls WebElement's submit.

#### `reset()`

Looks for element with id "`form id`_reset" and clicks on it.

### Select

If some element is selected, it returns Select instance inherited from selenium's Select and WebDriver wrapper. So you can use all method from WebDriver and Select.

```python
select = driver.get_elm(tag_name='select')
select.get_attribute('name')
select.select_by_value('value')
select.find_elements_by_text('Option text')
```

### Exceptions

You can import all Selenium's exceptions from webdriverwrapper:

```
import webdriver.exceptions
```

### `WebdriverTestCase`

`WebdriverTestCase` provides method aliases on driver and some other cool stuff. If you need driver instance, it's *hide* in `self.driver`.

```python
from webdriverwrapper.testcase import WebdriverTestCase

class TestCase(WebdriverTestCase):
    def test(self):
        self.go_to('http://www.google.com')
        self.click('gbqfsb')  # I'm feeling luck.
        self.contains_text('Doodles')
```

Tip: if you want to write something into `__init__`, write it into method `init` and you do not have to call parent's `__init__`.

#### `_get_driver()`

By default `WebdriverTestCase` creates instance of Firefox. You can overwrite this method and create instance of driver you want.

#### `_check_error_messages()`

`WebdriverTestCase` check your web application on errors. When your page contains some elements with class `error`, this method finds them and print that there is some problem.

#### `_check_js_errors()`

`WebdriverTestCase` looks for JavaScript errors in your web application. For that you need put into your site this code:

```javascript
<script type="text/javascript">
    window.jsErrors = [];
    window.onerror = function(errorMessage) {
        window.jsErrors[window.jsErrors.length] = errorMessage;
    }
</script>
```

#### `check_errors()`

When your test needs to check errors somewhere in the middle of the test, just call this method. It call same check as is called after each test with one difference that it not depends on decorator. It means that no error is allowed.

#### `make_screenshot([screenshot_name])`

You can take screenshot of what is currently seen in browser window by this method. If you will not provide `screenshot_name`, name of test will be used.

If you want to take screenshot of failed test, just provide class variable `screenshot_path`.

```python
class TestCase(WebdriverTestCase):
    screenshot_path = '/tmp'

    def test_fail(self):
        self.go_to('http://google.com')
        self.click('some-non-exist-element')  # Fail, so screenshot will be taken automatically.

    def test_ok(self):
        self.go_to('http://google.com')
        self.make_screenshot('some-screenshot.png')  # Will not fail, but I can take screenshot manually.
```

#### `debug(msg)`

Show message in console. (Uses module `logging`.)

#### `break_point()`

Waits for user input. Good for debuging.

#### Usefull decorators

```python
from webdriverwrapper.decorators import *
```

##### `GoToPage`

##### `ShouldBeOnPage`

```python
class TestCase(WebdriverTestCase):
    @GoToPage('http://www.google.com')
    @ShouldBeOnPage('doodles/finder/2013/All%20doodles')
    def test(self):
        self.click('gbqfsb')
        self.contains_text('Doodles')
```

##### `ShouldBeError`

By default `WebdriverTestCase` looks for error messages in elements with class `error`. If you want to test that some page has some error message, use this decorator.

```python
class TestCase(WebdriverTestCase):
    @ShouldBeError('some-error')
    def test(self):
        # ...
```

##### `CanBeError`

Same as `ShouldBeError`, but if test ends without error, it's ok as well as with error.

##### `ShouldByErrorPage`

Similar to `ShouldByError`, but it looks for error page, not error message. By error page I mean page with code 403, 404, 500 and so on. By default error page is decoded from `.error-page h1`.

You can override method `get_error_page` which returns title of error page (for example 404 Not found).

```python
class TestCase(WebdriverTestCase):
    @ShouldBeErrorPage(403)
    def test(self):
        # ...
```

You can override method `get_error_messages` which returns list of error messages on page. Default implementation returns all texts from elements with class `error`. But text is bad for testing (it can be changed one day), so you can specify attribute `error`:

```html
<div class="error" error="username_is_mandatory">Username is mandatory</div>
```

##### `ShouldBeInfo`

Same as `ShoulBeError`, just looks for info messages.

```python
class TestCase(WebdriverTestCase):
    @ShouldBeInfo('some-info')
    def test(self):
        # ...
```

You can override method `get_info_messages` which returns list of info messages on page. Default implementation returns all texts from elements with class `info`. But text is bad for testing (it can be changed one day), so you can specify attribute `info`:

```html
<div class="info" info="successfully_saved">Your profile was successfully saved</div>
```

#### TestCase options

##### `domain`

By default you have to specify domain in first `go_to` call. It's not good because you should not know which test is called first. So you can specify domain by this class variable.

```python
class TestCase(WebdriverTestCase):
    domain = 'www.example.com'
```

##### `instances_of_driver`

By default `WebdriverTestCase` create one driver for all tests. If you want one driver for every `TestCase` or for every test, change this variable.

Note: It's good to define it in some base TestCase for all TestCases.

```python
from webdriverwrapper.testcase import ONE_INSTANCE_FOR_ALL_TESTS

class TestCase(WebdriverTestCase):
    instances_of_driver = ONE_INSTANCE_FOR_ALL_TESTS
```

Options are:

 * `ONE_INSTANCE_FOR_ALL_TESTS`
 * `ONE_INSTANCE_PER_TESTCASE`
 * `ONE_INSTANCE_PER_TEST`

Warning: If you use option `ONE_INSTANCE_FOR_ALL_TESTS` (which is default), you need to call by yourself class method `quit_driver` for example like this:

```python
from webdriverwrapper.testcase import WebdriverTestCase
import nose

ok = nose.run(...)

WebdriverTestCase.quit_driver()
```

##### `wait_after_test`

When you have to do some debug page (for example with Firebug or with Chrome Developer tools), you can set `wait_after_test` and after each test it waits for input to continue.

```python
class TestCase(WebdriverTestCase):
    wait_after_test = True
```

#### Windows

If you in your test switch to another window, you don't have to remeber that you have to switch back into main window. `WebdriverTestCase` ensure that every tests starts in main window.

### `FuzzyTestCase`

Trust me, it's good to test web app by randomly clicking on links and buttons. It can find a lot of bugs, mostly JS (when you call some JS and some element doesn't exist and so on). For this webdriverwrapper provide `FuzzyTestCase`. It randomly click on clickable elements and looks for page error (code 500) and JS errors.

Whole example is in examples/fuzzy.py.

You can override several methods:

#### `is_error_page()`

By default calls `get_error_page` and returns `True` if curren page is error page. You shoul override it when you override method `get_error_page`.

#### `reset_after_page_error()`

When error occurs by randomly clicking, it's good to restart to some default state. By default is called `self.go_to('/')`. If you need something more, there is place where you should put that code.

#### `get_clickable_elements()`

Returns all clickable elememnts on current page. By default it returns all `a`, `submit` and `input[@type="submit"]` elements which doesn't have class `selenium_donotclick`.

TIP: When you want to make some elements more important, just add more references for them. For example if you want click mostly on some elements in page and don't click very ofter to menu, you can write something like this:

```python
class FuzzyTest(FuzzyTestCase):
    def get_clickable_elements(self):
        elms_in_menu = self.get_elms(...)
        other_elms = self.get_elms(...)
        return elms_in_menu + other_elms * 5
```

TIP 2: Do not forget remove elements with class `selenium_donotclick`. Then you can add this class to elements which you want to test by fuzzy. Because it can for example delete something from database and destroy rest of test.

#### Metaclass `FuzzyTestCaseType`

You have to use this metaclass for your test. It create by default 50 tests (50 random clicks) which you can override by class variable `count_of_clicks`.

If you overrided method `get_error_messages`, you should pass your class `CanBeError` to this class by class variable `can_be_error_decorator`. In fuzzy testing some error messages are ignored. If you don't want ignore error messages, pass `None`.
