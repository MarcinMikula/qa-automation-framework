# Project map

This document maps the current repository structure and project direction.

It is a high-level orientation document.

It does not replace the root `README.md`, architecture decisions, or detailed
guides.

---

## Project identity

This repository is a reusable QA automation framework skeleton.

It is focused on:

- Page Object Model,
- Service Object Model,
- clear test levels,
- deterministic local execution,
- reusable automation structure,
- future project-specific adaptation.

It is not:

```text
a demo shop
a demo CRM
a demo ERP
a domain-specific product
a plug-and-play enterprise framework
```

The framework should stay simple, readable, reusable, and ready to be filled
with project-specific content.

---

## Current stage

Current stage:

```text
POM/SOM foundation completed, inactive legacy placeholders removed, and public
documentation aligned for the framework-core phase.
```

This does not mean the framework is fully validated.

It means the core structure now exists and should not be expanded through fake
demo-product features.

Next important work is around:

- agile, risk-based framework acceptance,
- framework requirements and acceptance risks,
- human-led adaptation guide validation,
- AI-assisted filling instructions,
- reporting improvements,
- dependency review.

---

## Core framework layers

Current conceptual map:

```text
POM layer
├── BasePage
├── concrete Page Objects
├── BaseComponent
├── concrete Components
└── E2E tests with business assertions

SOM layer
├── BaseClient
├── MicroserviceClient
├── concrete Service Objects
├── Pydantic request/response models
└── integration tests with business assertions

Test infrastructure
├── pytest configuration
├── fixtures
├── markers
├── local deterministic services
├── E2E service autostart
└── CI consistency gates

Documentation
├── architecture decisions
├── known limitations
├── gaps
├── testing strategy
├── POM guides/checkpoints
├── SOM guides/checkpoints
├── adaptation guidance
└── future filling/acceptance plans
```

---

## POM map

Current POM foundation:

```text
pages/base_page.py
→ reusable page-level browser mechanics

components/base_component.py
→ reusable component-level browser mechanics

pages/ecommerce_*.py
→ concrete Page Object examples

pages/swagger_users_page.py
→ technical smoke Page Object

components/price_summary.py
→ concrete component example

tests/e2e/
→ browser-level tests through Page Objects
```

Responsibility split:

```text
BasePage
→ page-level mechanics

Concrete Page Objects
→ application-facing page actions and state

BaseComponent
→ component-level mechanics

Concrete Components
→ reusable UI fragment behavior and state

Tests
→ business assertions
```

Stop point:

```text
Do not add more demo UI components now.
```

Future Page Objects and components should be created during real
application-context adaptation.

---

## SOM map

Current SOM foundation:

```text
api/base_client.py
→ generic low-level HTTP foundation

api/microservice_client.py
→ convenience client for simple local JSON microservices

api/users_service.py
api/products_service.py
api/orders_service.py
→ concrete Service Object examples

api/swagger_generator.py
→ OpenAPI/Swagger helper for scaffolding Service Objects

tests/integration/
→ Service Object integration tests and workflow tests
```

Responsibility split:

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

Client decision guide:

```text
BaseClient
→ raw httpx.Response, advanced/external/provider-specific APIs

MicroserviceClient
→ parsed JSON, simple local/internal CRUD-like APIs
```

Stop point:

```text
Do not add more demo microservices now.
```

Future Service Objects should be created during real application-context
adaptation.

---

## Domain-neutral example vocabulary

The framework core uses readable neutral nouns:

```text
User
Product
Order
```

It intentionally avoids two extremes:

```text
hidden industry assumptions
and
unhelpful abstractions such as Entity or Resource
```

Project-specific adaptation owns the domain vocabulary.

Examples:

```text
User → Customer, Subscriber, Employee, Contact
external_id → CRM ID, customer number, MSISDN
external_reference → payment, billing, shipping, or ERP reference
```

This keeps the skeleton understandable for automation engineers and for test
analysts or methodologists with strong project knowledge but less programming
experience.

---

## Purpose-first adaptation

The framework should be filled because a project has a real testing or
test-support need.

It should not be filled only because folders exist.

Current adaptation model:

```text
project need
→ automation intent
→ smallest useful scope
→ POM / SOM / workflow / fixture
→ expected result or output
→ implementation
→ evidence
→ human acceptance
```

POM and SOM may support:

```text
verification tests
and
test-support workflows
```

The initial detailed guide lives in:

```text
docs/human-led-adaptation.md
```

Human-led means that tools may help with discovery and drafting, while a human
owns architecture, risk, assertions, and acceptance.

---

## Demo target boundary

Demo targets exist only to make the framework executable and reviewable.

They are not the product.

The guiding rule:

```text
The demo target exists to exercise the framework.
It must not become the framework.
```

Current local demos are acceptable because they support deterministic tests.

They should not grow into full fake products.

---

## Repository hygiene

The active repository should contain only code that supports the current
framework story.

Current rule:

```text
Runnable and maintained examples stay in the repository.
Historical attempts stay in Git history and LEARNINGS.md.
```

The earlier unvalidated auth/customer/login/dashboard placeholders and static
telco mocks were removed instead of being moved into a legacy directory.

The `external` pytest marker remains available for future real-project tests,
but the framework does not ship inactive external placeholders.

---

## Current test map

Current test levels:

```text
tests/unit/
→ reusable framework helpers, models, stores, generators

tests/integration/
→ Service Object tests and local API workflow tests

tests/e2e/
→ browser flows through Page Objects
```

Current consistency gates:

```text
python -m compileall -q api pages components services testdata tests
python -m pytest --collect-only -q
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/e2e/ -v
```

The goal is not only green CI.

The goal is to understand what green CI proves.

---

## Documentation map

Recommended reading order:

1. `docs/architecture-decisions.md`
2. `docs/known-limitations.md`
3. `docs/testing-strategy.md`
4. `docs/project-map.md`
5. `docs/pom-guide.md`
6. `docs/pom-base-page.md`
7. `docs/pom-components.md`
8. `docs/pom-foundation-checkpoint.md`
9. `docs/som-guide.md`
10. `docs/som-foundation-checkpoint.md`
11. `docs/adaptation-guide.md`
12. `docs/human-led-adaptation.md`
13. `docs/framework-filling-instructions-plan.md`
14. `docs/example-cases.md`
15. `docs/ai-assisted-adaptation.md`
16. `docs/gaps.md`
17. `docs/future-ideas.md`

Evergreen automation principles live in:

```text
AUTOMATION_PRINCIPLES.md
```

---

## Parked future work

Parked topics:

- validation of the human-led adaptation guide,
- AI-assisted framework filling guide,
- framework UAT plan,
- context-aware framework filler,
- complex enterprise UI validation,
- real e-commerce validation,
- reporting/Allure dashboard,
- dependency and runner compatibility review.

These should not pull the project into building richer fake demo applications.

---

## Final validation question

The final validation question remains:

```text
Does this framework skeleton actually help automate a concrete application?
```

That should be answered later through framework UAT:

```text
take a real or realistic application
fill the skeleton with project-specific content
write meaningful POM/SOM tests
observe friction
improve the framework
```

This is UAT of the framework as a tool.

It is not UAT of the tested application.
