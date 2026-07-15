# POM BasePage

`BasePage` is a small shared base class for Page Objects.

It is part of the framework skeleton.

It is not application-specific.

---

## Purpose

The purpose of `BasePage` is to keep repeated low-level Playwright interaction
helpers in one place.

It can help with:

- opening pages,
- locating elements by stable `data-testid`,
- clicking,
- filling,
- reading text,
- reading visibility,
- waiting for basic page readiness.

It should stay small.

---

## What belongs in BasePage

Good candidates:

```text
open(path)
wait_for_ready()
by_test_id(test_id)
click_by_test_id(test_id)
fill_by_test_id(test_id, value)
text_by_test_id(test_id)
texts_by_test_id(test_id)
is_visible_by_test_id(test_id)
current_url()
title()
```

These are reusable technical helpers.

They do not know the tested application domain.

---

## What does not belong in BasePage

Do not put business behavior in `BasePage`.

Avoid methods such as:

```text
login_as_admin()
create_customer()
approve_order()
change_tariff_plan()
verify_invoice_is_paid()
assert_order_is_confirmed()
```

Those belong in:

- concrete Page Objects,
- Service Objects,
- fixtures,
- or test assertions.

---

## Assertion boundary

`BasePage` should not become an assertion container.

Page Objects may return useful state:

```python
order_confirmation.status()
cart_page.total()
customer_page.account_status()
```

Tests should own business assertions:

```python
assert order_confirmation.status() == "Order confirmed"
assert cart_page.total() == "4999.00 PLN"
```

This keeps Page Objects as adapters and tests as behavior checks.

---

## Example

A concrete Page Object may inherit from `BasePage`:

```python
from pages.base_page import BasePage


class LoginPage(BasePage):
    def open_login(self) -> None:
        self.open("/login")

    def login(self, username: str, password: str) -> None:
        self.fill_by_test_id("username", username)
        self.fill_by_test_id("password", password)
        self.click_by_test_id("login-submit")

    def error_message(self) -> str:
        return self.text_by_test_id("login-error")
```

The test remains responsible for the assertion:

```python
login_page.open_login()
login_page.login("wrong-user", "wrong-password")

assert login_page.error_message() == "Invalid username or password"
```

---

## Design rule

```text
BasePage provides reusable browser mechanics.
Concrete Page Objects provide application-facing actions.
Tests provide business assertions.
```
