# Automation Principles

Evergreen testing principles extracted before rewriting the project-specific documentation.

This file is intentionally broader than this repository. It captures the automation rules that
should remain useful across different frameworks, projects, tools, and domains.

The framework may change. These principles should change only when the testing thinking behind
them changes.

---

## 1. A test must explain the behavior it protects

A useful automated test does more than execute code or click through a screen.

It should make clear:

- what behavior is being verified,
- why that behavior matters,
- what kind of failure it would expose,
- what business or user outcome is at risk.

A test that fails without explaining what broke is expensive to diagnose.

A test that passes without protecting meaningful behavior is noise.

Good tests help the reader understand the system before debugging starts.

---

## 2. Tests should speak business language, not implementation details

Tests should describe scenarios in terms of domain actions and outcomes.

Good examples:

```python
dashboard.search_customer(msisdn="48100200301")
customer_service.suspend_account(customer_id)
order_service.create_order(customer_id, product_id)
```

Weak examples:

```python
page.locator("#btn-123").click()
client.post("/internal/api/v1/x/y/z")
```

Selectors, URLs, headers, payload construction, and low-level protocol details belong in framework
layers.

The test should describe the scenario.

---

## 3. Page Objects model user interactions

A Page Object should hide UI mechanics from the test.

It should know:

- locators,
- page-specific actions,
- UI waits,
- navigation details,
- stable ways to interact with the screen.

It should expose meaningful user actions:

```python
login_page.login(username, password)
case_page.create_case(subject, priority)
dashboard.search_customer(msisdn)
```

The test should not know how those actions are implemented.

A Page Object is not valuable because it stores selectors.

It is valuable because it turns UI mechanics into readable test language.

---

## 4. Page Objects should not own business assertions

A Page Object may expose state or helper methods that make assertions easier.

But the test should decide what matters.

Good:

```python
login_page.login("admin", "secret")

assert dashboard.is_loaded()
assert dashboard.current_user_name() == "Admin User"
```

Risky:

```python
login_page.login_and_assert_success("admin", "secret")
```

Why?

Because business intent belongs to the scenario.

A Page Object should help the test observe the application, not silently decide which outcome is
important.

---

## 5. Service Objects model business operations, not raw HTTP calls

A Service Object should hide API mechanics from the test.

It should know:

- base URLs,
- endpoints,
- headers,
- authentication,
- payload shape,
- status-code handling,
- response parsing.

It should expose meaningful operations:

```python
customer_service.get_customer_by_msisdn(msisdn)
customer_service.change_plan(customer_id, new_plan)
billing_service.get_invoice_status(invoice_id)
case_service.create_case(customer_id, subject)
```

Weak Service Objects are only wrappers around `get()` and `post()`.

Good Service Objects express domain behavior.

The lower-level HTTP client belongs underneath the Service Object, not in every test.

---

## 6. Configuration must not be hardcoded in tests

A framework should support multiple environments without changing test logic.

Examples:

- DEV,
- SIT,
- UAT,
- staging,
- local,
- production-like environments.

Environment-specific values should live in configuration, settings, or environment variables.

Tests should not hardcode:

- base URLs,
- credentials,
- tokens,
- environment names,
- browser settings,
- API hosts.

A test should say what it verifies.

Configuration should decide where it runs.

---

## 7. Test data must be controlled, explicit, and explainable

Test data is part of the test design.

It should be clear:

- where the data comes from,
- whether it is seeded, mocked, generated, or pre-existing,
- which scenario it supports,
- whether tests can safely modify it,
- whether it is isolated from other tests.

Random or manually prepared data creates hidden dependencies.

Deterministic data makes failures easier to reproduce.

A test that depends on unknown state is not a reliable test.

---

## 8. State is a first-class part of automation design

Automated tests do not run in a vacuum.

They depend on state:

- database records,
- users,
- permissions,
- orders,
- accounts,
- contracts,
- API tokens,
- feature flags,
- environment configuration.

A framework must make state visible and manageable.

Good automation answers:

- What state does this test need?
- Who creates that state?
- Who cleans it up?
- Can another test affect it?
- Can the test be repeated safely?

State that is not controlled becomes flakiness.

---

## 9. Fixtures should reduce noise, not hide meaning

Fixtures are useful when they remove repetitive setup.

They become dangerous when they hide important scenario context.

Good fixtures:

- create known users,
- prepare isolated data,
- configure clients,
- start local services,
- provide readable setup.

Risky fixtures:

- silently mutate shared state,
- hide business-critical assumptions,
- do too much behind the test,
- make the test impossible to understand without jumping across files.

A fixture should make the test cleaner, not mysterious.

---

## 10. Unit tests are contracts for small behavior

A unit test is a contract.

It says:

> this function, method, model, or rule behaves exactly like this under these conditions.

When the implementation changes and breaks that contract, the test should fail early.

Before accepting a unit test, understand:

- what code is being tested,
- what responsibility that code has,
- what input data it receives,
- what output or side effect is expected,
- what edge case is being protected.

A unit test that does not protect a real rule is just executable noise.

---

## 11. API and integration tests protect contracts between layers

API and integration tests should verify boundaries.

They are useful for checking:

- HTTP status codes,
- response shape,
- required fields,
- error handling,
- authentication behavior,
- service-to-service assumptions,
- backward compatibility of contracts.

They should not blindly duplicate unit tests.

They should answer:

> Can this layer still communicate correctly with the next one?

When an API test fails, it should point toward a broken contract, not just a random
implementation detail.

---

## 12. E2E tests should be few, critical, and business-relevant

