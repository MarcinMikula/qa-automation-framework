# Playwright Codegen Guide

Playwright Codegen is a useful helper for discovering selectors and recording
initial browser interactions.

In this framework, Codegen is treated as a **POM helper**, not as a generator
of finished tests.

Generated code should be reviewed, simplified, and moved into Page Objects
before it becomes part of the test suite.

---

## What Codegen is useful for

Codegen can help with:

- quickly discovering available selectors,
- checking how Playwright sees a page,
- recording a rough interaction flow,
- exploring a new screen,
- capturing first-draft UI actions,
- understanding accessible roles and labels,
- speeding up early Page Object creation.

It is especially useful when you are adapting the framework to an unfamiliar
application.

---

## What Codegen is not

Codegen is **not**:

- a replacement for test design,
- a replacement for Page Object Model,
- a source of finished production-ready tests,
- a guarantee of stable selectors,
- a substitute for QA review,
- a tool for deciding what should be automated.

Generated code is a draft.

The QA engineer decides whether the scenario, data, assertions, and selectors
are meaningful.

---

## Basic usage

Run Codegen against an application URL:

```bash
playwright codegen https://your-application.local
```

This opens a browser and a Playwright Inspector window.

As you interact with the page, Playwright generates code for the actions.

For this repository, use generated code only as a starting point for Page
Objects.

---

## Authenticated sessions

Many enterprise applications require authentication before the interesting
flows are reachable.

Playwright Codegen can save and reuse browser storage state.

### Step 1 — record login and save storage

```bash
playwright codegen https://your-application.local --save-storage=auth.json
```

Log in manually in the opened browser.

When the session ends, Playwright saves cookies, local storage, and IndexedDB
state to `auth.json`.

### Step 2 — reuse saved storage

```bash
playwright codegen https://your-application.local/dashboard --load-storage=auth.json
```

This opens the application with the previously saved storage state.

Use this to explore flows behind login without recording the login process every
time.

### Security note

Do not commit real authentication state files.

Add local auth artifacts to `.gitignore`, for example:

```text
auth.json
*.auth.json
playwright/.auth/
```

Storage state may contain sensitive tokens or session cookies.

---

## Recommended workflow in this framework

Use Codegen as a discovery tool, then refactor the result into the framework
structure.

```text
1. Run Codegen against the target screen.
2. Perform the target user flow manually.
3. Copy only useful selectors and actions.
4. Move selectors and actions into a Page Object.
5. Rename methods to business-readable actions.
6. Keep assertions in the test.
7. Review locator stability.
8. Delete raw generated code.
```

The final test should not look like generated code.

The final test should read like a scenario.

---

## Example: generated code vs framework code

### Raw Codegen output

Codegen may generate something like this:

```python
page.locator("[data-testid='username']").fill("agent01")
page.locator("[data-testid='password']").fill("secret")
page.locator("[data-testid='btn-login']").click()
page.locator("[data-testid='customer-search']").fill("48100200301")
page.locator("[data-testid='search-submit']").click()
```

This is useful information, but it should not stay directly in the test.

### Page Object version

Move UI mechanics into Page Objects:

```python
class LoginPage(BasePage):
    USERNAME_INPUT = "[data-testid='username']"
    PASSWORD_INPUT = "[data-testid='password']"
    LOGIN_BUTTON = "[data-testid='btn-login']"

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
```

```python
class DashboardPage(BasePage):
    CUSTOMER_SEARCH_INPUT = "[data-testid='customer-search']"
    SEARCH_BUTTON = "[data-testid='search-submit']"

    def search_customer(self, msisdn: str) -> None:
        self.fill(self.CUSTOMER_SEARCH_INPUT, msisdn)
        self.click(self.SEARCH_BUTTON)
```

### Test version

The test should describe the scenario:

```python
def test_agent_can_search_customer(login_page, dashboard_page):
    login_page.login(username="agent01", password="secret")

    dashboard_page.search_customer(msisdn="48100200301")

    assert dashboard_page.customer_result_visible(msisdn="48100200301")
```

