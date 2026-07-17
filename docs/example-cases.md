# Example cases and validation boundaries

This document separates three things that should not be confused:

```text
current local examples
framework acceptance
future reference implementation
```

The local examples make the skeleton executable.

Framework acceptance will evaluate whether the skeleton helps on a real or
realistic need.

The future reference repository will show one complete adaptation.

---

## Current local POM example

Current flow:

```text
product search
→ product details
→ add to cart
→ cart summary
→ checkout
→ order confirmation
```

Current artifacts include:

```text
pages/ecommerce_*.py
components/price_summary.py
tests/e2e/test_ecommerce_checkout_flow.py
services/demo_shop/
```

Purpose:

- exercise `BasePage`,
- exercise concrete Page Objects,
- exercise a Component Object,
- keep business assertions in the test,
- provide deterministic local E2E execution.

Boundary:

This is a minimal execution target.

It is not the final e-commerce reference implementation and should not grow
into a feature-rich shop.

---

## Current local SOM example

Current concepts:

```text
User
Product
Order
```

Current workflow:

```text
create user
→ create product
→ create order
→ change order status
→ attach optional external reference
```

Current artifacts include:

```text
api/users_service.py
api/products_service.py
api/orders_service.py
services/users/
services/products/
services/orders/
tests/integration/
```

Purpose:

- exercise `BaseClient` and `MicroserviceClient`,
- demonstrate concrete Service Objects,
- demonstrate typed request and response models,
- demonstrate a readable multi-service workflow,
- keep HTTP details outside business-facing tests.

Boundary:

The concepts are readable neutral examples.

They are not a universal domain model.

---

## Framework acceptance case

The next major validation should start from a real project need.

Possible need types:

```text
regression protection
test-support workflow
data or environment preparation
diagnostic or defect-reproduction automation
```

The acceptance case should verify whether a user can:

- identify the real need,
- choose the smallest useful scope,
- collect the required context,
- select POM, SOM, fixtures, workflow, and test level,
- implement project-specific artifacts,
- define meaningful assertions or workflow output,
- run the quality gates,
- document friction and limitations.

The acceptance target and requirements should be defined in the dedicated
framework-acceptance plan.

Do not prejudge the result.

The acceptance phase may reveal that:

- the structure helps,
- the instructions are unclear,
- a base class is too broad or too weak,
- a proposed abstraction is unnecessary,
- the skeleton needs revision.

That evidence is the point of the phase.

---

## Future reference implementation

After framework acceptance stabilizes the skeleton, create one separate
repository:

```text
qa-automation-framework-ecommerce-demo
```

It should show a complete e-commerce adaptation and contain a controlled
comparison of:

```text
human-led adaptation
vs
AI-assisted adaptation
```

Both paths should use:

- the same target application,
- the same starting skeleton,
- the same scope,
- the same flows,
- the same acceptance criteria,
- the same quality gates.

The goal is to compare adaptation processes, not maintain two competing demo
products.

---

## Complex enterprise UI validation

A future validation may use a more difficult enterprise UI with:

- dynamic rendering,
- overlays or frames,
- asynchronous loading,
- complex permissions,
- unstable locator candidates,
- advanced component trees,
- Shadow DOM.

That work should use a real or realistic application context.

It should not be implemented by expanding this repository into a fake CRM,
ERP, or other domain product.

---

## AI exploratory agent boundary

A dedicated AI frontend exploratory-testing agent remains conditional.

First evaluate the AI-assisted adaptation path.

Build a separate agent only if evidence shows a repeatable gap that normal LLM
assistance and Playwright tooling do not solve well enough.
