# Architecture decisions

This file records the main design decisions behind the framework.

It is not a complete architecture specification. It is a map of the decisions
that future maintainers should not have to rediscover from code or commit
history.

---

## Decision 1 — Treat the repository as a framework skeleton, not a product

**Decision:**

This repository is positioned as a reusable QA automation framework skeleton.

It is not a plug-and-play automation solution.

**Reasoning:**

Real enterprise applications require project-specific context:

- locators,
- authentication,
- test data,
- API contracts,
- roles,
- permissions,
- business rules,
- environment configuration.

A public repository cannot provide those safely or honestly.

**Consequence:**

The repository provides structure and examples, but the user must adapt it to
the application under test.

---

## Decision 2 — Keep POM and SOM in one repository, but in separate layers

**Decision:**

Page Object Model and Service Object Model live in the same repository.

They are not merged into one abstraction.

**Reasoning:**

Enterprise QA automation often needs both UI and API coverage.

A single framework skeleton can provide shared configuration, fixtures,
reporting, and test structure while keeping UI and API responsibilities
separate.

**Consequence:**

- `pages/` contains UI-facing Page Objects.
- `api/` contains API-facing Service Objects.
- `tests/e2e/` should use POM.
- `tests/integration/` should use SOM.
- shared fixtures and settings may support both layers.

---

## Decision 3 — Treat `services/` as replaceable example implementation

**Decision:**

The FastAPI services under `services/` are demo infrastructure, not framework
core.

**Reasoning:**

They make the skeleton executable and reviewable without access to a private
enterprise system.

**Consequence:**

Real users may remove or replace `services/` with their actual application,
public test API, or internal test environment.

---

## Decision 4 — Keep tests organized by level

**Decision:**

Tests are grouped into:

```text
tests/unit/
tests/integration/
tests/e2e/
```

**Reasoning:**

The test pyramid is a maintenance strategy.

Different test levels answer different questions and have different costs.

**Consequence:**

New tests should be added to the level that matches the risk being tested.

---

## Decision 5 — CI should run deterministic tests by default

**Decision:**

CI should prefer deterministic tests that do not depend on private or unstable
live systems.

**Reasoning:**

A public skeleton should be runnable and understandable without secrets, VPN
access, or corporate environments.

**Consequence:**

External/live tests should be marked explicitly and excluded from default CI
unless deliberately enabled.

---

## Decision 6 — AI may assist adaptation, but QA owns correctness

**Decision:**

The repository may be used with AI-assisted development, but AI output is not
treated as correct by default.

**Reasoning:**

AI can generate useful structure, but it cannot safely infer project truth,
production risk, or business meaning without review.

**Consequence:**

Generated Page Objects, Service Objects, fixtures, and tests require manual QA
review before being trusted.

---

## Decision 7 — Keep evergreen principles outside project documentation

**Decision:**

General testing principles live in `AUTOMATION_PRINCIPLES.md`.

**Reasoning:**

Principles such as deterministic data, business-readable tests, and QA
ownership of AI-generated output apply beyond this repository.

**Consequence:**

Project documentation can stay focused on this framework, while broader
testing rules remain preserved separately.

---

## Decision 8 — Use e-commerce as the first public POM/SOM demo context

**Decision:**

Use an e-commerce-like system as the first public demonstration context for the
framework, while keeping Salesforce/ERP/CRM-style systems as future hard POM
validation targets.

**Reasoning:**

E-commerce is a strong public demonstration context because it is recognizable,
business-readable, and naturally maps to both UI and API automation.

It is especially strong for SOM — Service Object Model — because typical
e-commerce systems expose many service boundaries, for example:

- `Catalog`,
- `Search`,
- `Cart`,
- `Order`,
- `Payment`,
- `Inventory`,
- `Pricing`,
- `Promo`,
- `User`,
- `Notification`,
- `Review`.

These boundaries can be represented as Service Objects and tested through
business workflows such as:

```text
search product
→ create cart
→ add item
→ apply promo
→ create order
→ simulate payment
→ verify order status
```

E-commerce can also support a useful POM demonstration, for example:

```text
product search
→ product details
→ add to cart
→ cart summary
→ checkout
→ order confirmation
```

However, e-commerce should not be treated as the hardest possible POM
validation target.

Large enterprise ERP/CRM systems, especially Salesforce-like applications, are
a stronger future POM challenge because they may include:

- highly dynamic UI,
- Shadow DOM,
- complex component trees,
- iframes or overlays,
- long asynchronous loading,
- unstable selectors,
- complex authentication,
- bot-detection or login friction,
- enterprise-specific workflows and permissions.

**Consequence:**

The first public demo should stay e-commerce-oriented because it is practical,
understandable, and safe to run locally or in CI.

The final hard POM validation may still use Salesforce/ERP/CRM-style ideas, but
that should be treated as a later phase, not as the first public demo.

Future GraphQL-based Service Objects or Query Objects may be considered later,
especially if an application groups service requests through GraphQL. This is
not current scope.
