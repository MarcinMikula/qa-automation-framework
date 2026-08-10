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

## Optional TestRepairEngine boundary

`click_by_test_id()` and `fill_by_test_id()` may delegate a timed-out Playwright
interaction to TestRepairEngine when the optional package is installed and its
pytest runtime is explicitly enabled.

The boundary remains mechanical:

```text
Concrete Page Object
-> BasePage test-id helper
-> Playwright interaction
-> Playwright timeout
-> optional TestRepairEngine recovery
-> retry the same interaction once
-> original test continues
```

Important rules:

- `BasePage` does not import TestRepairEngine at module load time,
- the framework remains runnable when TestRepairEngine is absent,
- TestRepairEngine disabled means the original Playwright timeout is preserved,
- non-timeout Playwright errors are not delegated to TestRepairEngine,
- concrete Page Objects do not know about the repair engine,
- assertions and expected business behavior are never repaired here,
- a recovered interaction is not equivalent to a passing test.

The current integration slice is intentionally limited to timed-out
`data-testid` click and fill helpers. Other failure modes, locator families, or
interaction types require separate validation before they belong in this
boundary.

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
Optional runtime recovery may intercept only validated low-level timeouts.
```
