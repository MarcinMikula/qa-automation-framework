# Page Object Model guide

Page Object Model is the UI automation layer of this framework.

Its purpose is to keep browser mechanics out of tests.

A test should describe the scenario. A Page Object should know how to interact with the page.

## Scope

Use POM for:

- browser-based E2E tests,
- UI workflows,
- form interactions,
- page navigation,
- visible state checks,
- user-facing flows.

Do not use POM for:

- raw API calls,
- database setup,
- backend state manipulation,
- low-level HTTP checks,
- business logic that belongs in service objects or fixtures.

## Basic rule

Tests should not know selectors.

Weak test:

```python
page.locator("[data-testid='username']").fill("admin")
page.locator("[data-testid='password']").fill("secret")
page.locator("[data-testid='login-button']").click()
```

Better test:

```python
login_page.login(username="admin", password="secret")
```

The first version exposes UI mechanics. The second version expresses user intent.

## Responsibility split

### Page Object responsibilities

A Page Object should own:

- locators,
- page-specific actions,
- page-specific waits,
- simple page state queries,
- navigation details when they belong to that page.

### Test responsibilities

A test should own:

- scenario name,
- test data choice,
- business intent,
- assertions,
- test-level setup and teardown.

### Important convention: no heavy assertions in Page Objects

Page Objects should generally avoid test assertions.

They may expose query methods such as:

```python
def get_success_message(self) -> str:
    return self.get_text(self.SUCCESS_MESSAGE)
```

The test should decide what to assert:

```python
assert case_page.get_success_message() == "Case created"
```

This keeps Page Objects reusable across scenarios with different expected outcomes.

## Suggested Page Object structure

```python
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "/login"

    INPUT_USERNAME = "[data-testid='username']"
    INPUT_PASSWORD = "[data-testid='password']"
    BUTTON_LOGIN = "[data-testid='login-button']"

    def open(self) -> None:
        self.navigate(self.URL)

    def login(self, username: str, password: str) -> None:
        self.fill(self.INPUT_USERNAME, username)
        self.fill(self.INPUT_PASSWORD, password)
        self.click(self.BUTTON_LOGIN)
```

This structure keeps locators close to the behavior they support.

## Locator strategy

Prefer stable and meaningful locators.

Recommended order:

1. `data-testid` or equivalent stable test attributes,
2. accessible roles and names,
3. labels and form semantics,
4. stable text only when the text is part of the business requirement,
5. CSS/XPath as a fallback,
6. generated absolute XPath only as temporary diagnostic output.

Avoid selectors that depend on:

- visual layout,
- generated class names,
- unstable DOM depth,
- random IDs,
- implementation-specific wrappers,
- translated text unless localization is the subject of the test.

## Components

Use `components/` when the same UI fragment appears on multiple pages.

Examples:

- header navigation,
- side menu,
- toast notification,
- modal dialog,
- table component,
- lookup field,
- date picker.

A component should not represent a full user flow. It should represent reusable UI behavior.

## Enterprise UI considerations

Enterprise UIs are often difficult to automate because of:

- dynamic DOM updates,
- delayed rendering,
- custom components,
- nested forms,
- permission-dependent UI,
- iframes,
- client-side validation,
- inconsistent test data,
- slow environments.

For this reason, Page Objects should include stable waits and domain-aware actions, not just raw clicks.

Weak:

```python
self.click("button.save")
```

Better:

```python
def save_case(self) -> None:
    self.click(self.BUTTON_SAVE)
    self.wait_until_case_header_is_visible()
```

## Salesforce-like flow example

A future Salesforce-like case study should be modeled as a Page Object flow, not as raw Playwright code in the test.

Example target flow:

```text
Login
→ open Service area
→ create Case
→ fill required fields
→ save
→ verify case number or confirmation
```

Possible Page Objects:

```text
pages/salesforce_like/
├── login_page.py
├── app_launcher.py
├── case_page.py
└── opportunity_page.py
```

The test should stay readable:

```python
def test_create_case(login_page, app_launcher, case_page):
    login_page.login_as_agent()
    app_launcher.open_service_console()
    case_page.create_case(customer="Acme", subject="Billing issue")

    assert case_page.get_status() == "New"
```

## Codegen usage

Playwright codegen can be useful for discovering selectors.

Generated code should not be pasted directly into tests as final implementation.

Recommended workflow:

1. Use codegen to inspect candidate locators.
2. Move stable locators into a Page Object.
3. Replace raw actions with meaningful methods.
4. Keep assertions in the test.
5. Remove temporary selectors that depend on DOM position.

More details live in `CODEGEN.md`.

## Review checklist

Before accepting a Page Object, ask:

- Does the test avoid raw selectors?
- Are locators stable enough for the application?
- Does the Page Object expose business-readable actions?
- Are assertions kept in tests rather than hidden in the page layer?
- Are waits explicit enough for dynamic UI behavior?
- Can this Page Object be reused in more than one scenario?
- Would a failure message help diagnose what happened?
