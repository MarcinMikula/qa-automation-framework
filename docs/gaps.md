# Gaps

Known gaps that are incomplete, intentionally deferred, or still need a clear
decision.

This file tracks work that should not be forgotten. It is not a bug list.

The project now has a stronger framework baseline than before:

- CI syntax check through `compileall`,
- pytest collection check,
- unit coverage for the core SOM helpers,
- integration coverage for local FastAPI services,
- lightweight CI report artifacts,
- documented framework consistency gates.

The remaining gaps are mostly about realistic usage, external examples,
reporting, and final usefulness validation.

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
- the framework needs one realistic browser flow to prove its structure,
- this is required before claiming that the POM side is practically useful.

Status: planned.

---

## Gap 2 — Stronger SOM case study still needs selection

The SOM layer has useful local FastAPI service examples and stronger unit
coverage now, but it still needs one clearer business scenario that shows
multiple Service Objects working together.

Candidate directions:

- local FastAPI flow: create customer → create order → verify status,
- public API flow marked as external,
- OpenAPI/Swagger-based Service Object draft reviewed by QA.

Why this matters:

- SOM should represent business operations, not only isolated HTTP calls,
- integration tests should protect service contracts and workflow intent,
- the framework needs one clear API scenario comparable to the future POM case
  study.

Status: planned.

---

## Gap 3 — External/live examples need cleanup and clear policy

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
- external examples must not make the framework look less reusable,
- tests that require private credentials must never be part of default CI.

Status: partially addressed through markers and CI, but still needs cleanup.

---

## Gap 4 — Current E2E/POM example is still a technical smoke test

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

## Gap 5 — Reporting and Allure dashboard are still future work

The CI now produces lightweight pytest reports and workflow summaries.

That improves visibility, but it is not the same as a full Allure dashboard.

Current lightweight reporting:

- JUnit XML files,
- captured pytest output,
- GitHub Actions step summary,
- downloadable `pytest-reports` artifact.

Future reporting work:

- generate Allure results,
- generate a static Allure HTML report,
- decide whether to publish it through GitHub Pages,
- decide which artifacts are useful for UI and API failures,
- document the local and CI reporting workflow.

Status: lightweight reporting added; Allure dashboard deferred.

---

## Gap 6 — Dependency and runner compatibility should be revisited later

The CI runner is currently pinned to `ubuntu-22.04` for compatibility with the
pinned Playwright version.

This is acceptable as a focused fix, but it should not be forgotten.

Future cleanup:

- review pinned dependency versions,
- decide when to update Playwright,
- decide whether the CI runner can safely return to `ubuntu-latest`,
- keep dependency changes separate from framework behavior changes.

Status: deferred.

---

## Gap 7 — Final framework usefulness validation is still open

This is the most important final project question:

```text
Does this framework skeleton actually help automate a concrete application?
```

The project should not be judged only by:

- green CI,
- number of tests,
- documentation quality,
- nice folder structure,
- internal unit/integration coverage.

The final validation should apply the skeleton to a concrete or realistic
application context and check whether it actually helps.

Planned validation approach:

```text
Choose a realistic application context
→ manually fill the framework with application-specific content
→ add Page Objects / Service Objects / fixtures / test data
→ write meaningful tests
→ observe where the framework helps or gets in the way
→ document gaps, friction, and improvements
```

For this validation phase, the framework should be filled manually first.

Reason:

```text
If LLM-generated filling is used too early,
we would mix two questions:

1. Is the framework skeleton useful?
2. Did the LLM fill it correctly?
```

Manual adaptation gives a cleaner answer to the framework question.

Status: parked for final validation phase.

---

## Gap 8 — Formal framework testing phase should be designed later

After the current development phase, the framework should be tested more
systematically.

This should be closer to ISTQB-style thinking:

- define framework requirements,
- separate test levels,
- define what each level proves,
- map tests to requirements or risks,
- identify gaps,
- execute and summarize results.

Some test levels already exist:

- syntax check,
- collection check,
- unit tests,
- integration tests,
- E2E smoke tests.

But the final framework testing phase should be more explicit.

Possible questions:

- What are the functional requirements of the framework?
- What are its non-functional requirements?
- Which requirements are covered by unit tests?
- Which require integration tests?
- Which require a realistic app-context validation?
- Which parts remain out of scope?

Status: parked for later.

---

## Gap 9 — Context-aware framework filler is parked

A possible future tool could use this framework skeleton together with
application context to propose project-specific automation artifacts.

This would not be Playwright Codegen 2.0.

It should answer:

```text
Where should this element, action, endpoint, or flow live in the framework?
```

not only:

```text
How can Playwright interact with this element?
```

Possible future architecture:

- local CLI agent,
- replaceable LLM backend,
- repository context,
- application context,
- deterministic UI/API collectors,
- structured JSON output,
- human QA review loop.

This idea should stay parked until the framework has been manually validated
against a realistic application context.

Status: future idea, not current scope.

---

## Recently closed or improved gaps

The following gaps were reduced by recent commits:

### Unit coverage for reusable SOM framework pieces

Added or improved unit coverage for:

- `InMemoryStore`,
- `create_crud_router`,
- `MicroserviceClient`,
- local service Pydantic models,
- `BaseClient`,
- `api/swagger_generator.py`.

### CRUD create contract

Unit tests exposed that `create_item()` was storing only explicitly provided
fields, which dropped Pydantic defaults.

The create path now stores full validated payloads, while the update path still
uses partial updates.

### `BaseClient` HTTP method coverage

`BaseClient` now supports:

- `GET`,
- `POST`,
- `PUT`,
- `PATCH`,
- `DELETE`.

This aligns it with methods that the OpenAPI/Swagger generator may emit.

### Swagger/OpenAPI generator behavior

`api/swagger_generator.py` now has behavior tests for:

- name normalization,
- class name generation,
- tag filtering,
- method name generation,
- generated method rendering,
- unsupported method filtering,
- empty-tag fallback behavior.

### Framework consistency gates

Testing strategy now explicitly documents:

```text
syntax check
→ collection check
→ unit tests
→ integration tests
→ E2E tests
```

This helps explain what the green pipeline actually proves.