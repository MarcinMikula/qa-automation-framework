# qa-automation-framework

![Tests](https://github.com/MarcinMikula/qa-automation-framework/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> A reusable QA automation framework skeleton for enterprise UI and API testing.  
> Bring your own application, locators, endpoints, data, and domain rules.

This repository is a **framework skeleton**, not a plug-and-play automation product.

It provides a clean structure for building tests around two complementary automation patterns:

- **Page Object Model (POM)** for browser-based UI and E2E flows.
- **Service Object Model (SOM)** for API, microservice, and integration testing.

The repository includes a small working example implementation so the structure can be executed, reviewed, and adapted before it is used against a real application.

---

## What this repository is

This repository is a practical starting point for building automated tests in enterprise-style systems such as:

- CRM platforms,
- billing systems,
- customer portals,
- internal back-office tools,
- API-driven microservice platforms,
- regulated or integration-heavy environments.

It provides the reusable structure. You provide the project-specific context.

In a real project, you are expected to replace or extend:

- UI locators,
- page actions,
- API endpoints,
- service methods,
- test data,
- authentication flow,
- environment configuration,
- business assertions,
- domain-specific fixtures.

The goal is not to pretend that a public repository can fully automate an unknown enterprise system.

The goal is to show how a QA automation framework can be structured so it can be safely adapted to one.

---

## What this repository is not

This repository is **not**:

- a ready-made framework for every application,
- a Salesforce automation framework out of the box,
- a complete enterprise test suite,
- a replacement for domain knowledge,
- an AI agent,
- a self-healing test tool,
- a code generator that removes the need for review.

The skeleton can be used with AI-assisted development, but the output still requires QA review, project context, and manual adaptation.

---

## Why POM and SOM are in one repository

Many enterprise systems are not tested effectively through only one layer.

A realistic test automation project usually needs both:

| Layer | Pattern | Purpose |
|---|---|---|
| UI / E2E | Page Object Model | Model screens, forms, user actions, and browser flows |
| API / integration | Service Object Model | Model endpoints, service operations, contracts, and backend behavior |

Keeping POM and SOM in one framework skeleton is intentional.

They are not mixed into one abstraction. They are separated into different adapter layers:

- `pages/` contains UI-facing Page Objects.
- `api/` contains API-facing Service Objects.
- `tests/e2e/` uses POM.
- `tests/integration/` uses SOM.
- shared fixtures, settings, data, and reporting support both layers.

The shared repository gives one consistent test structure while keeping UI and API responsibilities separate.

---

## Core framework vs example implementation

This repository contains two things:

```text
1. Reusable framework skeleton
2. Replaceable example implementation
```

### Reusable framework skeleton

These parts represent the structure you would keep and adapt in a real project:

```text
pages/        Page Object Model layer for UI automation
components/   Reusable UI component abstractions
api/          Service Object Model layer for API automation
testdata/     Test data models, seed data, and settings
mocks/        Mocked responses and isolated test inputs
tests/        Unit, integration, and E2E test structure
.github/      CI workflow
docs/         Project documentation and adaptation guides
```

### Replaceable example implementation

These parts exist so the skeleton can run locally and demonstrate the patterns:

```text
services/     Example FastAPI microservices: users, orders, products
tests/unit/   Example unit tests for data models and constraints
tests/integration/
              Example API tests through Service Objects
tests/e2e/    Example browser tests through Page Objects
```

In a real project, the example microservices can be removed or replaced with your actual application under test.

---

## Project structure

```text
qa-automation-framework/
├── .github/
│   └── workflows/
│       └── tests.yml
├── api/
│   ├── base_client.py
│   ├── customer_service.py
│   ├── order_service.py
│   ├── product_service.py
│   ├── user_service.py
│   └── swagger_generator.py
├── components/
│   └── ...
├── docs/
│   ├── README.md
│   ├── architecture-decisions.md
│   ├── gaps.md
│   ├── known-limitations.md
│   ├── testing-strategy.md
│   ├── future-ideas.md
│   ├── pom-guide.md
│   ├── som-guide.md
│   ├── adaptation-guide.md
│   ├── example-cases.md
│   └── ai-assisted-adaptation.md
├── mocks/
│   └── ...
├── pages/
│   ├── base_page.py
│   ├── dashboard_page.py
│   ├── login_page.py
│   └── swagger_users_page.py
├── services/
│   ├── common/
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

## Main patterns

### Page Object Model

The POM layer hides browser details from tests.

Tests should not know CSS selectors, XPath expressions, or Playwright mechanics directly.

Instead of this:

```python
page.locator("[data-testid='username']").fill("admin")
page.locator("[data-testid='password']").fill("secret")
page.locator("[data-testid='login-button']").click()
```

A test should speak through a page object:

```python
login_page.login(username="admin", password="secret")
```

The responsibility of a Page Object is to expose meaningful user actions.

The responsibility of a test is to describe the scenario and verify the outcome.

### Service Object Model

The SOM layer hides HTTP details from tests.

Tests should not build raw URLs, headers, payloads, and status-code handling repeatedly.

Instead of this:

```python
response = client.post(
    "/customers/123/change-plan",
    json={"plan": "premium"}
)
assert response.status_code == 200
```

A test should speak through a service object:

```python
customer_service.change_plan(customer_id=123, new_plan="premium")
```

The responsibility of a Service Object is to expose meaningful API operations.

The responsibility of a test is to verify business-relevant behavior.

---

## Stack

| Area | Technology |
|---|---|
| UI automation | Playwright + pytest |
| API automation | httpx + Service Object Model |
| Test runner | pytest |
| Test data | SQLAlchemy + SQLite |
| Example backend | FastAPI |
| Reporting | Allure |
| CI | GitHub Actions |
| Language | Python 3.11+ |

---

## Test strategy

The framework follows the ISTQB-style test pyramid.

```text
        E2E / UI
      Playwright + POM
     critical user flows

    Integration / API
       httpx + SOM
 contracts, APIs, services

       Unit tests
 models, constraints, logic
```

E2E tests are intentionally fewer because they are slower, more fragile, and more expensive to maintain.

Detailed execution rules are documented in [Testing Strategy](docs/testing-strategy.md).

---

## Current example coverage

The repository currently includes an executable example test suite split by test level:

```text
tests/unit/          unit-level examples
tests/integration/   API / SOM examples
tests/e2e/           UI / POM examples
```

The example implementation is intentionally small.

Its purpose is to demonstrate structure, not to simulate a full enterprise system.

Tests marked as external should not block normal CI execution.

---

## How to use this skeleton

### 1. Clone the repository

```bash
git clone https://github.com/MarcinMikula/qa-automation-framework.git
cd qa-automation-framework
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 3. Initialize local test data

```bash
python testdata/testdb.py
```

### 4. Start the example services

```bash
python -m services.users.main &
python -m services.orders.main &
python -m services.products.main &
```

### 5. Run tests

```bash
python -m pytest tests/ -v -m "not external"
```

Run selected levels:

```bash
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v -m "not external"
python -m pytest tests/e2e/ -v
```

### 6. Generate an Allure report

```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

---

## How to adapt this framework to a real project

The short version:

1. Replace or extend Page Objects in `pages/` and `components/`.
2. Replace or extend Service Objects in `api/`.
3. Replace demo data in `testdata/` and `mocks/`.
4. Move environment-specific values into settings or environment variables.
5. Add tests at the correct level: unit, integration, or E2E.
6. Keep external/live tests opt-in.

For the full process, see [Adaptation Guide](docs/adaptation-guide.md).

---

## Documentation

Detailed project documentation lives in [`docs/`](docs/).

| Document | Purpose |
|---|---|
| [Documentation index](docs/README.md) | Entry point for the full documentation set |
| [Architecture decisions](docs/architecture-decisions.md) | Key design decisions and boundaries |
| [Gaps](docs/gaps.md) | Known open gaps and follow-up work |
| [Known limitations](docs/known-limitations.md) | Current boundaries and intentional non-goals |
| [Testing strategy](docs/testing-strategy.md) | Unit, integration, E2E, markers, and CI scope |
| [Future ideas](docs/future-ideas.md) | Ideas intentionally not in the current scope |
| [POM guide](docs/pom-guide.md) | How to structure UI automation with Page Objects |
| [SOM guide](docs/som-guide.md) | How to structure API automation with Service Objects |
| [Adaptation guide](docs/adaptation-guide.md) | How to adapt the skeleton to a real project |
| [Example cases](docs/example-cases.md) | Planned Salesforce-like UI and API/SOM examples |
| [AI-assisted adaptation](docs/ai-assisted-adaptation.md) | How to use AI safely with this skeleton |

Root-level supporting documents:

- [AUTOMATION_PRINCIPLES.md](AUTOMATION_PRINCIPLES.md) — evergreen testing and automation principles.
- [PHILOSOPHY.md](PHILOSOPHY.md) — older design rationale, to be rewritten after principles extraction.
- [LEARNINGS.md](LEARNINGS.md) — learning journal and lessons from building the framework.
- [CODEGEN.md](CODEGEN.md) — notes about Swagger/OpenAPI-based Service Object generation.

---

## Domain annotations

Some example files use domain markers to show what is reusable and what is project-specific.

```python
# [DOMAIN: TELCO] — telecommunications-specific example
# [DOMAIN: CRM] — CRM-specific example
# [DOMAIN: GENERIC] — reusable across most projects
```

When adapting the framework, search for domain markers and replace anything that does not match your project context.

The markers are not part of the framework mechanics.

They are documentation hints for safe adaptation.

---

## AI-assisted adaptation

This repository is designed to work well with AI-assisted development.

AI can speed up framework adaptation, but it should not decide business meaning on its own.

A QA engineer still needs to verify:

- whether the scenario matters,
- whether the assertion is valuable,
- whether the data is realistic,
- whether the locator is stable,
- whether the API operation matches the real contract,
- whether the test failure would help diagnose a real problem.

See [AI-assisted adaptation](docs/ai-assisted-adaptation.md) for a practical workflow.

---

## Tooling

Developed with AI assistance and manual QA review.

Tools used during development:

- Python,
- pytest,
- Playwright,
- FastAPI,
- SQLAlchemy,
- Allure,
- GitHub Actions,
- AI-assisted coding tools.

Every generated or AI-assisted change should be reviewed before being treated as framework code.