The test does not know selectors.

The Page Objects know selectors.

The scenario remains readable.

---

## Locator review checklist

Before accepting a locator from Codegen, ask:

- Is this selector stable?
- Does it depend on CSS layout?
- Does it depend on generated IDs?
- Does it depend on translated text?
- Does it use a role or label that reflects user-facing meaning?
- Is there a `data-testid` or similar stable test hook?
- Would this selector survive a UI refactor?

Recommended locator priority:

```text
1. Stable test IDs where available
2. Accessible roles and names
3. Labels and visible form semantics
4. Stable CSS attributes
5. XPath only as a last resort
```

Generated selectors often work once.

Framework selectors must survive change.

---

## Assertions generated by Codegen

Codegen may suggest assertions or recorded checks.

Treat them as prompts, not final decisions.

Before keeping an assertion, ask:

- What behavior does it verify?
- Would this fail if the business rule were broken?
- Is this the right test level?
- Is the expected value stable?
- Would the failure help diagnose the issue?

Avoid assertions that only check implementation details.

Prefer assertions that verify meaningful user-visible or business-relevant
outcomes.

---

## Salesforce-like and heavy SPA applications

For large enterprise SPAs, Codegen is useful but risky.

Applications such as Salesforce-like CRMs may include:

- dynamic DOM structure,
- generated IDs,
- delayed rendering,
- modals and overlays,
- tabs,
- iframes,
- Shadow DOM-like boundaries,
- role-dependent UI,
- changing labels,
- hidden validation logic.

In this kind of application, do not trust generated selectors blindly.

Use Codegen to explore the UI, then manually stabilize the Page Object.

Good Page Object methods should describe business actions:

```python
case_page.create_case(...)
case_page.assign_case(...)
case_page.mark_status_as_complete(...)
opportunity_page.create_opportunity(...)
```

The messy UI details should stay inside the Page Object.

---

## What belongs in Page Objects

Move these from generated code into Page Objects:

- locators,
- UI actions,
- page-specific waits,
- navigation helpers,
- small read methods for visible state.

Example:

```python
def success_message_visible(self) -> bool:
    return self.is_visible(self.SUCCESS_MESSAGE)
```

Page Objects may expose state to the test.

They should not silently decide the business outcome of the scenario.

---

## What belongs in tests

Keep these in tests:

- scenario structure,
- test data choice,
- expected business result,
- assertions,
- reason why the flow matters.

Example:

```python
def test_created_case_has_new_status(case_page):
    case_page.create_case(subject="Billing issue", priority="High")

    assert case_page.current_status() == "New"
```

The test owns the expectation.

The Page Object owns the mechanics.

---

## What not to commit

Do not commit:

- raw Codegen recordings,
- temporary generated scripts,
- real credentials,
- saved authenticated storage,
- private URLs,
- copied corporate selectors from protected systems,
- screenshots or traces containing sensitive data.

Codegen often captures real UI details.

Review before committing.

---

## Suggested local scratch area

If you want to keep temporary generated files during exploration, use a local
scratch directory that is ignored by Git:

```text
scratch/
tmp/
playwright/.auth/
```

Example `.gitignore` entries:

```text
scratch/
tmp/
auth.json
*.auth.json
playwright/.auth/
```

Only commit reviewed Page Objects and tests.

---

## Relationship to SOM

Codegen is only relevant to UI automation.

It helps with the POM layer:

```text
pages/
components/
tests/e2e/
```

It does not help design Service Objects.

For API automation, use:

```text
api/
tests/integration/
```

If API code is generated from OpenAPI or Swagger, treat that as a separate
Service Object scaffolding topic, not Playwright Codegen.

---

## Practical rule

Use Codegen to answer:

> How can Playwright interact with this screen?

Do not use Codegen to answer:

> What should this test verify?

That second question belongs to test design and QA judgment.
