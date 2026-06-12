# qa-automation-framework
![Tests](https://github.com/MarcinMikula/llm-qa-toolkit/actions/workflows/llm-qa.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> A structured QA framework skeleton — bring your own application, fill in the blanks.

Not a plug-and-play tool. A **skeleton** — built on proven patterns (POM, SOM, ISTQB pyramid), 
ready to be filled with project-specific content: your locators, your endpoints, your test data.

---

## What this is

A reusable framework structure for testing enterprise applications in regulated industries 
(telco, banking, insurance, e-commerce).

You get the architecture. You provide the application.

- Page Object Model classes → add your locators and UI actions
- Service Object Model classes → add your endpoints and business logic  
- Test data layer → replace seed data with your domain objects
- pytest fixtures and hooks → extend with your setup/teardown needs
- CI/CD pipeline → plug in your environment variables and run

The skeleton ships with **working examples** built on local FastAPI microservices 
(users, orders, products) so you can see every pattern in action before replacing 
it with real application code.

---

## When to use this

- Starting a new QA automation project from scratch
- Standardizing test structure across multiple projects
- Onboarding a new team member who needs a reference implementation
- Demonstrating QA engineering practices in a code review or interview

---

## Stack

| Layer | Technology |
|---|---|
| UI (E2E) | Playwright + pytest |
| API | httpx + Service Object Model |
| Test data | SQLAlchemy (SQLite) |
| Reporting | Allure |
| CI/CD | GitHub Actions |
| Example backend | FastAPI (local microservices) |

---

## Project structure
qa-automation-framework/
├── services/           # Example FastAPI microservices (users, orders, products)
│                       # Replace with your application under test
├── testdata/           # SQLAlchemy models, seed data, environment settings
│                       # [DOMAIN: TELCO] examples — adapt to your domain
├── pages/              # Page Object Model — UI layer
│                       # Add your locators and page actions here
├── components/         # Reusable UI components
├── api/                # Service Object Model — API layer
│                       # Add your endpoints and business methods here
├── mocks/              # Mocked API responses
└── tests/
├── unit/           # Unit tests — models, constraints, defaults
├── integration/    # API tests through SOM
└── e2e/            # End-to-end tests through POM + Playwright

---

## Domain annotations

Code throughout this skeleton is annotated with domain markers:

```python
# [DOMAIN: TELCO]   — specific to telecommunications (msisdn, plan, contract_type)
# [DOMAIN: ECOM]    — specific to e-commerce
# [DOMAIN: GENERIC] — universal, works in any domain
```

When adapting to a new project, search for `[DOMAIN: TELCO]` to find everything 
that needs replacing with your domain's concepts.

---

## Test coverage (example implementation)
tests/unit/          →  26 tests   (models, constraints, seed data)
tests/integration/   →  34 tests   (API layer through SOM)
tests/e2e/           →   2 tests   (UI layer through POM + Playwright)
─────────────────────────────────────────────────────────────────────
Total:                  62 tests   — all green, CI verified

Tests marked `@pytest.mark.external` require live external services 
and are skipped in CI automatically.

---

## How to use this skeleton

### 1. Clone and install

```bash
git clone https://github.com/MarcinMikula/qa-automation-framework.git
cd qa-automation-framework
pip install -r requirements.txt
python -m playwright install chromium
```

### 2. Run the example implementation

```bash
# Start example microservices
python -m services.users.main &
python -m services.orders.main &
python -m services.products.main &

# Initialize test database
python testdata/testdb.py

# Run all tests
python -m pytest tests/ -v -m "not external"

# Allure report
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### 3. Adapt to your project

| What to replace | Where |
|---|---|
| UI locators and page actions | `pages/` |
| API endpoints and methods | `api/` |
| Domain models and seed data | `testdata/testdb.py` |
| Environment URLs | `testdata/settings.py` |
| Example microservices | `services/` (or remove entirely) |

### 4. Generate Service Object from Swagger

```bash
python api/swagger_generator.py --swagger path/to/swagger.json --tag customers
```

---

## Environment configuration

Environment variables override defaults from `testdata/settings.py`:

```bash
BASE_URL=https://your-app.com \
API_BASE_URL=https://your-api.com \
pytest tests/ -v
```

---

## Design philosophy

- **ISTQB test pyramid** — unit → integration → E2E, in that order
- **POM and SOM** — tests speak business language, not HTTP or CSS
- **Deterministic test data** — seed is fixed, tests are reproducible
- **Domain-annotated** — every domain-specific assumption is marked and replaceable
- **CI-first** — all tests run on GitHub Actions on every push

Full design rationale: [PHILOSOPHY.md](PHILOSOPHY.md)  
Lessons learned during development: [LEARNINGS.md](LEARNINGS.md)

---

## Tooling

Developed with AI assistance:
- Cursor IDE
- Claude Sonnet (Anthropic)

> Every generated piece of code is verified and accepted by the author.