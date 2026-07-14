# POM case study plan

This document defines the planned Page Object Model case study for this
framework.

The goal is not to add another technical browser smoke test.

The goal is to answer a more useful question:

```text
Can this framework express a realistic UI automation flow through clear Page
Objects, fixtures, test data, and business-readable assertions?
```

This is separate from the final real-application validation. The POM case study
is still an internal framework demonstration. The final validation should later
apply the skeleton to a concrete application context.

---

## Current decision

The first realistic POM case study should use an e-commerce-like flow.

Earlier ideas included CRM/telco-style flows such as customer search, plan
change, or order creation. Those are still useful, but e-commerce is a better
first public demonstration because it is easier to understand, easy to model
locally, and naturally combines UI, API, test data, and business assertions.

The chosen direction:

```text
Product search
→ product details
→ add to cart
→ cart summary
→ checkout step
→ order confirmation
```

This flow is small enough to implement safely, but realistic enough to show why
POM matters.

---

## Current state

The current E2E layer proves that Playwright can run in the framework and that
a Page Object can hide browser interactions.

However, the current UI example is still based on Swagger UI.

That is useful as a smoke test, but it is not a strong POM demonstration.

Known limitations:

- the UI is documentation-oriented, not business-oriented,
- the flow does not model a realistic user task,
- assertions are mostly technical,
- the Page Object is tied to generated Swagger UI structure,
- the example does not yet show reusable page/component boundaries.

---

## Target e-commerce flow

The first POM case study should model a small e-commerce journey.

Recommended first slice:

```text
Search product
→ open product details page
→ add product to cart
→ verify cart total
→ continue to checkout
→ place demo order
→ verify order confirmation
```

Possible Page Objects:

```text
SearchPage
ProductPage
CartPage
CheckoutPage
OrderConfirmationPage
```

Possible reusable components:

```text
HeaderNavigation
MiniCart
ConfirmationBanner
PriceSummary
```

The first version does not need a full production-like shop.

It only needs enough UI and state to prove the framework structure.

---

## Why e-commerce is a good POM case study

E-commerce is useful for POM because it contains recognizable user journeys and
clear business outcomes:

- search should return relevant products,
- product details should show price and availability,
- add-to-cart should update basket state,
- cart total should match product price and quantity,
- checkout should preserve selected products and customer data,
- order confirmation should expose a meaningful order identifier or status.

These are visible UI behaviors, so they belong naturally in a small number of
E2E tests.

At the same time, many rules can and should be tested lower:

- price calculation,
- promo logic,
- quantity boundaries,
- inventory rules,
- order status transitions,
- API error handling.

This keeps the POM case study aligned with the test pyramid instead of turning
E2E into a dumping ground for every possible check.

---

## What this case study should prove

The POM case study should prove that the framework supports:

- business-readable E2E tests,
- clear Page Object boundaries,
- reusable component abstractions where useful,
- selectors hidden outside test bodies,
- test assertions owned by tests, not Page Objects,
- environment/configuration separation,
- realistic test data usage,
- deterministic CI execution,
- useful failure diagnostics.

It should also make limitations visible instead of hiding them.

---

## What this case study should not prove

This case study should not pretend to prove:

- production e-commerce readiness,
- compatibility with every enterprise SPA,
- complex payment-provider integration,
- real logistics integration,
- event-driven consistency,
- full checkout risk coverage,
- Shadow DOM handling,
- self-healing selectors,
- AI-generated framework adaptation,
- full production-grade test coverage.

Those are separate concerns.

This case study is only a framework structure demonstration.

---

## Suggested folder impact

A small local e-commerce UI case study could add or extend:

```text
pages/
├── search_page.py
├── product_page.py
├── cart_page.py
├── checkout_page.py
└── order_confirmation_page.py

components/
├── header_navigation.py
├── mini_cart.py
├── confirmation_banner.py
└── price_summary.py

tests/e2e/
└── test_ecommerce_checkout_flow.py
```

If a local demo UI is added, it could live under:

```text
services/demo_ui/
```

or a clearly named example area.

The UI should stay replaceable. It must not become the framework's main product.

---

## Page Object rules

Page Objects should:

- expose user actions,
- hide Playwright selectors,
- model screens or stable UI areas,
- return useful state when needed,
- avoid business assertions.

Example style:

```python
search_page.search_for("Samsung 65 OLED")
product_page.add_to_cart()
cart_page.proceed_to_checkout()
checkout_page.place_order(customer_data)
```

Page Objects should not do this:

```python
assert cart_page.total_is_correct()
```

The test should own the assertion.

---

## Test rules

E2E tests should:

- describe a user-visible scenario,
- stay short,
- avoid raw selectors,
- avoid low-level Playwright details,
- use Page Objects and fixtures,
- verify business-relevant outcomes.

Example target style:

```python
def test_customer_can_buy_available_product(...):
    search_page.search_for("Samsung 65 OLED")
    product_page.open_first_result()
    product_page.add_to_cart()
    cart_page.proceed_to_checkout()
    checkout_page.place_order(customer_data)

    assert order_confirmation.order_id() is not None
    assert order_confirmation.status() == "Order confirmed"
```

---

## Candidate requirements

Possible framework-level requirements for the POM case study:

```text
POM-REQ-001
The framework shall allow E2E tests to interact with UI flows through Page
Objects instead of raw Playwright selectors in test bodies.

POM-REQ-002
The framework shall keep business assertions in tests, not inside Page Objects.

POM-REQ-003
The framework shall support reusable UI component abstractions for repeated UI
areas such as navigation, messages, mini-cart, or price summaries.

POM-REQ-004
The framework shall support deterministic execution of the POM case study in
CI without private credentials.

POM-REQ-005
The framework shall make the replaceable demo UI boundary explicit.

POM-REQ-006
The framework shall demonstrate at least one business-readable e-commerce UI
flow with meaningful assertions.

POM-REQ-007
The framework shall keep E2E coverage focused on critical user-facing behavior
and leave lower-level rules to unit or integration tests.
```

---

## Acceptance criteria

The POM case study can be considered useful when:

- at least one realistic e-commerce UI flow exists,
- the test body contains no raw selectors,
- Page Objects expose meaningful user actions,
- assertions verify business-relevant outcomes,
- cart/order state is visible and verifiable,
- the flow runs locally and in CI,
- documentation explains what the case study proves,
- documentation explains what it does not prove.

---

## Open decisions

Before implementation, decide:

1. Should the first POM case study use a local demo UI?
2. Should the demo UI be FastAPI/Jinja, simple static HTML, or another minimal
   frontend?
3. Should it reuse existing local service data or stay isolated?
4. Should the first slice include full checkout or stop at cart validation?
5. Should the first version include login, or should login be deferred?
6. Should product/cart/order state be backed by local services or in-memory UI
   state?
7. How much UI code is acceptable before the demo app becomes too large?

---

## Recommended first implementation slice

The smallest useful slice:

```text
Local demo e-commerce UI
→ product search
→ product details
→ add to cart
→ cart total
→ order confirmation
→ one E2E test through Page Objects
```

This is enough to show the POM pattern without pretending to be a full online
shop.

It also creates a bridge to the final validation question:

```text
Does this framework skeleton actually help automate a concrete application?
```