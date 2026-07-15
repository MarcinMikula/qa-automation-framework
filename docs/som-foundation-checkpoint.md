# SOM foundation checkpoint

This document records the current Service Object Model foundation status.

It is a checkpoint, not a new demo-service roadmap.

---

## Status

The SOM foundation is mostly in place, but its main client boundary must stay
explicit.

Implemented framework pieces:

```text
BaseClient
MicroserviceClient
Concrete Service Objects
Pydantic request/response models
Service-level integration tests
Multi-service workflow test
Swagger/OpenAPI generator helper
Tests owning assertions
```

Current concrete examples:

```text
UserService
ProductService
OrderService
```

Current workflow example:

```text
customer
→ product
→ order
→ order status change
```

The purpose of these examples is to prove the framework structure, not to grow
a fake microservice platform.

---

## What is now covered

The framework now has:

- a generic `BaseClient`,
- a convenience `MicroserviceClient`,
- Service Objects for users, products, and orders,
- typed Pydantic models for service payloads,
- unit tests for reusable SOM helpers,
- integration tests for concrete Service Objects,
- a first multi-service SOM workflow,
- Swagger/OpenAPI generator behavior tests,
- documentation for SOM usage.

This is enough to demonstrate the core SOM pattern.

---

## SOM responsibility split

The intended responsibility split is:

```text
BaseClient / MicroserviceClient
→ reusable HTTP mechanics

Concrete Service Objects
→ application-facing service actions and state

Pydantic models
→ request/response structure and validation

Tests
→ business assertions
```

The test should not repeatedly build raw URLs, headers, HTTP calls, and payloads
when a Service Object can express the operation in business-readable language.

Preferred test style:

```python
order = order_service.create_order(customer_id=customer.id, product_id=product.id)

assert order.status == "NEW"
```

Avoid test style:

```python
response = httpx.post("http://localhost:8003/orders", json={...})
assert response.json()["status"] == "NEW"
```

---

## BaseClient vs MicroserviceClient

The repository currently has two HTTP helper classes.

They serve different purposes.

This distinction should remain explicit because otherwise users may not know
which one to use.

---

## BaseClient

`BaseClient` is the generic low-level HTTP foundation for Service Objects.

It returns raw `httpx.Response` objects.

Use it when the Service Object needs control over:

- status codes,
- response headers,
- raw response body,
- provider-specific behavior,
- redirects,
- rate limits,
- correlation IDs,
- idempotency keys,
- unusual success responses,
- non-JSON responses,
- generated Service Objects.

Mental model:

```text
BaseClient
= give me the raw response; the Service Object decides what it means
```

Example e-commerce use cases:

```text
PaymentService
ExternalTaxService
ShippingProviderService
SalesforceRestService
OAuthService
PublicApiClient
```

Example:

```python
class PaymentService:
    def __init__(self):
        self.client = BaseClient(
            base_url="https://payment-provider.example",
            token="secret-token",
        )

    def authorize_payment(self, payload: dict):
        return self.client.post("/payments/authorize", payload)
```

A test or higher-level Service Object may then check:

```python
response = payment_service.authorize_payment(payment_data)

assert response.status_code == 202
assert "Location" in response.headers
```

This is useful because payment, OAuth, shipping, tax, and external-provider APIs
often encode important behavior in status codes and headers, not only in JSON
body fields.

---

## MicroserviceClient

`MicroserviceClient` is a convenience client for simple local JSON
microservices.

It parses successful JSON responses and raises for HTTP errors.

Use it when the Service Object works with predictable JSON APIs and the test
does not need direct access to the raw `httpx.Response`.

Mental model:

```text
MicroserviceClient
= give me parsed JSON or fail fast
```

Example e-commerce use cases:

```text
CatalogService
CartService
OrderService
InventoryService
UserService
ProductService
```

Example:

```python
class CatalogService:
    def __init__(self):
        self.client = MicroserviceClient("http://localhost:8001")

    def get_product(self, product_id: int):
        return self.client.get(f"/products/{product_id}")
```

A test can then remain business-readable:

```python
product = catalog_service.get_product(123)

assert product["name"] == "Samsung 65 OLED"
```

This is useful for deterministic local examples and simple internal
microservices where most successful responses are JSON and HTTP errors should
fail the test immediately.

---

## Quick decision guide

Use `MicroserviceClient` when:

```text
API is simple
API returns JSON
you want dict/list/None
HTTP errors should fail immediately
you do not need headers or raw status handling
the service is local, deterministic, or CRUD-like
```

Use `BaseClient` when:

```text
you need raw httpx.Response
you verify status codes
you verify headers
you handle 202, 204, 409, 422, 429, redirects, or polling
you need provider-specific behavior
you use advanced auth, correlation, or idempotency
the API is external, generated, or not simple JSON CRUD
```

Simple e-commerce mapping:

```text
CatalogService       → MicroserviceClient
CartService          → MicroserviceClient
OrderService         → MicroserviceClient or BaseClient, depending on complexity
InventoryService     → MicroserviceClient
PaymentService       → BaseClient
ShippingProvider     → BaseClient
ExternalTaxService   → BaseClient
OAuthService         → BaseClient
SalesforceRestService→ BaseClient
```

---

## Important rule

Tests should normally not use either client directly.

Preferred flow:

```text
Test
→ Service Object
→ BaseClient or MicroserviceClient
→ API
```

This keeps tests readable and keeps HTTP mechanics out of test bodies.

Good:

```python
order = order_service.create_order(customer_id, product_id)

assert order.status == "NEW"
```

Less desirable:

```python
response = client.post("/orders", payload)
assert response.status_code == 201
```

The second style may be acceptable in low-level client tests, but not as the
default style for business-facing integration tests.

---

## What should not be added now

Do not add more demo microservices just to make the local example look richer.

Avoid adding demo services such as:

```text
PaymentService
InventoryService
PromoService
BillingService
NotificationService
ShippingService
TaxService
ReviewService
```

unless they are required by a real project-context adaptation later.

Adding them now would shift the project toward building a fake microservice
platform.

That is not the goal.

---

## Why we stop here

The framework should stay:

- simple,
- reusable,
- readable,
- aligned with POM,
- aligned with SOM,
- aligned with good automation principles,
- helpful for an automation tester,
- ready to be filled with project-specific context.

The repository should not become:

```text
mini e-commerce platform
mini telco backend
mini Salesforce
mini ERP
mini CRM
```

The demo services exist only to exercise the framework.

They must not become the framework.

---

## What comes later

Further Service Objects should be created during application-context adaptation.

Examples:

```text
E-commerce validation:
- CatalogService
- CartService
- OrderService
- PaymentService
- InventoryService
- PromoService

Salesforce / CRM-style validation:
- AccountService
- OpportunityService
- CaseService
- ContactService

External-provider validation:
- PaymentProviderService
- ShippingProviderService
- TaxProviderService
```

Those should be created only when validating the framework against a real or
realistic application.

They are not part of the current framework-core build phase.

---

## Current conclusion

The SOM foundation is good enough for the current stage if the
`BaseClient`/`MicroserviceClient` distinction remains documented.

Next SOM work should not expand the demo backend.

Useful next directions:

- clarify adaptation workflow,
- document manual and AI-assisted filling later,
- prepare framework UAT plan,
- revisit whether `MicroserviceClient` should remain example-specific or become
  part of the documented public skeleton.
