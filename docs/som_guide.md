# Service Object Model guide

Service Object Model is the API and integration layer of this framework.

Its purpose is to keep HTTP mechanics out of tests.

A test should describe the business operation. A Service Object should know how to call the API.

## Scope

Use SOM for:

- REST API tests,
- integration tests,
- service boundary checks,
- contract-level assumptions,
- backend workflows,
- setup operations that are safer through API than UI.

Do not use SOM for:

- browser UI flows,
- CSS selector handling,
- visual checks,
- page navigation,
- raw database assertions unless explicitly part of the test design.

## Basic rule

Tests should not build raw URLs or payloads repeatedly.

Weak test:

```python
response = client.post(
    "/customers/123/change-plan",
    json={"plan": "premium"},
    headers={"Authorization": f"Bearer {token}"},
)
assert response.status_code == 200
```

Better test:

```python
customer_service.change_plan(customer_id=123, new_plan="premium")
```

The first version exposes HTTP mechanics. The second version expresses domain intent.

## Responsibility split

### Base client responsibilities

`api/base_client.py` should own low-level HTTP mechanics such as:

- base URL,
- common headers,
- authentication token handling,
- timeout configuration,
- common `get`, `post`, `put`, `patch`, `delete` wrappers,
- shared response handling helpers.

### Service Object responsibilities

A Service Object should own one API domain or service boundary.

Examples:

```text
customer_service.py
order_service.py
product_service.py
case_service.py
billing_service.py
```

Service Objects should expose meaningful operations:

```python
customer_service.get_customer_by_msisdn(msisdn)
order_service.create_order(customer_id, product_id)
billing_service.get_invoice_status(invoice_id)
case_service.create_case(customer_id, subject)
```

### Test responsibilities

A test should own:

- scenario selection,
- input data,
- expected behavior,
- assertions,
- failure interpretation.

## Suggested Service Object structure

```python
from api.base_client import BaseClient


class CustomerService(BaseClient):
    def get_customer_by_msisdn(self, msisdn: str):
        return self.get(f"/customers/msisdn/{msisdn}")

    def change_plan(self, customer_id: int, new_plan: str):
        payload = {"plan": new_plan}
        return self.post(f"/customers/{customer_id}/change-plan", json=payload)
```

This keeps endpoint details out of tests.

## Domain methods vs generic methods

A Service Object should not be just a renamed HTTP client.

Weak:

```python
user_service.get("/users")
user_service.post("/users", json=data)
```

Better:

```python
user_service.list_users()
user_service.create_user(name="Alice", email="alice@example.com")
```

The test should read as a business action, not as transport-layer plumbing.

## Response validation

There are two useful levels of response validation.

### Technical validation

Examples:

- HTTP status code,
- response is valid JSON,
- required fields exist,
- schema matches expected shape,
- response time is within an agreed threshold.

### Business validation

Examples:

- newly created order has status `CREATED`,
- suspended account cannot place an order,
- invoice belongs to the requested customer,
- case is assigned to the correct queue,
- product cannot be ordered when inactive.

Technical validation proves the API responded.

Business validation proves the behavior matters.

## Where to put assertions

For simple reusable expectations, a Service Object may expose helper methods:

```python
def assert_customer_exists(self, customer_id: int) -> None:
    response = self.get_customer(customer_id)
    assert response.status_code == 200
```

However, business-specific assertions usually belong in tests.

This keeps Service Objects reusable across positive, negative, and edge-case scenarios.

## Authentication

Authentication should be handled outside individual tests when possible.

Recommended places:

- environment variables,
- settings module,
- pytest fixtures,
- BaseClient initialization,
- token provider helper.

Avoid hardcoding credentials in:

- tests,
- Service Objects,
- example payloads,
- documentation snippets that look real.

## Test data and idempotency

API tests should be repeatable.

Prefer:

- deterministic seed data,
- unique test identifiers,
- cleanup fixtures,
- isolated test accounts,
- local demo services for CI.

Be careful with:

- assuming database IDs start from `1`,
- relying on manually prepared state,
- using shared mutable data across tests,
- creating data without cleanup in live environments.

## Public API case study

A future public or local API case study should demonstrate SOM through a realistic flow:

```text
Create customer
→ create order
→ verify order status
→ fetch related customer data
→ validate response contract
```

The goal is to show how tests use Service Objects, not to test a third-party API as a product.

## Swagger/OpenAPI generation

Generated Service Objects can speed up initial scaffolding.

Generated code should be reviewed before it becomes framework code.

Review generated methods for:

- meaningful names,
- correct endpoint paths,
- request payload shape,
- response expectations,
- authentication requirements,
- error cases,
- domain meaning.

Generated code is a starting point. It is not test design.

## Review checklist

Before accepting a Service Object, ask:

- Does the test avoid raw URLs and repeated payload construction?
- Does the method name describe a business operation?
- Is authentication handled consistently?
- Are response expectations clear?
- Is test data deterministic or explicitly external?
- Is the service boundary clear?
- Would a failure help diagnose a contract or business behavior change?
