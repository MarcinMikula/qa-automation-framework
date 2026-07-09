# qa-automation-framework

![Tests](https://github.com/MarcinMikula/qa-automation-framework/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> A reusable QA automation framework skeleton for enterprise UI and API testing.  
> Bring your own application, locators, endpoints, data, and domain rules.

This repository is a **framework skeleton**, not a plug-and-play automation product.

It gives you a clean structure for building tests around two complementary automation patterns:

- **Page Object Model (POM)** for browser-based UI and E2E flows.
- **Service Object Model (SOM)** for API, microservice, and integration testing.

The framework includes a small working example implementation so the structure can be executed, reviewed, and adapted before it is used against a real application.

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
│   ├── architecture.md
│   ├── pom_guide.md
│   ├── som_guide.md
│   ├── adaptation_guide.md
│   ├── test_strategy.md
│   ├── example_cases.md
│   ├── known_limitations.md
│   └── ai_assisted_adaptation.md
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

### Unit tests

Unit tests verify small, isolated pieces of logic.

Typical examples:

- model defaults,
- constraints,
- validation rules,
- deterministic seed data,
- edge cases.

### Integration tests

Integration tests verify communication between layers.

Typical examples:

- API response structure,
- HTTP status codes,
- service object behavior,
- contract-level assumptions,
- mocked or local service interactions.

### E2E tests

E2E tests verify user-facing flows through the browser.

Typical examples:

- login,
- search,
- create entity,
- submit form,
- verify visible result.

E2E tests are intentionally fewer because they are slower, more fragile, and more expensive to maintain.

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

### Step 1: Replace the UI layer

Update or add Page Objects in:

```text
pages/
components/
```

Replace demo selectors with real application locators.

Recommended locator strategy:

1. stable `data-testid` attributes where available,
2. accessible roles and names,
3. stable labels and form semantics,
4. CSS/XPath only when no better option exists.

### Step 2: Replace the API layer

Update or add Service Objects in:

```text
api/
```

Replace demo endpoints with real project APIs.

Each Service Object should represent meaningful business operations, not random HTTP calls.

Good examples:

```python
customer_service.get_customer_by_msisdn(...)
order_service.create_order(...)
billing_service.get_invoice_status(...)
case_service.create_case(...)
```

Weak examples:

```python
api_client.get(...)
api_client.post(...)
```

The lower-level HTTP methods belong in the base client. Tests should use domain-level service methods.

### Step 3: Replace test data

Update:

```text
testdata/
mocks/
```

Replace demo seed data with real project concepts.

For example:

```text
customer
account
contract
subscription
invoice
order
case
opportunity
```

### Step 4: Configure environments

Update settings and environment variables for your project.

Example:

```bash
BASE_URL=https://your-app.example.com
API_BASE_URL=https://your-api.example.com
```

Keep environment-specific values outside test logic.

Tests should not hardcode DEV, SIT, UAT, or PROD-like URLs.

### Step 5: Add project-specific tests

Add tests to the correct level:

```text
tests/unit/          pure logic, models, validation
tests/integration/   APIs, contracts, service behavior
tests/e2e/           critical UI flows
```

If you are unsure where a test belongs, ask:

```text
Am I testing a small unit, an API/service boundary, or a full user flow?
```

---

## Documentation

Detailed project documentation lives in [`docs/`](docs/).

| Document | Purpose |
|---|---|
| [Documentation index](docs/README.md) | Entry point for the full documentation set |
| [Architecture](docs/architecture.md) | Framework layers, boundaries, and data flow |
| [POM Guide](docs/pom_guide.md) | How to structure UI automation with Page Objects |
| [SOM Guide](docs/som_guide.md) | How to structure API automation with Service Objects |
| [Adaptation Guide](docs/adaptation_guide.md) | How to adapt the skeleton to a real project |
| [Test Strategy](docs/test_strategy.md) | Unit, integration, E2E, markers, and CI scope |
| [Example Cases](docs/example_cases.md) | Planned Salesforce-like UI and API/SOM examples |
| [Known Limitations](docs/known_limitations.md) | Current boundaries and intentional gaps |
| [AI-assisted Adaptation](docs/ai_assisted_adaptation.md) | How to use AI safely with this skeleton |

Root-level supporting documents:

- [PHILOSOPHY.md](PHILOSOPHY.md) — design rationale and test philosophy.
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

A practical workflow:

1. Provide the AI model with this repository structure.
2. Add project-specific context:
   - application type,
   - main user roles,
   - key workflows,
   - available environments,
   - authentication method,
   - UI locator strategy,
   - API documentation,
   - data constraints.
3. Ask the AI to propose Page Objects or Service Objects.
4. Review the generated code manually.
5. Replace fake assumptions with verified project facts.
6. Add tests gradually.
7. Run the suite locally and in CI.

AI can speed up framework adaptation, but it should not decide business meaning on its own.

A QA engineer still needs to verify:

- whether the scenario matters,
- whether the assertion is valuable,
- whether the data is realistic,
- whether the locator is stable,
- whether the API operation matches the real contract,
- whether the test failure would help diagnose a real problem.

---

## Example future use cases

The skeleton is intentionally generic, but it is suitable for realistic case studies such as:

### UI / POM case study

A Salesforce-like CRM flow:

```text
Login
→ open Sales / Service area
→ create Case or Opportunity
→ fill required fields
→ save
→ verify record status or confirmation
```

This belongs in the POM / E2E layer.

### API / SOM case study

A public or local microservice flow:

```text
Create customer
→ create order
→ verify order status
→ fetch related customer data
→ validate response contract
```

This belongs in the SOM / integration layer.

These case studies should be added as examples, not as hardcoded assumptions inside the framework core.

---

## Service Object generation

The repository includes a Swagger/OpenAPI helper as a productivity tool.

Example:

```bash
python api/swagger_generator.py --swagger path/to/swagger.json --tag customers
```

Generated code should be treated as a starting point.

Before accepting generated Service Objects, review:

- method names,
- endpoint paths,
- request payloads,
- response expectations,
- authentication,
- error handling,
- domain meaning.

Generated code is not automatically good test design.

---

## Design principles

### Tests should speak business language

A test should describe the behavior being verified.

Good:

```python
customer_service.suspend_account(customer_id)
dashboard.search_customer(msisdn)
```

Weak:

```python
client.post("/x/y/z")
page.locator("#btn-123").click()
```

### Page Objects should hide UI mechanics

Page Objects should know:

- locators,
- UI actions,
- page-specific waits,
- navigation details.

Tests should know:

- scenario,
- input data,
- expected business result.

### Service Objects should hide HTTP mechanics

Service Objects should know:

- endpoints,
- payloads,
- headers,
- status-code expectations,
- response parsing.

Tests should know:

- business operation,
- input data,
- expected behavior.

### Test data should be deterministic

Tests should not depend on random, unknown, or manually prepared state unless explicitly marked as external or environment-dependent.

### CI should run safe tests by default

CI should run deterministic tests that do not require private environments or live third-party systems.

External tests should be clearly marked and opt-in.

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
