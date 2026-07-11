# Adaptation guide

How to adapt this framework skeleton to a real project.

---

## Step 1 — Identify the application layers

List what you need to test:

- UI flows,
- APIs,
- database/state,
- background jobs,
- external integrations,
- reports,
- permission models.

Then decide which layer each scenario belongs to:

- unit,
- integration/API,
- E2E/UI.

---

## Step 2 — Replace the UI layer

Update or add Page Objects in:

```text
pages/
components/
```

Replace demo locators and actions with real application behavior.

Do not put raw selectors directly into tests.

---

## Step 3 — Replace the API layer

Update or add Service Objects in:

```text
api/
```

Replace demo endpoints with real project APIs.

Service methods should describe business operations, not just HTTP calls.

---

## Step 4 — Replace test data

Update:

```text
testdata/
mocks/
```

Define:

- required users,
- roles,
- permissions,
- reference data,
- cleanup strategy,
- generated values,
- environment-specific constraints.

---

## Step 5 — Configure environments

Move environment-specific values into settings or environment variables.

Examples:

```bash
BASE_URL=https://your-app.example.com
API_BASE_URL=https://your-api.example.com
```

Tests should not hardcode environment URLs or credentials.

---

## Step 6 — Add tests gradually

Start with the safest layer.

Recommended order:

1. unit tests for local logic and models,
2. API tests through Service Objects,
3. only then E2E tests for critical user flows.

Do not use E2E tests for everything.

---

## Step 7 — Mark external tests

Any test requiring live external systems should be explicitly marked:

```python
@pytest.mark.external
```

Default local and CI runs should exclude external tests unless deliberately
enabled.

---

## Step 8 — Review with QA judgment

Before accepting new automation, check:

- Is the scenario worth automating?
- Is this the right test level?
- Is the assertion meaningful?
- Is the data controlled?
- Will the failure be diagnostic?
- Can the test be maintained under change?

The skeleton helps with structure. QA still owns the testing decision.
