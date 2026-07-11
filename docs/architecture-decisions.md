# Architecture decisions

This file records the main design decisions behind the framework.

It is not a complete architecture specification. It is a map of the decisions
that future maintainers should not have to rediscover from code or commit
history.

---

## Decision 1 — Treat the repository as a framework skeleton, not a product

**Decision:** This repository is positioned as a reusable QA automation
framework skeleton.

It is not a plug-and-play automation solution.

**Reasoning:** Real enterprise applications require project-specific context:
locators, authentication, test data, API contracts, roles, permissions,
business rules, and environment configuration. A public repository cannot
provide those safely or honestly.

**Consequence:** The repository provides structure and examples, but the user
must adapt it to the application under test.

---

## Decision 2 — Keep POM and SOM in one repository, but in separate layers

**Decision:** Page Object Model and Service Object Model live in the same
repository.

They are not merged into one abstraction.

**Reasoning:** Enterprise QA automation often needs both UI and API coverage.
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

**Decision:** The FastAPI services under `services/` are demo infrastructure,
not framework core.

**Reasoning:** They make the skeleton executable and reviewable without access
to a private enterprise system.

**Consequence:** Real users may remove or replace `services/` with their
actual application, public test API, or internal test environment.

---

## Decision 4 — Keep tests organized by level

**Decision:** Tests are grouped into:

```text
tests/unit/
tests/integration/
tests/e2e/
```

**Reasoning:** The test pyramid is a maintenance strategy. Different test
levels answer different questions and have different costs.

**Consequence:** New tests should be added to the level that matches the risk
being tested.

---

## Decision 5 — CI should run deterministic tests by default

**Decision:** CI should prefer deterministic tests that do not depend on
private or unstable live systems.

**Reasoning:** A public skeleton should be runnable and understandable without
secrets, VPN access, or corporate environments.

**Consequence:** External/live tests should be marked explicitly and excluded
from default CI unless deliberately enabled.

---

## Decision 6 — AI may assist adaptation, but QA owns correctness

**Decision:** The repository may be used with AI-assisted development, but AI
output is not treated as correct by default.

**Reasoning:** AI can generate useful structure, but it cannot safely infer
project truth, production risk, or business meaning without review.

**Consequence:** Generated Page Objects, Service Objects, fixtures, and tests
require manual QA review before being trusted.

---

## Decision 7 — Keep evergreen principles outside project documentation

**Decision:** General testing principles live in `AUTOMATION_PRINCIPLES.md`.

**Reasoning:** Principles such as deterministic data, business-readable tests,
and QA ownership of AI-generated output apply beyond this repository.

**Consequence:** Project documentation can stay focused on this framework,
while broader testing rules remain preserved separately.
