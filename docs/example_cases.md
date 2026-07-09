# Example cases

This document describes the example cases used or planned for the framework.

The goal of example cases is not to simulate a full enterprise platform. The goal is to show how the skeleton should be used in realistic testing situations.

## Current example implementation

The repository currently uses a small local example implementation to make the framework executable.

### Local FastAPI microservices

Purpose:

- demonstrate Service Object Model,
- provide deterministic integration tests,
- avoid dependence on private environments,
- keep CI safe and repeatable.

Example domains:

```text
users
orders
products
```

These services are replaceable. They are not the framework core.

### Existing test levels

```text
tests/unit/          model, seed data, and constraint examples
tests/integration/   API tests through Service Objects
tests/e2e/           browser tests through Page Objects
```

The current examples prove the skeleton can run. They do not claim to represent a complete production system.

## Planned POM case study — Salesforce-like UI flow

The planned POM case study should demonstrate a realistic enterprise UI flow without depending on private company data.

Recommended flow:

```text
Login
→ open Sales or Service area
→ create Case or Opportunity
→ fill required fields
→ save
→ verify confirmation, status, or generated record identifier
```

### Why this case matters

A Salesforce-like flow is useful because it represents common enterprise UI automation challenges:

- multi-step forms,
- dynamic rendering,
- required fields,
- role-specific navigation,
- saved record confirmation,
- business object lifecycle.

### Recommended Page Objects

```text
pages/salesforce_like/
├── login_page.py
├── app_launcher_page.py
├── case_page.py
└── opportunity_page.py
```

### Example test shape

```python
def test_create_case(login_page, app_launcher_page, case_page):
    login_page.login_as_service_agent()
    app_launcher_page.open_service_area()
    case_page.create_case(
        customer="Acme Corp",
        subject="Billing issue",
        priority="Medium",
    )

    assert case_page.get_status() == "New"
```

### What this case should not do

The case study should not:

- use real company data,
- require production Salesforce access,
- hardcode private credentials,
- pretend to be a complete Salesforce framework,
- cover every field and permutation,
- bypass test design with raw generated Playwright code.

### Acceptance criteria

The case study is good enough when:

- the test reads like a business scenario,
- selectors are hidden in Page Objects,
- credentials come from configuration,
- assertions are meaningful,
- the flow can be adapted to a real CRM with manual locator replacement,
- limitations are documented.

## Planned SOM case study — API / microservice flow

The planned SOM case study should demonstrate a realistic API workflow through Service Objects.

Recommended flow:

```text
Create customer
→ create order
→ verify order status
→ fetch related customer data
→ validate response contract
```

This can be implemented against local demo services or a safe public API.

### Why this case matters

It demonstrates that the framework is not UI-only.

It shows how to:

- model service operations,
- keep tests away from raw HTTP details,
- validate responses,
- manage test data,
- keep integration tests CI-safe.

### Recommended Service Objects

```text
api/
├── customer_service.py
├── order_service.py
└── product_service.py
```

### Example test shape

```python
def test_create_order_for_existing_customer(customer_service, order_service, product_service):
    customer = customer_service.create_customer(name="Acme Corp")
    product = product_service.get_available_product()

    order = order_service.create_order(
        customer_id=customer.id,
        product_id=product.id,
    )

    assert order.status == "CREATED"
```

### Acceptance criteria

The case study is good enough when:

- tests use Service Objects rather than raw HTTP calls,
- data setup is deterministic,
- negative scenarios are included,
- external dependencies are marked if used,
- CI remains safe by default,
- response validation covers both status and meaningful fields.

## External APIs

Public APIs can be useful for demonstration, but they introduce risk:

- network instability,
- rate limits,
- changing behavior,
- unavailable endpoints,
- data cleanup limitations.

If a public API is used, tests should be marked as external:

```python
@pytest.mark.external
```

Default CI should not depend on external APIs.

## Recommended order of implementation

1. Keep the existing local demo services as CI-safe examples.
2. Add a clearer SOM flow using the local services.
3. Add a Salesforce-like POM case study as a documented skeleton.
4. Optionally add external live tests behind an explicit marker.
5. Update `known_limitations.md` when a case is intentionally incomplete.

## Case study principle

A good case study proves the architecture.

It does not need to pretend that a public repository can fully model a private enterprise platform.
