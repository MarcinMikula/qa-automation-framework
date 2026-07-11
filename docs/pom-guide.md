# POM guide

Page Object Model is the UI adapter layer of the framework.

Its purpose is to hide browser and selector mechanics from tests.

---

## Responsibility of a Page Object

A Page Object should know:

- locators,
- page-specific actions,
- navigation details,
- waits and synchronization,
- stable ways to read visible state.

It should expose meaningful user actions:

```python
login_page.login(username, password)
dashboard.search_customer(msisdn)
case_page.create_case(subject, priority)
```

---

## Responsibility of a test

A test should know:

- scenario,
- input data,
- expected result,
- business meaning.

It should not know:

- CSS selectors,
- XPath expressions,
- low-level Playwright calls,
- implementation details of the page.

---

## Assertions

Prefer keeping business assertions in tests.

A Page Object may expose helper methods that make assertions readable:

```python
assert dashboard.is_loaded()
assert case_page.success_message_visible()
assert case_page.current_status() == "New"
```

Avoid hiding business expectations inside actions:

```python
case_page.create_case_and_assert_success(...)
```

That makes the scenario harder to read and maintain.

---

## Locator strategy

Recommended order:

1. stable `data-testid` attributes,
2. accessible roles and names,
3. stable labels and form semantics,
4. CSS/XPath only when no better option exists.

A framework skeleton should encourage stable locators, but real projects may
not always provide them.

When locators are weak, document the trade-off.

---

## Example structure

```python
class LoginPage(BasePage):
    username_input = "[data-testid='username']"
    password_input = "[data-testid='password']"
    submit_button = "[data-testid='login-button']"

    def login(self, username: str, password: str) -> None:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.submit_button)
```

The test can then stay focused on the scenario:

```python
def test_user_can_log_in(login_page, dashboard_page):
    login_page.login("admin", "secret")

    assert dashboard_page.is_loaded()
```

---

## Salesforce-like note

For heavy enterprise UIs such as Salesforce-like CRM systems, Page Objects
should avoid overfitting to unstable DOM details.

Prefer methods that describe business actions:

```python
opportunity_page.create_opportunity(...)
case_page.assign_case(...)
case_page.mark_status_as_complete(...)
```

The implementation can later handle the messy UI details internally.
