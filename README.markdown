# Better interface for WebDriver in Python

> **Warning: Do not use it yet! Work in progress.**

## What this wrapper do

* Adds some usefull method to WebDriver and WebElement. Such as
 * `find_element_by_text`,
 * `contains_text`,
 * `wait_for_element`,
 * or `go_to` (explained below).
* Makes filling out forms easier.
* Provide TestCase.

## Documentation

```python
driver = Firefox()
```

### Method added to `WebDriver` and `WebElement`

#### `find_element_by_text(text)`

```python
elements = driver.find_element_by_text('hello')
another_elements = elements[0].find_element_by_text('world')
```

#### `contains_text(text)`

```python
if driver.contains_text(text):
    print 'good'
```

#### `get_elm(id_|class_name|tag_name|xpath[, parent_id|parent_class_name|parent_tag_name])`

It returns first element from list of found elements.

```python
elm = driver.find_element_by_id('someid')
elm.find_elements_by_class_name('someclasss')

# or with webdriverwrapper

elm = driver.get_elm(class_name='someclass', parent_id='someid')
```

#### `get_elms(id_|class_name|tag_name|xpath[, parent_id|parent_class_name|parent_tag_name])`

Same as `get_elm` but it returns all found elements.

#### `click([id_|class_name|tag_name|xpath[, parent_id|parent_class_name|parent_tag_name]])`

It clicks on first found element if you pass some arguments. Otherwise it calls webdriver's click method.

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

Domain is parsed from `current_url` if you don't specify any, so you can define domain only once. Query can be string or dictionary.

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

This looks for element with id "`form id`_reset" and clicks on it.

















