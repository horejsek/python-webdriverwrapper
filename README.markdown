# Better interface for WebDriver in Python

## What this wrapper do

* Adds some usefull method to WebDriver and WebElement. Such as
 * `find_element_by_text`,
 * `contains_text`,
 * `wait_for_element`,
 * or `go_to` (explained below).
* Makes filling out forms easier.
* Provide TestCase.

## How to install chromedriver

Just install Chrome/ium and download chromedriver from [this site](https://code.google.com/p/chromedriver/downloads/list).

## Documentation

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

#### `contains_text(text)`

```python
if driver.contains_text(text):
    print 'good'
```

#### `get_elm(id_|class_name|tag_name|xpath[, parent_id|parent_class_name|parent_tag_name])`

Returns first element from list of found elements.

```python
elm = driver.find_element_by_id('someid')
elm.find_elements_by_class_name('someclasss')

# or with webdriverwrapper

elm = driver.get_elm(class_name='someclass', parent_id='someid')
```

#### `get_elms(id_|class_name|tag_name|xpath[, parent_id|parent_class_name|parent_tag_name])`

Same as `get_elm` but it returns all found elements.

#### `click([id_|class_name|tag_name|xpath[, parent_id|parent_class_name|parent_tag_name]])`

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

#### `wait_for_element(timeout=10, id_|class_name|tag_name|xpath[, parent_id|parent_class_name|parent_tag_name])`

Alias for `WebDriverWait(driver, timeout).until(lambda driver: driver.get_elm(...))`.

```python
driver.wait_for_element(id_='someid')
```

#### `go_to([path[, query[, domain]]])`

Go to page. It uses `driver.get` method.

Domain is parsed from `current_url` if you don't specify any, so you can define domain only once. Query can be string or dictionary. `path` can be whole URL.

```python
driver.go_to(domain='google.com')
driver.go_to('search')  # See, I do not need to write again google.com.
driver.go_to(query={'q': 'hello from cool webdriverwrapper'})
```

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

#### `fill_out_and_submit(data)`

Same as `fill_out`, but after that calls `submit`.

#### `submit()`

Some forms have more buttons than one. Simple example is: one for submit and one for reset. This method firstly look for element with id "`form id`_submit" and click on it. Otherwise it calls WebElement's submit.

#### `reset()`

Looks for element with id "`form id`_reset" and clicks on it.

### `WebdriverTestCase`

`WebdriverTestCase` provides method aliases on driver and some other cool stuff. If you need driver instance, it's *hide* in `self.driver`.

```python
from webdriverwrapper import WebdriverTestCase

class TestCase(WebdriverTestCase):
    def test(self):
        self.go_to('http://www.google.com')
        self.click('gbqfsb')  # I'm feeling luck.
        self.contains_text('Doodles')
```

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

#### `debug(msg)`

Show message in console. (Uses module `logging`.)

#### `break_point()`

Waits for user input. Good for debuging.

#### Usefull decorators

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

You can override method `get_errors` which returns list of error messages on page.

```python
class TestCase(WebdriverTestCase):
    @ShouldBeError('some-error')
    def test(self):
        # ...
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