End-to-end tests are valuable but expensive.

They are usually:

- slower,
- more fragile,
- harder to isolate,
- harder to debug,
- more dependent on environment stability.

Use them for critical user journeys, not every small rule.

Good E2E candidates:

- login and access,
- create a case,
- create an opportunity,
- place an order,
- submit a form,
- complete a payment-like flow,
- verify a critical status transition.

If a scenario can be reliably tested at unit or API level, it usually should be.

---

## 13. The test pyramid is a maintenance strategy

A healthy automation suite usually has:

```text
        E2E / UI
      few, critical flows

    API / integration
   contracts and services

        Unit
 small rules and logic
```

The higher the test is in the pyramid, the more expensive it is to run and maintain.

The lower the test is in the pyramid, the faster and more isolated it should be.

Use the right layer for the risk being tested.

Do not use E2E tests to compensate for missing lower-level tests.

---

## 14. A passing test is not automatically a valuable test

A test can be technically correct and still useless.

Warning signs:

- it has no meaningful assertion,
- it only checks that code executes,
- it verifies implementation details instead of behavior,
- it would pass even if the business rule were broken,
- nobody can explain what risk it protects,
- failure would not help diagnose a real problem.

A valuable test protects behavior that matters.

---

## 15. A failing test should provide diagnostic value

A good failure should help answer:

- what behavior failed,
- where the failure happened,
- what data was used,
- what expected result was not met,
- whether the problem is likely in UI, API, data, environment, or test code.

Automation is not only about detecting failure.

It is also about shortening the path from failure to diagnosis.

---

## 16. Flakiness is usually a design signal

A flaky test should not be ignored.

Flakiness often points to one of these problems:

- uncontrolled state,
- weak synchronization,
- unstable selectors,
- shared data,
- hidden test dependencies,
- environment instability,
- overuse of E2E testing,
- unclear ownership of setup and cleanup.

Retrying can reduce noise, but it does not explain the cause.

A flaky test deserves investigation.

---

## 17. Mocks isolate risk, but they must be honest

Mocks are useful when they isolate tests from unstable or expensive dependencies.

They can help verify:

- edge cases,
- error responses,
- contract assumptions,
- timeout handling,
- unavailable downstream systems.

But mocks must stay close to reality.

A mock that does not reflect real behavior creates false confidence.

Use mocks to isolate risk, not to invent a better system than the one you have.

---

## 18. Names are part of test design

Names should communicate intent.

Good test names describe:

- condition,
- action,
- expected result.

Example:

```python
def test_suspend_active_customer_changes_status_to_suspended():
    ...
```

Weak names hide the scenario:

```python
def test_customer_1():
    ...
```

A reader should understand the purpose of the test before reading the body.

If the name is hard to write, the scenario may not be clear enough yet.

---

## 19. AI can generate a skeleton, but QA owns the meaning

AI can help write:

- initial Page Objects,
- Service Object methods,
- test skeletons,
- fixtures,
- mock data,
- edge-case suggestions,
- refactoring proposals.

But AI does not automatically know:

- business priority,
- production risk,
- domain exceptions,
- environment constraints,
- which assertion matters,
- whether test data is realistic,
- whether a scenario is worth automating.

AI output is a starting point.

QA review turns it into useful automation.

---

## 20. Do not accept generated tests you cannot explain

Before accepting an AI-generated test, be able to answer:

- What behavior does this test verify?
- What input data does it use?
- What is the expected result?
- Why is this assertion meaningful?
- What production risk does this test reduce?
- What would this failure tell us?
- Is this the right test layer?

If you cannot explain the test, do not merge it.

---

## 21. Framework code should make good tests easier to write

A framework should reduce repetitive mechanics and encourage better structure.

It should make it easy to:

- express domain actions,
- reuse stable setup,
- manage data,
- separate UI from API logic,
- run tests by level,
- debug failures,
- configure environments safely.

A framework should not hide so much that tests become unreadable.

Good framework design supports QA thinking instead of replacing it.

---

## 22. Automation supports testing; it is not the whole testing strategy

Automation is one part of quality engineering.

It does not replace:

- exploratory testing,
- risk analysis,
- test design,
- domain conversations,
- production incident learning,
- accessibility review,
- usability judgment,
- critical thinking.

Automated tests are strongest when they encode well-understood expectations.

They are weakest when they are used as a substitute for understanding the system.

---

## 23. The best automation is maintainable under change

Enterprise systems change constantly:

- selectors change,
- APIs evolve,
- data rules shift,
- roles and permissions change,
- environments become unstable,
- workflows are redesigned.

A framework should expect change.

Maintainable automation separates:

- test intent from implementation detail,
- domain operations from protocol mechanics,
- environment configuration from test logic,
- reusable setup from scenario-specific data.

The goal is not to avoid change.

The goal is to make change survivable.

---

## 24. Prefer honest limitations over fake completeness

A framework skeleton should clearly say what it does not do yet.

Known limitations are not failures when they are intentional and documented.

They help future readers understand:

- what is complete,
- what is demo-only,
- what needs project-specific adaptation,
- what should not be trusted blindly,
- what is planned for later.

Honest documentation is part of quality.

---

## Summary

Useful automation is not defined by the number of tests.

It is defined by whether the tests:

- protect meaningful behavior,
- run at the right level,
- use controlled data,
- communicate intent,
- fail with diagnostic value,
- remain maintainable under change,
- support real QA thinking.

The goal is not to automate everything.

The goal is to automate the right things in a way that can be understood, trusted, and maintained.
