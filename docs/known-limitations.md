# Known limitations

Things that are known to be incomplete, demo-only, or outside the current scope.

These are documented intentionally so the repository does not overclaim.

---

## Scope boundaries

- This repository is a **framework skeleton**, not a ready-made automation
  product.
- It does not automate Salesforce or any other enterprise platform out of the
  box.
- It does not contain real corporate locators, credentials, endpoints, or
  business rules.
- It does not replace domain analysis or QA review.
- It does not provide self-healing automation.
- It is not an AI agent.

---

## Demo implementation boundaries

The `services/` directory contains local FastAPI example services.

They exist to make the framework executable and to demonstrate SOM-style API
testing.

They are not intended to model a full production system.

A real project may replace them entirely.

---

## POM limitations

- Current Page Objects are demonstration-level.
- They do not yet include a realistic Salesforce-like flow.
- They rely on simplified selectors and flows.
- They do not cover advanced UI problems such as heavy SPA re-rendering,
  complex modals, Shadow DOM, or dynamic permissions.

Those topics may be addressed in future case studies, but they are not part of
the current core skeleton.

---

## SOM limitations

- Current Service Objects demonstrate the pattern, but not every production API
  concern.
- Authentication, retries, pagination, schema validation, and contract testing
  may need project-specific expansion.
- Generated Service Objects require review and cleanup before being trusted.

---

## Test data limitations

- Example data is small and simplified.
- The repository does not solve test data management for real enterprise
  environments.
- Seeding, cleanup, isolation, permissions, and state reset must be adapted per
  project.

---

## CI limitations

- CI should run deterministic tests by default.
- External tests should be opt-in.
- Any test requiring secrets, VPN, or live third-party systems must be clearly
  marked and excluded from default runs.

---

## AI-assisted adaptation limitations

AI can help adapt the skeleton, but it cannot safely decide:

- which scenario matters,
- which assertion is meaningful,
- which data is valid,
- whether a locator is stable,
- whether an API contract is correct,
- whether a test belongs at UI, API, or unit level.

Generated code must be reviewed before it is trusted.
