# qa-automation-framework

![Tests](https://github.com/MarcinMikula/qa-automation-framework/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> A reusable Python test automation framework skeleton for UI and API testing.
>
> Bring your own application, locators, endpoints, data, risks, and domain rules.

This repository is a **framework skeleton**, not a plug-and-play automation
product.

It provides two complementary adapter patterns:

- **Page Object Model (POM)** for browser-based UI and E2E automation.
- **Service Object Model (SOM)** for API, service, and integration automation.

A small local implementation keeps the skeleton executable and reviewable.

It is not the product.

---

## Current status

The POM and SOM foundations are closed for the current framework-core stage.

The repository currently contains:

```text
POM foundation
→ BasePage, BaseComponent, concrete Page Objects, component example, E2E flow

SOM foundation
→ BaseClient, MicroserviceClient, concrete Service Objects, typed models,
  integration tests, multi-service workflow

Local execution targets
→ minimal deterministic FastAPI services and demo shop

Adaptation guidance
→ purpose-first human-led adaptation guide

Next major phase
→ framework acceptance against real or realistic application needs
```

Green local tests and CI prove that the committed implementation is executable
and internally consistent.

They do **not** yet prove that the skeleton is useful to a person adapting it to
a concrete project.

That is the purpose of the next framework-acceptance phase.

---

## What this repository is

This repository is a practical starting point for automation around systems
such as:

- customer-facing web applications,
- internal business tools,
- API-driven platforms,
- integration-heavy systems,
- regulated environments,
- complex enterprise applications.

It provides reusable structure.

The project supplies:

- the real testing or test-support need,
- application behavior,
- UI locators,
- API contracts,
- authentication,
- test data,
- environment configuration,
- risks,
- expected results,
- domain-specific fixtures and workflows.

The framework should be filled because a project has a real need.

It should not be filled only because folders exist.

---

## What this repository is not

This repository is **not**:

- a ready-made framework for every application,
- a complete test suite,
- a domain-specific automation product,
- a replacement for test analysis or domain knowledge,
- an AI agent,
- a self-healing tool,
- a code generator that removes the need for review,
- proof that the skeleton has already passed framework acceptance.

The local examples demonstrate structure and execution.

They do not claim production readiness for an unknown system.

---

## Purpose-first adaptation

The preferred adaptation sequence is:

```text
project need
→ automation intent
→ smallest useful scope
→ required context
→ POM / SOM / workflow / fixture
→ expected result or useful output
→ implementation
→ evidence
→ human acceptance
```

Typical automation intents include:

```text
verification
→ regression, smoke, integration, contract, or E2E checks

test support
→ repeated setup, cleanup, record creation, or environment preparation

data and environment work
→ seeding, generation, reconciliation, or state reset

diagnostic work
→ defect reproduction, traces, screenshots, responses, or evidence collection
```

Not every useful automation is a test.

```text
POM and SOM are reusable automation adapters.

Tests are one consumer.
Test-support workflows are another.
```

A workflow should not pretend to be a test when it does not verify product
behavior.

For the full process, see:

- [Adaptation guide](docs/adaptation-guide.md)
- [Human-led adaptation guide](docs/human-led-adaptation.md)

---

## Human-led does not mean tool-free

A human-led adaptation may use:

- Playwright Codegen,
- browser DevTools,
- OpenAPI/Swagger,
- IDE refactoring,
- deterministic generators,
- LLM assistance.

The distinction is ownership.

A human owns:

- the project need,
- architecture,
- Page Object and Service Object boundaries,
- test-level selection,
- risk selection,
- assertions,
- final acceptance.

Tools may accelerate discovery and drafting.

They do not own correctness.

---

## Why POM and SOM are in one repository

Many systems are not tested effectively through only one interface.

| Layer | Pattern | Purpose |
|---|---|---|
| UI / E2E | Page Object Model | Model screens, reusable components, user actions, and visible outcomes |
| API / integration | Service Object Model | Model endpoints, service operations, contracts, setup, and backend behavior |

POM and SOM share one repository, but they are not merged into one abstraction.

```text
pages/ and components/
→ UI adapter layer

api/
→ API/service adapter layer

tests/
→ verification intent and assertions

optional project workflows
→ repeated test-support orchestration
```

---

## Core framework vs local execution targets

### Reusable framework structure

```text
pages/        Page Object Model layer
components/   reusable UI component layer
api/          Service Object Model layer
testdata/     deterministic example data and settings
tests/        unit, integration, and E2E structure
.github/      CI workflow
docs/         decisions, guides, gaps, and limitations
```

### Replaceable local examples

```text
services/     minimal FastAPI users, products, and orders services
demo shop     minimal UI target for the POM flow
tests/unit/   reusable-mechanics and local-model examples
tests/integration/
              Service Object examples and neutral workflow
tests/e2e/    browser examples through Page Objects
```

The local targets exist to exercise the framework.

They must not become a product roadmap.

---

## Project structure

```text
qa-automation-framework/
├── .github/
│   └── workflows/
│       └── tests.yml
├── api/
│   ├── base_client.py
│   ├── microservice_client.py
│   ├── orders_service.py
│   ├── products_service.py
│   ├── users_service.py
│   └── swagger_generator.py
├── components/
│   ├── base_component.py
│   └── price_summary.py
├── docs/
│   ├── README.md
│   ├── architecture-decisions.md
│   ├── project-map.md
│   ├── gaps.md
│   ├── known-limitations.md
│   ├── testing-strategy.md
│   ├── pom-guide.md
│   ├── pom-base-page.md
│   ├── pom-components.md
│   ├── pom-foundation-checkpoint.md
│   ├── som-guide.md
│   ├── som-foundation-checkpoint.md
│   ├── adaptation-guide.md
│   ├── human-led-adaptation.md
│   ├── framework-filling-instructions-plan.md
│   ├── example-cases.md
│   ├── ai-assisted-adaptation.md
│   └── future-ideas.md
├── pages/
│   ├── base_page.py
│   ├── ecommerce_search_page.py
│   ├── ecommerce_product_page.py
│   ├── ecommerce_cart_page.py
│   ├── ecommerce_checkout_page.py
│   ├── ecommerce_order_confirmation_page.py
│   └── swagger_users_page.py
├── services/
│   ├── common/
│   ├── demo_shop/
│   ├── orders/
│   ├── products/
│   └── users/
├── testdata/
│   ├── settings.py
│   └── testdb.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── AUTOMATION_PRINCIPLES.md
├── CODEGEN.md
├── LEARNINGS.md
├── PHILOSOPHY.md
├── README.md
└── requirements.txt
```

---

## Page Object Model

The POM layer hides browser mechanics from tests.

Instead of:

```python
page.get_by_test_id("search-input").fill("laptop")
page.get_by_test_id("search-submit").click()
```

a test should speak through a Page Object:

```python
search_page.search_for("laptop")
```

Responsibility split:

```text
BasePage / BaseComponent
→ reusable Playwright mechanics

Concrete Page Objects / Components
→ application-facing UI actions and state

Tests
→ scenario intent and business assertions
```

---

## Service Object Model

The SOM layer hides repeated HTTP mechanics from tests and workflows.

Instead of:

```python
response = client.post("/orders", json=order_payload)
assert response.status_code == 201
```

a test can speak through a Service Object:

```python
order = order_service.create(order_payload)
```

Responsibility split:

```text
BaseClient / MicroserviceClient
→ reusable HTTP mechanics

Concrete Service Objects
→ service operations and response mapping

Tests or workflows
→ verification or orchestration intent
```

The active examples use readable neutral concepts:

```text
User
Product
Order
external_id
external_reference
```

A real project replaces or extends their meaning.

---

## Testing strategy

The repository separates:

```text
framework consistency gates
→ syntax and pytest collection

unit tests
→ small deterministic contracts and reusable mechanics

integration tests
→ Service Objects, APIs, and component boundaries

E2E tests
→ a small number of user-visible browser flows
```

The test pyramid is used as a maintenance heuristic, not as a claim that one
fixed distribution is correct for every project.

Test placement should follow:

- the risk,
- the behavior being checked,
- the fastest trustworthy test level,
- maintainability,
- diagnostic value.

See [Testing strategy](docs/testing-strategy.md).

---

## Current executable examples

### POM

```text
product search
→ product details
→ add to cart
→ checkout
→ order confirmation
```

The flow exists to exercise Page Objects and component boundaries.

It is not the future reference implementation.

### SOM

```text
user
→ product
→ order
→ status change
→ optional external reference
```

The flow exists to exercise Service Objects and typed models.

It is not a universal domain model.

See [Example cases](docs/example-cases.md).

---

## Run locally

### Install dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### Initialize local test data

```bash
python testdata/testdb.py
```

### Start local services manually

```bash
python -m services.users.main
python -m services.orders.main
python -m services.products.main
```

Integration and E2E fixtures may also start the required local targets.

### Run checks and tests

```bash
python -m compileall -q api pages components services testdata tests
python -m pytest --collect-only -q
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/e2e/ -v
```

### Generate Allure results locally

```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

A published Allure dashboard is not part of the current baseline.

---

## Documentation

| Document | Purpose |
|---|---|
| [Documentation index](docs/README.md) | Entry point for project documentation |
| [Architecture decisions](docs/architecture-decisions.md) | Current design decisions and boundaries |
| [Project map](docs/project-map.md) | Current framework layers, status, and direction |
| [Gaps](docs/gaps.md) | Open work and deferred validation |
| [Known limitations](docs/known-limitations.md) | Current boundaries and evidence limits |
| [Testing strategy](docs/testing-strategy.md) | Consistency gates, test levels, markers, and CI |
| [POM guide](docs/pom-guide.md) | Page Object Model rules |
| [POM foundation checkpoint](docs/pom-foundation-checkpoint.md) | Current POM stop point |
| [SOM guide](docs/som-guide.md) | Service Object Model rules |
| [SOM foundation checkpoint](docs/som-foundation-checkpoint.md) | Current SOM stop point |
| [Adaptation guide](docs/adaptation-guide.md) | Short purpose-first adaptation path |
| [Human-led adaptation](docs/human-led-adaptation.md) | Detailed path from project need to human acceptance |
| [Example cases](docs/example-cases.md) | Current examples and future reference implementation boundary |
| [AI-assisted adaptation](docs/ai-assisted-adaptation.md) | Preliminary AI guardrails and future comparison boundary |
| [Future ideas](docs/future-ideas.md) | Ideas intentionally outside current scope |

Root-level supporting documents:

- [AUTOMATION_PRINCIPLES.md](AUTOMATION_PRINCIPLES.md) — evergreen testing
  and automation principles.
- [PHILOSOPHY.md](PHILOSOPHY.md) — project-specific rationale.
- [LEARNINGS.md](LEARNINGS.md) — decisions and lessons from implementation.
- [CODEGEN.md](CODEGEN.md) — OpenAPI-based Service Object scaffolding notes.

---

## Future reference implementation

After framework acceptance stabilizes the skeleton, create one separate
repository:

```text
qa-automation-framework-ecommerce-demo
```

It should contain a controlled comparison of:

```text
human-led adaptation
vs
AI-assisted adaptation
```

Both approaches should use the same target, starting skeleton, scope,
acceptance criteria, and quality gates.

This core repository remains domain-neutral.

---

## AI-assisted adaptation

AI may help draft:

- Page Objects,
- Service Objects,
- fixtures,
- workflows,
- test skeletons,
- documentation,
- refactoring proposals.

A human must still verify:

- whether the need is real,
- whether the scenario matters,
- whether the test level is appropriate,
- whether locators and contracts are verified,
- whether assertions protect the intended risk,
- whether the result is maintainable.

```text
AI proposes.
Tests provide evidence.
A human accepts or rejects.
```

See [AI-assisted adaptation](docs/ai-assisted-adaptation.md).

---

## Tooling

Developed with Python, pytest, Playwright, httpx, FastAPI, SQLAlchemy, Allure,
GitHub Actions, and AI-assisted coding tools.

Generated or AI-assisted output is not treated as framework code until it has
been reviewed and tested.
