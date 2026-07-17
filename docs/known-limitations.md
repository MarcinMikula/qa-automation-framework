# Known limitations

Things that are known to be incomplete, intentionally simplified, or outside
the current scope.

These limitations are documented so the repository does not overclaim.

---

## Scope boundaries

- This repository is a framework skeleton, not a ready-made automation product.
- It does not contain real project credentials, endpoints, locators, or business
  rules.
- It does not replace test analysis, domain knowledge, or human review.
- It is not an AI agent.
- It does not provide self-healing automation.
- It has not yet passed framework acceptance against a concrete project need.

---

## Evidence boundary

Current green tests and CI show that committed checks pass.

They provide evidence for:

- Python syntax,
- pytest collection,
- reusable helper behavior,
- local service integration,
- local browser examples,
- deterministic CI execution.

They do not prove that:

- the framework is easy to adapt,
- the guidance works for a lower-programming-skills user,
- the correct project risks will be selected,
- every real application concern is supported,
- the skeleton is production-ready.

Framework acceptance is required before making stronger claims.

---

## Local target boundaries

The local FastAPI services and demo shop exist only to exercise the framework.

They do not model:

- a complete e-commerce platform,
- production authentication,
- realistic permissions,
- external providers,
- distributed transactions,
- event-driven processing,
- complex enterprise state.

They should remain minimal.

A real project may remove or replace them entirely.

---

## POM limitations

- Current Page Objects exercise a small deterministic e-commerce flow and a
  Swagger UI smoke example.
- They use simplified local selectors and application behavior.
- They do not validate advanced UI concerns such as complex re-rendering,
  overlays, frames, Shadow DOM, dynamic permissions, or difficult
  authentication.
- `BasePage` and `BaseComponent` have not yet been validated through a full
  real-project adaptation.
- More demo Page Objects should not be added merely to make the repository look
  complete.

---

## SOM limitations

- Current Service Objects demonstrate readable neutral `User`, `Product`, and
  `Order` examples.
- They do not cover every production API concern.
- Authentication, pagination, retries, polling, idempotency, rate limits,
  asynchronous operations, and provider-specific error handling remain
  project-specific.
- Generated Service Objects are scaffolding and require review.
- The neutral examples are not universal business contracts.

---

## Test data limitations

- Example data is small and deterministic.
- The repository does not solve test-data management for real environments.
- Ownership, isolation, cleanup, permissions, privacy, and state reset must be
  designed per project.
- The SQLAlchemy example demonstrates mechanics, not a complete persistence
  strategy.

---

## Testing and CI limitations

- Default CI intentionally uses local deterministic checks.
- External tests requiring secrets, VPN access, private systems, or unstable
  third parties are excluded by default.
- A green pipeline does not prove risk coverage or assertion quality.
- Published Allure reporting is not part of the current baseline.
- The workflow remains pinned to Ubuntu 22.04 because of the current
  Playwright/dependency compatibility boundary.
- Dependency and runner modernization is a separate maintenance task.

---

## Adaptation guidance limitations

- The human-led guide is an initial implementation.
- It has not yet been validated through framework acceptance.
- It may still be too detailed, unclear, or incomplete for some users.
- The repository does not yet contain the final AI-assisted adaptation guide.
- File-placement guidance cannot replace real project architecture knowledge.

---

## AI-assisted adaptation limitations

AI may help draft framework content.

It cannot safely decide alone:

- whether the project need is valuable,
- which risk matters,
- whether a scenario should exist,
- whether the selected test level is appropriate,
- whether data is valid,
- whether a locator is stable,
- whether an API contract is current,
- whether an assertion is meaningful.

AI output requires human review and executable evidence.

The dedicated comparison has not yet been performed.

---

## Reusability limitation

One successful adaptation will be useful evidence.

It will not prove that the skeleton is equally effective for every:

- UI architecture,
- service topology,
- domain,
- team,
- environment,
- maturity level.

Claims should remain proportional to the evidence collected.
