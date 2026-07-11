# Gaps

Known gaps that are incomplete, intentionally deferred, or still need a clear
decision.

This file tracks work that should not be forgotten. It is not a bug list.

---

## Gap 1 — Realistic POM case study is not implemented yet

The framework currently has simple UI examples, but not a realistic
Salesforce-like CRM flow.

Planned direction:

```text
Login
→ open Sales or Service area
→ create Case or Opportunity
→ fill required fields
→ save
→ verify status or confirmation
```

Status: planned.

---

## Gap 2 — Public or realistic SOM case study needs selection

The SOM layer needs one stronger API case study that demonstrates business
operations rather than isolated HTTP calls.

Candidate directions:

- local FastAPI flow: create customer → create order → verify status,
- public API flow marked as external,
- generated Service Object from OpenAPI/Swagger.

Status: planned.

---

## Gap 3 — `PHILOSOPHY.md` still contains older project narrative

The root `PHILOSOPHY.md` contains useful ideas, but it predates the clearer
POM/SOM framework positioning.

Now that `AUTOMATION_PRINCIPLES.md` exists, `PHILOSOPHY.md` can be rewritten
as a shorter project-specific rationale or retired later.

Status: pending.

---

## Gap 4 — `LEARNINGS.md` needs conversion into a cleaner project journal

`LEARNINGS.md` contains useful context and development history, but it should
be cleaned up so it reads as a project journal rather than mixed notes.

Status: pending.

---

## Gap 5 — Some examples may still look more telco-specific than generic

The repository intentionally contains telco/CRM/billing examples, but the
documentation should make clear which concepts are domain examples and which
are reusable framework mechanics.

Status: partially addressed through domain markers and documentation.

---

## Gap 6 — External/live test policy needs enforcement in code

Documentation says external tests should be opt-in and excluded from default
CI. The pytest marker and CI behavior should be verified against the current
test suite.

Status: needs verification.

---

## Gap 7 — Allure/reporting story should be verified and documented against CI

The README mentions Allure, but the exact local and CI reporting workflow should
be checked and kept consistent with repository behavior.

Status: needs verification.

---

## Gap 8 — Codegen should stay optional and clearly bounded

`CODEGEN.md` and `api/swagger_generator.py` are useful, but code generation
should not become the main promise of the repository.

Generated Service Objects should be treated as starting points, not complete
test design.

Status: documented, but needs final cleanup after code review.
