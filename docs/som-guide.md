# SOM guide

Service Object Model is the API adapter layer of the framework.

Its purpose is to hide HTTP mechanics from tests and expose meaningful service
operations.

---

## Responsibility of a Service Object

A Service Object should know:

- endpoints,
- HTTP methods,
- request payloads,
- headers,
- authentication,
- status-code expectations,
- response parsing,
- service-specific error handling.

It should expose business operations:

```python
customer_service.get_customer_by_msisdn(msisdn)
customer_service.change_plan(customer_id, new_plan)
order_service.create_order(customer_id, product_id)
billing_service.get_invoice_status(invoice_id)
```

---

## Responsibility of a test

A test should know:

- the API behavior being verified,
- the input data,
- the expected outcome,
- the business risk.

It should not repeatedly build raw URLs, headers, and payloads.

---

## Weak vs strong Service Objects

Weak:

```python
response = api_client.post("/customers/123/change-plan", json={"plan": "premium"})
assert response.status_code == 200
```

Stronger:

```python
customer_service.change_plan(customer_id=123, new_plan="premium")
customer = customer_service.get_customer(customer_id=123)

assert customer["plan"] == "premium"
```

The second version communicates intent.

---

## Base client role

The base client should hold shared mechanics:

- base URL,
- timeout,
- default headers,
- authentication token,
- low-level `get`, `post`, `put`, `patch`, `delete`,
- common error handling.

Service Objects should build on top of it.

Tests should use Service Objects directly.

---

## Generated Service Objects

Generated code can be useful when OpenAPI/Swagger exists.

But generated code should be reviewed for:

- readable method names,
- correct endpoint mapping,
- business meaning,
- payload correctness,
- authentication,
- error handling,
- useful assertions.

Generated code is scaffolding.

It is not finished test design.
