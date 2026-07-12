# Learnings

Project journal for lessons learned while building and adapting this framework.

This file is intentionally lighter than PhoenixQA's `LEARNINGS.md`.

PhoenixQA is a research-heavy self-healing project with many architecture
pivots. This repository is simpler: it is a reusable POM/SOM framework skeleton
that should become more interesting when it is adapted to a real application.

The goal of this file is not to duplicate all documentation.

Use the dedicated documents for stable reference material:

- [`README.md`](README.md) — repository landing page.
- [`AUTOMATION_PRINCIPLES.md`](AUTOMATION_PRINCIPLES.md) — evergreen automation principles.
- [`PHILOSOPHY.md`](PHILOSOPHY.md) — project-specific framework philosophy.
- [`docs/`](docs/) — architecture decisions, gaps, limitations, testing strategy, and guides.

This file should capture what changed in understanding while the project was
being built.

---

## Current phase: framework skeleton

The current phase is about making the repository coherent as a practical QA
automation framework skeleton.

The main work is not advanced algorithm design.

The main work is:

- clarifying scope,
- separating framework core from demo implementation,
- making POM and SOM boundaries explicit,
- documenting how the skeleton should be adapted,
- keeping tests organized by level,
- avoiding overclaiming.

The repository should be understandable before it becomes more ambitious.

---

## Lesson 1 — A framework skeleton must not overclaim

The early version of the repository could be read as if it tried to be a full
enterprise automation framework.

That was too broad.

A public repository cannot honestly provide automation for an unknown
enterprise system because it does not know:

- the real application,
- stable locators,
- authentication rules,
- API contracts,
- domain data,
- permissions,
- environment constraints,
- business-critical assertions.

The better positioning is:

> This repository provides the structure. The real project provides the truth.

That makes the framework more credible and easier to adapt.

---

## Lesson 2 — POM and SOM can live together if their boundaries are explicit

Combining Page Object Model and Service Object Model in one repository is not a
problem by itself.

The problem appears when the documentation makes them look like one mixed
abstraction.

The clearer model is:

```text
pages/   -> UI adapter layer
api/     -> API/service adapter layer
```

POM and SOM can share:

- fixtures,
- settings,
- test data,
- reporting,
- CI structure,
- test organization.

But they should not hide their different responsibilities.

POM models user interactions.

SOM models API/service operations.

The test should use whichever layer fits the risk being checked.

---

## Lesson 3 — Demo services are useful, but they must be labeled as replaceable

The local FastAPI services are useful because they make the framework runnable
without access to a private system.

They help demonstrate:

- Service Object structure,
- integration tests,
- local API flows,
- CI-safe examples.

But they are not the product.

They should be treated as example implementation, not framework core.

A real project may remove or replace them completely.

This distinction should be visible in documentation, otherwise the repository
starts to look like a demo app instead of a framework skeleton.

---

## Lesson 4 — Test level matters more than test count

The framework should not aim to maximize the number of tests.

It should make it easier to place tests at the right level.

Useful distinction:

```text
Unit          -> small deterministic logic
Integration  -> API/service contracts and boundaries
E2E/UI        -> critical user-facing flows
```

A UI test is not automatically better because it is closer to the user.

An API test is not automatically sufficient because it is faster.

A unit test is not automatically valuable because it is cheap.

The correct level depends on the risk.

This is why the folder structure matters:

```text
tests/unit/
tests/integration/
tests/e2e/
```

The structure should guide test design.

---

## Lesson 5 — Test data and state are not secondary details

Test data is part of the test design.

During earlier work, one important integration-testing trap became clear:

> Do not assert exact auto-increment IDs when the storage layer does not reset
> counters between tests.

For example, in local in-memory services or database-backed examples, cleanup
may remove records without resetting ID counters.

A safer assertion may be:

```python
assert created_entity["id"] > 0
```

instead of:

```python
assert created_entity["id"] == 1
```

The broader lesson is that automation must understand state.

If state is not controlled, tests become fragile.

If state is not visible, failures become harder to diagnose.

---

## Lesson 6 — AI helps create drafts, not trusted automation

AI can speed up work on a framework skeleton.

It can help generate:

- Page Objects,
- Service Objects,
- fixtures,
- mock data,
- test skeletons,
- documentation.

But generated automation is only a draft.

A QA engineer still needs to verify:

- whether the scenario matters,
- whether the test belongs at the right level,
- whether the data is realistic,
- whether the assertion is meaningful,
- whether the locator or endpoint is real,
- whether the failure would help diagnose a real issue.

This lesson is important enough that the detailed rules were moved to
[`AUTOMATION_PRINCIPLES.md`](AUTOMATION_PRINCIPLES.md).

---

## Lesson 7 — Documentation structure matters before code expansion

Before adding more code, the repository needed clearer documentation.

The cleanup created a stronger separation:

```text
README.md                    -> landing page
AUTOMATION_PRINCIPLES.md     -> evergreen testing rules
PHILOSOPHY.md                -> project-specific rationale
docs/                        -> framework documentation
LEARNINGS.md                 -> project journal
```

This makes later work safer.

When the framework is adapted to a real application, new code changes can be
judged against the documented scope instead of reinventing the project direction
each time.

---

## Lesson 8 — Keep the skeleton boring until real usage proves otherwise

This project should not become complex too early.

For now, boring is good:

- clear folders,
- readable Page Objects,
- readable Service Objects,
- simple fixtures,
- deterministic examples,
- explicit limitations,
- safe CI defaults.

More advanced patterns should be added only when real usage justifies them.

The framework should change because a real test case exposed a need, not
because the architecture could theoretically become more impressive.

---

## Future learning area: real application adaptation

The most valuable future learnings will appear when this framework is used
against a realistic application.

That phase may change the framework more than the initial skeleton work.

Expected learning areas:

### Salesforce-like UI adaptation

Questions to capture later:

- How much of the current POM structure survives a heavy SPA UI?
- Which locator strategy works best?
- Which waits are framework-level and which are page-specific?
- How should modals, tabs, dynamic forms, and validation messages be modeled?
- Where do Page Objects become too large?
- Which flows are worth E2E automation?

### API / SOM adaptation

Questions to capture later:

- Are current Service Objects expressive enough?
- How should authentication be handled?
- Is response validation too weak or too heavy?
- Should contracts be checked with schemas or typed models?
- How should test data setup be shared between API and UI tests?

### Test data and state

Questions to capture later:

- What state must be created through API before UI tests?
- What state can be mocked?
- What needs cleanup?
- Which tests can run repeatedly?
- Which tests require known seeded records?

### Framework changes caused by real usage

Track any changes that real usage forces, such as:

- new base page helpers,
- better service client behavior,
- retry or timeout policy,
- improved fixtures,
- stronger reporting,
- Allure conventions,
- environment profiles,
- external/live test markers.

This is where `LEARNINGS.md` should grow.

Not because the skeleton needs more notes now, but because real usage will
expose real trade-offs.

---

## Current status

The documentation has been reorganized around a more realistic scope.

Current shape:

- the repository is a POM/SOM framework skeleton,
- POM and SOM are separate adapter layers,
- demo services are replaceable examples,
- evergreen principles are preserved separately,
- project-specific docs live in `docs/`,
- the next major source of learning should be real-world adaptation.

The project is now ready to move from documentation cleanup toward code review,
test verification, and realistic case studies.
