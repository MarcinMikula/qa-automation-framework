# Architecture

`qa-automation-framework` is a reusable QA automation framework skeleton for enterprise-style UI and API testing.

It is not a finished test suite for a specific application. It provides structure, conventions, and example implementation patterns that can be adapted to a real project.

## Core idea

The framework is built around two complementary automation patterns:

- **Page Object Model (POM)** for UI and browser-based E2E testing.
- **Service Object Model (SOM)** for API, integration, and microservice testing.

The two patterns live in one repository because real enterprise systems often require both layers.

They are not merged into one abstraction. They are separate adapter layers that share configuration, fixtures, test data conventions, and reporting.

```text
                 tests/
        ┌──────────┴──────────┐
        │                     │
   tests/e2e/           tests/integration/
        │                     │
        ▼                     ▼
     pages/                 api/
   POM layer              SOM layer
        │                     │
        ▼                     ▼
  browser / UI          HTTP / services
```

## Framework core vs example implementation

The repository contains two categories of code.

### Reusable framework core

These parts are intended to survive adaptation to a real project:

```text
pages/        Page Object Model layer
components/   reusable UI component abstractions
api/          Service Object Model layer
testdata/     deterministic test data and settings
mocks/        mocked responses and isolated inputs
tests/        unit, integration, and E2E test structure
.github/      CI workflow
```

### Replaceable example implementation

These parts exist to make the skeleton executable and reviewable:

```text
services/     local FastAPI demo services
tests/unit/   example model and data tests
tests/integration/
              example API tests through Service Objects
tests/e2e/    example browser tests through Page Objects
```

The example implementation should be treated as a sandbox. In a real project, it can be removed or replaced with the actual application under test.

## Layer responsibilities

### Tests

Tests describe scenarios and expected behavior.

Tests should avoid direct low-level interaction with CSS selectors, raw URLs, HTTP headers, and implementation details.

A good test reads like a business scenario:

```python
case_page.create_case(customer="Acme", subject="Billing problem")
case_page.expect_case_created()
```

or:

```python
order_service.create_order(customer_id=customer.id, product_id=product.id)
order_service.expect_order_status(order_id, "CREATED")
```

### Page Objects

Page Objects know how to interact with a specific page, view, form, or screen.

They own:

- locators,
- UI actions,
- page-specific waits,
- navigation details,
- small UI queries needed by tests.

They should not own broad test intent or business-level assertions.

### Components

Components model reusable pieces of UI that appear across multiple pages.

Examples:

- navigation bar,
- modal dialog,
- toast notification,
- search component,
- data table,
- date picker.

A component should be extracted when the same UI behavior appears in more than one Page Object.

### Service Objects

Service Objects know how to interact with a specific API domain or service boundary.

They own:

- endpoint paths,
- request payload construction,
- HTTP method selection,
- status-code expectations,
- response parsing,
- domain-specific API operations.

They should expose business operations, not generic HTTP mechanics.

Good:

```python
customer_service.get_customer_by_msisdn(msisdn)
customer_service.change_plan(customer_id, new_plan="premium")
```

Weak:

```python
client.get("/customers/123")
client.post("/customers/123/change-plan", json={...})
```

The raw HTTP methods belong in the base client. Tests should use domain-level methods.

### Test data

The test data layer provides deterministic, repeatable data for tests.

It should help answer:

- What data does the test need?
- Where does the data come from?
- Can this test be repeated safely?
- Does this data represent a realistic business scenario?

### Mocks

Mocks isolate tests from dependencies that are unstable, unavailable, too slow, or outside the current test scope.

Mocks should be used intentionally. They are useful for isolation, but they do not replace integration testing against real contracts.

### Example services

The local FastAPI services are not the product being tested.

They exist to demonstrate:

- service boundaries,
- integration tests,
- Service Object usage,
- deterministic local execution,
- CI-safe behavior.

## UI / E2E flow

A browser test should normally follow this path:

```text
test
  → Page Object
  → BasePage / Playwright
  → browser
  → application UI
```

The test should express intent. The Page Object should know the mechanics.

## API / integration flow

An API test should normally follow this path:

```text
test
  → Service Object
  → BaseClient / httpx
  → API endpoint
  → response validation
```

The test should express the business operation. The Service Object should know the endpoint and payload details.

## What belongs where

| Need | Place |
|---|---|
| Browser action on one page | `pages/` |
| Reusable UI widget | `components/` |
| API business operation | `api/` |
| Raw HTTP method wrapper | `api/base_client.py` |
| Environment setting | `testdata/settings.py` or env var |
| Deterministic seed data | `testdata/` |
| Mocked response | `mocks/` |
| Pure logic test | `tests/unit/` |
| API/service test | `tests/integration/` |
| Browser flow test | `tests/e2e/` |

## Design decisions

### AD-001 — The repository is a framework skeleton

The repository is intentionally not a complete automation product.

A public skeleton cannot know a private enterprise application's workflows, selectors, endpoint contracts, authentication, data lifecycle, or business rules.

The skeleton provides structure. The project team provides context.

### AD-002 — POM and SOM live together but stay separate

POM and SOM are both included because real systems often need UI and API test layers.

They share test infrastructure but do not share responsibilities.

POM models screens and user actions. SOM models API operations and service behavior.

### AD-003 — Local services are examples, not framework core

The `services/` directory exists to make the project executable without access to a private enterprise system.

It should be treated as a replaceable demo sandbox.

### AD-004 — CI should run deterministic tests by default

Default CI should avoid private environments, live third-party dependencies, and unstable external services.

External or environment-dependent tests should be opt-in.

### AD-005 — Generated code is a starting point, not architecture

Codegen and AI-assisted generation can speed up development, but generated code must be reviewed and shaped into the framework's patterns.

Generated raw HTTP calls should become Service Objects.

Generated Playwright interactions should become Page Objects.

## Extension points

The framework can be extended by adding:

- new Page Objects in `pages/`,
- new reusable UI components in `components/`,
- new Service Objects in `api/`,
- new domain data models in `testdata/`,
- new isolated responses in `mocks/`,
- new pytest fixtures,
- new markers for external or environment-specific tests,
- new reporting hooks.

Extensions should preserve the boundary between test intent and implementation mechanics.

## Related documents

- [pom_guide.md](pom_guide.md)
- [som_guide.md](som_guide.md)
- [adaptation_guide.md](adaptation_guide.md)
- [test_strategy.md](test_strategy.md)
- [known_limitations.md](known_limitations.md)
