# Gaps

Known gaps that are incomplete, intentionally deferred, or still need a clear
decision.

This file tracks work that should not be forgotten. It is not a bug list.

---

## Gap 1 — Realistic POM case study is not implemented yet

The framework currently has simple UI examples, but not a realistic
Salesforce-like or CRM-like business flow.

Planned direction:

```text
Login
→ open Sales or Service area
→ create Case or Opportunity
→ fill required fields
→ save
→ verify status or confirmation
```

Why this matters:

- the POM layer should demonstrate business-readable UI automation,
- Page Objects should model user actions, not just technical selectors,
- the framework needs one realistic browser flow to prove its structure.

Status: planned.

---

## Gap 2 — Stronger SOM case study needs selection

The SOM layer has useful local FastAPI service examples, but it still needs one
stronger business scenario that shows multiple Service Objects working together.

Candidate directions:

- local FastAPI flow: create customer → create order → verify status,
- public API flow marked as external,
- OpenAPI/Swagger-based Service Object draft reviewed by QA.

Why this matters:

- SOM should represent business operations, not just isolated HTTP calls,
- integration tests should protect service contracts and workflow intent,
- the framework needs one clear API scenario comparable to the future POM case
  study.

Status: planned.

---

## Gap 3 — Unit tests do not yet cover the reusable POM/SOM framework core

The current unit test layer verifies the test data/database module well enough
for the present baseline.

That is useful, but it is not the same as unit-level confidence in the
framework itself.

Current unit coverage is mainly focused on:

- `testdata/testdb.py`,
- SQLAlchemy models,
- schema creation,
- model defaults,
- database constraints,
- seed data,
- idempotent initialization,
- session lifecycle.

Missing or weak unit-level coverage:

- `MicroserviceClient`,
- `InMemoryStore`,
- `create_crud_router`,
- Pydantic models in `services/users_service.py`,
- Pydantic models in `services/orders_service.py`,
- Pydantic models in `services/products_service.py`,
- `BaseClient` behavior and HTTP method contracts,
- `api/swagger_generator.py`.

Current status:

```text
Unit tests verify the test data layer well enough for now,
but they do not yet verify the reusable POM/SOM framework core.
```

Status: needs implementation.

---

## Gap 4 — Swagger/OpenAPI generator needs behavior tests and contract alignment

`api/swagger_generator.py` is a lightweight helper for generating first-draft
Service Object code from OpenAPI/Swagger input.

It should stay a scaffolding aid, not a promise of complete test design.

Known follow-up work:

- add focused unit tests for method name generation,
- add tests for tag filtering,
- add tests for generated class names,
- add tests for generated method bodies,
- verify that generated methods only call HTTP methods supported by
  `BaseClient`,
- decide whether `BaseClient` should support `put()` and `delete()` or whether
  the generator should restrict/flag unsupported operations.

Status: needs tests and design decision.

---

## Gap 5 — External/live examples need cleanup and clear policy

The repository contains tests and services that appear to belong to an external
or legacy demo path, such as auth/customer examples and login-related browser
tests.

These examples may still be useful, but their role must stay explicit.

They should be one of:

- documented external examples,
- moved into an examples area,
- rewritten against local demo services,
- or removed if they no longer support the framework story.

Rules to preserve:

- external/live tests must be opt-in,
- default CI must not depend on live third-party systems,
- external examples must not make the framework look less reusable.

Status: partially addressed through markers and CI, but still needs cleanup.

---

## Gap 6 — Current E2E/POM example is still a technical smoke test

The current browser example uses Swagger UI to demonstrate Playwright and Page
Object usage.

That is acceptable as a lightweight smoke test, but it is not a strong POM case
study.

Known limitations:

- it tests documentation UI rather than a real application screen,
- selectors are mostly Swagger-specific,
- assertions are mostly technical,
- the flow does not yet express business intent.

The future POM case study should show:

- screen/page responsibility,
- user-facing actions,
- business-readable test names,
- meaningful assertions,
- clear separation between Page Object interactions and test assertions.

Status: acceptable as smoke, not sufficient as final POM demonstration.

---

## Gap 7 — Reporting and Allure story should be verified against CI

The README mentions reporting, but the exact Allure workflow still needs to be
checked against the current repository behavior.

Open questions:

- what gets attached on UI failures,
- what gets attached on API failures,
- whether CI should publish Allure artifacts,
- which commands should be documented as the recommended local workflow,
- whether reporting should stay optional or become part of the default
  verification path.

Status: needs verification.

---

## Gap 8 — Code generation must stay optional and bounded

`CODEGEN.md` and `api/swagger_generator.py` are useful, but code generation
should not become the main promise of the repository.

Generated code should remain:

- a starting point,
- reviewed by QA,
- refactored into the framework structure,
- covered by tests before being treated as reliable.

Rules to preserve:

- Playwright Codegen helps discover UI interactions, not define test design,
- OpenAPI generation can draft Service Objects, not validate business intent,
- generated selectors and methods must be reviewed before use,
- assertions must remain human-owned.

Status: documented, but should be reinforced as generator tests are added.

---

## Gap 9 — Dependency and runner compatibility should be revisited later

The CI runner is currently pinned for compatibility with the pinned Playwright
version.

This is acceptable as a focused fix, but it should not be forgotten.

Future cleanup:

- review pinned dependency versions,
- decide when to update Playwright,
- decide whether the CI runner can safely return to `ubuntu-latest`,
- keep dependency changes separate from framework behavior changes.

Status: deferred.

---

## Gap 10 — Framework confidence should grow beyond green CI

The pipeline now checks syntax, pytest collection, and the current test suite.

That is a stronger baseline than only running pytest, but it is still not full
framework confidence.

Future confidence should come from:

- unit tests for reusable framework pieces,
- integration tests that show meaningful SOM workflows,
- realistic POM case study,
- clear external-test policy,
- reporting verification,
- generator behavior tests,
- documentation that matches actual behavior.

Status: ongoing.
