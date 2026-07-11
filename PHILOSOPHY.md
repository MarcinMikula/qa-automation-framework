# Framework Philosophy

This document explains the testing philosophy behind this repository.

It is intentionally project-specific.

General, evergreen automation principles live in
[`AUTOMATION_PRINCIPLES.md`](AUTOMATION_PRINCIPLES.md). This file focuses on
why this framework skeleton is structured the way it is.

---

## 1. The framework is a skeleton, not a product

This repository is not a ready-made automation product.

It is a reusable structure for building automated tests around real enterprise
systems.

A real project still needs its own:

- application URLs,
- authentication flow,
- UI locators,
- API endpoints,
- test data,
- environment configuration,
- business assertions,
- domain-specific fixtures.

The framework provides the shape.

The project provides the truth.

This distinction matters because enterprise systems cannot be automated
honestly without domain context.

---

## 2. The test should describe intent

The main job of a test is not to show that a tool can click buttons or send
requests.

The main job of a test is to describe behavior worth protecting.

A good test should make the reader understand:

- what scenario is being checked,
- what input data is used,
- what result is expected,
- why the result matters,
- what kind of failure the test would expose.

A test that passes but protects no meaningful behavior is noise.

A test that fails but does not help diagnose the problem is expensive.

The framework is designed to keep tests readable enough that their intent is
visible before debugging starts.

---

## 3. POM and SOM are adapter layers

The repository contains both Page Object Model and Service Object Model because
enterprise systems are rarely tested well through only one layer.

They are not mixed into one abstraction.

They are separate adapters:

```text
pages/   -> UI adapter layer
api/     -> API/service adapter layer
```

The test should not know UI selectors or raw HTTP mechanics.

Instead, it should use project-specific language:

```python
login_page.login(username, password)
dashboard.search_customer(msisdn)
customer_service.change_plan(customer_id, new_plan)
order_service.create_order(customer_id, product_id)
```

POM hides browser interaction details.

SOM hides API interaction details.

The test remains focused on the scenario.

---

## 4. Page Objects model user actions

A Page Object should expose meaningful actions that a user or role can perform.

Examples:

```python
login_page.login(...)
case_page.create_case(...)
opportunity_page.create_opportunity(...)
dashboard.search_customer(...)
```

A Page Object may know selectors, waits, navigation details, and page-specific
mechanics.

A test should not.

The value of POM is not that selectors are stored in another file.

The value of POM is that UI mechanics are translated into readable test
language.

---

## 5. Service Objects model business operations

A Service Object should expose meaningful API operations.

Examples:

```python
customer_service.get_customer_by_msisdn(...)
customer_service.suspend_account(...)
billing_service.get_invoice_status(...)
order_service.create_order(...)
```

A Service Object may know endpoints, headers, payload shape, authentication,
status-code expectations, and response parsing.

A test should not repeat those details.

The value of SOM is not wrapping `get()` and `post()`.

The value of SOM is that API mechanics are translated into domain-level
operations.

---

## 6. Configuration, object model, and state are the core concerns

This framework is built around three practical automation concerns.

### Configuration

Tests should not hardcode environment-specific values.

URLs, credentials, tokens, browser settings, and API hosts belong in
configuration or environment variables.

The same framework should be adaptable to local, DEV, SIT, UAT, staging, or
production-like environments without rewriting test logic.

### Object model

Each system layer should have a clear test-facing model:

- Page Objects for UI screens and flows,
- Service Objects for API and service operations,
- optional component objects for reusable UI fragments,
- fixtures for setup and shared context.

This makes tests easier to read and safer to change.

### State

Test data and environment state are part of the test design.

A test should make it clear:

- what data it needs,
- who creates that data,
- whether the data is isolated,
- whether cleanup is required,
- whether the test can run repeatedly.

Uncontrolled state is one of the most common causes of flaky automation.

---

## 7. The test pyramid guides scope

The framework follows a practical test pyramid:

```text
        E2E / UI
      few, critical flows

    API / integration
   contracts and services

        Unit
 small rules and logic
```

Each layer has a different purpose.

Unit tests should protect small, deterministic behavior.

Integration/API tests should protect contracts and service boundaries.

E2E tests should protect critical user-facing flows.

E2E tests are valuable, but they are also expensive. They should not be used as
a replacement for missing lower-level tests.

---

## 8. The example implementation is replaceable

The repository contains local example services and demo tests so the framework
can be executed and reviewed without access to a private application.

Those examples are not the product.

They exist to demonstrate:

- project structure,
- POM usage,
- SOM usage,
- fixture organization,
- test levels,
- CI-safe execution.

In a real project, the example services may be removed or replaced by the
actual system under test.

This is intentional.

---

## 9. AI can help adaptation, but QA owns correctness

This framework is designed to work well with AI-assisted development.

AI can help generate first drafts of:

- Page Objects,
- Service Objects,
- fixtures,
- test skeletons,
- mock data,
- documentation updates.

But AI does not own the meaning of the test.

A QA engineer still needs to verify:

- whether the scenario matters,
- whether the assertion is meaningful,
- whether the data is realistic,
- whether the locator is stable,
- whether the API operation matches the real contract,
- whether the test belongs at UI, API, or unit level.

AI can speed up scaffolding.

QA review turns scaffolding into useful automation.

---

## 10. Honest limitations are part of the design

A framework skeleton should not pretend to be more complete than it is.

Known limitations are useful when they are explicit.

They tell the reader:

- what is currently implemented,
- what is demo-only,
- what needs project-specific adaptation,
- what should not be trusted blindly,
- what may be added later.

For this repository, detailed boundaries live in:

- [`docs/known-limitations.md`](docs/known-limitations.md),
- [`docs/gaps.md`](docs/gaps.md),
- [`docs/future-ideas.md`](docs/future-ideas.md).

This keeps the project honest and easier to maintain.

---

## Summary

This framework is built around one practical idea:

> Tests should express business intent while the framework hides repetitive
> technical mechanics.

POM hides UI mechanics.

SOM hides API mechanics.

Fixtures and configuration hide repeatable setup.

Test data makes state explicit.

The test itself should remain readable, meaningful, and useful when it fails.

The goal is not to automate everything.

The goal is to make the right tests easier to write, understand, run, and
maintain.
