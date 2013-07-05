# Better interface for WebDriver in Python

## What this wrapper do

* Adds messges into webdriver's exceptions (by default there is no information about which element is missing etc.).
* Adds some usefull method to WebDriver and WebElement. Such as
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

### `WebDriver` specific method

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

Domain is parsed from `current_url` if you don't specify any, so you can define domain only once. Query can be string or dictionary. `path` can be whole URL.

```python
driver.go_to(domain='google.com')
driver.go_to('search')  # See, I do not need to write again google.com.
driver.go_to(query={'q': 'hello from cool webdriverwrapper'})
```

#### `switch_to_window(window_name|title|url)`

Switch to window by `window_name` (Selenium's classic way) or by `title` or by `url`.

```python
driver.click('some-link-which-opens-popup')
driver.switch_to_window(title='New popup window')
# make some work in popup
```

Param `url` can be dictionary and this dictionary can have three keys: `path`, `query` and `domain`. It's same as for method `go_to`. If you don't specify `domain`, it will be recognized from current url.

```python
driver.switch_to_window(url='http://www.example.com/path')
# or
driver.switch_to_window(url={'path': 'path'})
```

#### `close_window(window_name|title|url)`

Close window and stay in current window. Params are same as in `switch_to_window`.

#### `close_other_windows()`

Close all windows except the current window.

### `WebElement` specific method

#### `download_file()`

Download file by clicking on some link using Selenium is not good idea. With Chrome it's working thanks to no save dialog by default, but still you can't check status code, data, headers, etc. For that purpose there is special method `download_file`. You can call it will try download file using Python's `urllib2`. Method returns special object (not response or file data) which hold some useful information.

```python
f = driver.get_elm('some-link').download_file()
f.method  # You can check if method was GET or POST (returns in lowercase).
f.status_code
f.headers  # Dictionary of all response headers.
f.data
```

This method support downloading from link (use attribute href) or from button in form (use action or current URL). It looks for attribute method of form, so is used correctly GET or POST. Method collect all data from form and pass it to URL (in case of method GET) or to data request (in case of method POST).

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

#### `fill_out_and_submit(data)`

Same as `fill_out`, but after that calls `submit`.

#### `submit()`

Some forms have more buttons than one. Simple example is: one for submit and one for reset. This method firstly look for element with id "`form id`_submit" and click on it. Otherwise it calls WebElement's submit.

#### `reset()`

Looks for element with id "`form id`_reset" and clicks on it.

### Select

If some element is select, it returns Select instance inherited from selenium's Select and WebDriver wrapper. So you can use all method from WebDriver and Select.

```python
select = driver.get_elm(tag_name='select')
select.get_attribute('name')
select.select_by_value('value')
select.find_elements_by_text('Option text')
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

By default `WebdriverTestCase` create instance of Firefox. You can overwrite this method and create which instance of driver you want.

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

When your test need check of errors somewhere in the middle of the test, just call this method. It call same check as is called after each test.

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

By default `WebdriverTestCase` looks for error messages in elements with class `error`. If you want to test that some page have some error message, use this decorator.

```python
class TestCase(WebdriverTestCase):
    @ShouldBeError('some-error')
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

##### `wait_after_test`

When you have to do some debug page (for example with Firebug or with Chrome Developer tools), you can set `wait_after_test` and after each test it waits for input to continue.

```python
class TestCase(WebdriverTestCase):
    wait_after_test = True
```

#### Windows

If you in your test switch to another window, you don't have to remeber that you have to switch back into main window. `WebdriverTestCase` ensure that every tests starts in main window.
