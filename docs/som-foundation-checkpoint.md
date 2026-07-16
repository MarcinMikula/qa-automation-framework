# SOM foundation checkpoint

This document records the current Service Object Model foundation status.

It is a checkpoint, not a demo-service roadmap.

---

## Status

The SOM foundation is closed for the current framework-core stage.

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
user
→ product
→ order
→ order status change
→ optional external reference
```

The examples prove the SOM structure.

They do not define a complete business domain.

---

## Domain-neutral example contract

The active SOM examples use a small readable vocabulary:

```text
User
Product
Order
```

Neutral does not mean abstract.

The repository does not replace readable business nouns with `Entity`,
`Resource`, or `Object`.

It removes hidden industry assumptions instead.

Current neutral fields include:

```text
User:
- full_name
- external_id
- email
- status

Product:
- name
- sku
- price
- category
- description

Order:
- user_id
- product_id
- quantity
- total_amount
- status
- external_reference
```

A project may interpret or replace these fields during adaptation.

Examples:

```text
external_id
→ customer number, CRM ID, employee ID, source-system ID, MSISDN

external_reference
→ payment reference, billing reference, shipping reference, ERP ID
```

The framework does not decide that meaning for the user.

---

## What is now covered

The framework has:

- a generic `BaseClient`,
- a convenience `MicroserviceClient`,
- neutral Service Objects for users, products, and orders,
- typed Pydantic models,
- unit tests for reusable SOM helpers and models,
- integration tests for concrete Service Objects,
- a domain-neutral multi-service workflow,
- Swagger/OpenAPI generator behavior tests,
- documented client-selection rules.

This is enough to demonstrate the core SOM pattern.

---

## SOM responsibility split

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

Preferred test style:

```python
order = order_service.create(
    OrderCreate(
        user_id=user.id,
        product_id=product.id,
        total_amount=product.price,
    )
)

assert order.status == "NEW"
```

Avoid repeatedly building raw HTTP calls in business-facing tests.

---

## BaseClient vs MicroserviceClient

### BaseClient

`BaseClient` is the generic low-level HTTP foundation.

It returns raw `httpx.Response`.

Use it when a Service Object needs control over:

- status codes,
- response headers,
- raw body,
- redirects,
- rate limits,
- correlation IDs,
- idempotency keys,
- provider-specific behavior,
- non-JSON responses.

Mental model:

```text
Give me the raw response.
The Service Object decides what it means.
```

### MicroserviceClient

`MicroserviceClient` is a convenience client for simple JSON services.

It parses successful JSON responses and raises for HTTP errors.

Use it when:

- the API is predictable,
- successful responses are JSON,
- errors should fail fast,
- tests do not need raw response handling.

Mental model:

```text
Give me parsed JSON or fail fast.
```

---

## Quick decision guide

Use `MicroserviceClient` when:

```text
API is simple
API returns JSON
you want dict/list/None
HTTP errors should fail immediately
you do not need headers or raw status handling
```

Use `BaseClient` when:

```text
you need raw httpx.Response
you verify status codes or headers
you handle 202, 204, 409, 422, 429, redirects, or polling
you need provider-specific behavior
you use advanced authentication, correlation, or idempotency
```

Tests should normally use concrete Service Objects, not either client directly.

---

## Stop point

Do not add more local demo microservices just to make the example richer.

Avoid adding local demo services such as:

```text
PaymentService
InventoryService
PromoService
BillingService
NotificationService
ShippingService
TaxService
```

unless real framework acceptance work proves they are needed.

The local services exist only to exercise the skeleton.

They must not become the product.

---

## Future project adaptation

A real project will add domain-specific:

- Service Objects,
- Pydantic models,
- fixtures,
- test data,
- contract checks,
- authentication,
- targeted unit tests,
- integration workflows.

Those tests should focus on real methods, contracts, transformations, and risks.

The framework does not require a unit test for every trivial wrapper.

---

## Current conclusion

The SOM foundation is good enough for the current framework-core stage.

It is now:

- structurally explicit,
- executable,
- domain-neutral but readable,
- ready for later project-specific adaptation.

The next validation step is not another fake service.

It is framework acceptance against real or realistic systems.
