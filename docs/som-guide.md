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

It should expose readable operations:

```python
user_service.get(user_id)
product_service.get(product_id)
order_service.create(order_payload)
order_service.update(order_id, status_update)
```

---

## Responsibility of a test

A test should know:

- the API behavior being verified,
- the input data,
- the expected outcome,
- the business or technical risk.

It should not repeatedly build raw URLs, headers, and payloads.

---

## Weak vs stronger Service Objects

Weak:

```python
response = api_client.post(
    "/orders",
    json={
        "user_id": 123,
        "product_id": 456,
        "total_amount": 49.99,
    },
)
assert response.status_code == 201
```

Stronger:

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

The second version communicates intent and keeps HTTP mechanics below the test.

---

## Domain-neutral example vocabulary

Domain-neutral does not mean abstract.

The skeleton intentionally uses:

```text
User
Product
Order

UserService
ProductService
OrderService
```

These names are understandable to automation engineers, test analysts, and
people who know the project architecture but have less programming experience.

The skeleton avoids generic names such as:

```text
Entity
Resource
Object
GenericManager
```

It also avoids embedding one industry's assumptions.

For example, the core SOM does not define:

```text
MSISDN
PREPAID / POSTPAID
tariff plan
billing invoice reference
mobile plan
```

A real adaptation may replace or extend the neutral vocabulary:

```text
Telco:
User → Subscriber
external_id → MSISDN

CRM:
User → Customer or Contact
external_id → CRM record identifier

E-commerce:
User → Customer
external_reference → payment or fulfilment reference
```

The project supplies the domain meaning.

The framework supplies the structure.

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

The repository documents two client styles:

```text
BaseClient
→ raw httpx.Response and explicit response handling

MicroserviceClient
→ parsed JSON for simple deterministic services
```

See `som-foundation-checkpoint.md` for the decision guide.

---

## Typed payloads and responses

Pydantic models make request and response contracts explicit.

Example:

```python
user = user_service.create(
    UserCreate(
        full_name="Alex Morgan",
        external_id="USR-001",
        status="ACTIVE",
    )
)
```

Project adaptations may add their own fields and models.

The skeleton models are examples, not universal business contracts.

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
