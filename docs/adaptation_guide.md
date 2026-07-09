# Adaptation guide

This guide explains how to adapt `qa-automation-framework` to a real project.

The repository provides the skeleton. A real project provides the application, domain, data, selectors, endpoints, authentication, and business rules.

## Adaptation mindset

Do not copy the skeleton blindly.

Treat it as a starting architecture:

```text
framework structure + project context + manual QA review = useful automation
```

The framework becomes valuable only after it is connected to real domain behavior.

## Step 1 — Define the target scope

Before changing code, decide what kind of tests the project needs first.

Questions:

- Is the first priority UI, API, or both?
- Which workflows are business-critical?
- Which failures would be expensive in production?
- Which environments are stable enough for automation?
- Which data can be created safely by tests?
- Which data must be prepared manually?
- Which systems are out of scope?

Example scope:

```text
Initial scope:
- smoke login flow through UI
- create Case through UI
- fetch Case details through API
- verify required fields and status

Out of scope:
- production environment
- destructive operations
- end-to-end billing chain
- performance testing
```

## Step 2 — Map the domain

Create a short domain map before writing Page Objects or Service Objects.

Example CRM domain map:

```text
User roles:
- sales agent
- service agent
- manager

Objects:
- account
- contact
- case
- opportunity

Critical workflows:
- create case
- update case status
- create opportunity
- move opportunity to next stage
```

Example telco domain map:

```text
Objects:
- customer
- account
- contract
- subscription
- order
- invoice

Critical workflows:
- search customer by MSISDN
- change customer plan
- suspend account
- verify invoice status
```

The domain map should drive names in `pages/`, `api/`, and `tests/`.

## Step 3 — Configure environments

Move environment-specific values into configuration.

Typical values:

```text
BASE_URL
API_BASE_URL
USERNAME
PASSWORD
AUTH_TOKEN
TENANT_ID
ENVIRONMENT_NAME
```

Avoid hardcoding environment values inside tests.

Recommended approach:

- local defaults in settings,
- environment variables for real values,
- secrets managed by CI or local `.env`,
- no real secrets in Git.

## Step 4 — Adapt the POM layer

Update or add Page Objects in:

```text
pages/
components/
```

Recommended process:

1. Identify one critical UI flow.
2. Record or inspect the flow manually.
3. Collect stable locators.
4. Create one Page Object per meaningful page or view.
5. Extract shared UI pieces into components only when reuse is real.
6. Keep assertions in tests.
7. Add waits where the application is genuinely dynamic.

Do not start by modeling the entire application.

Start with one valuable flow.

## Step 5 — Adapt the SOM layer

Update or add Service Objects in:

```text
api/
```

Recommended process:

1. Identify the API boundary needed by the tests.
2. Review available API documentation.
3. Add domain-level methods.
4. Keep raw HTTP mechanics in the base client.
5. Add response handling and useful errors.
6. Write integration tests around business operations.

Good Service Object method names:

```python
case_service.create_case(...)
case_service.get_case_status(...)
opportunity_service.move_to_stage(...)
customer_service.get_customer_by_msisdn(...)
```

Weak names:

```python
service.get(...)
service.post(...)
service.call_endpoint(...)
```

## Step 6 — Replace test data

Update:

```text
testdata/
mocks/
```

Decide which data is:

- static seed data,
- created dynamically by tests,
- mocked,
- manually prepared,
- forbidden to touch.

A test data strategy is required for stable automation.

Without it, even well-written tests become flaky.

## Step 7 — Rebuild tests by level

Use the test pyramid.

```text
tests/unit/          pure logic, data models, helpers
tests/integration/   APIs, contracts, service behavior
tests/e2e/           critical UI flows
```

Do not force every scenario into E2E.

If a behavior can be tested reliably through API, prefer integration tests.

Use UI tests for workflows where browser behavior matters.

## Step 8 — Mark external dependencies

Tests that require live systems should be explicitly marked.

Examples:

```python
@pytest.mark.external
@pytest.mark.salesforce
@pytest.mark.uat
```

Default CI should run deterministic tests.

Live environment tests should be opt-in.

## Step 9 — Add reporting gradually

Allure or another report layer should help answer:

- what scenario failed,
- what data was used,
- what environment was used,
- what API response or UI state was observed,
- what business behavior was affected.

Do not add reporting noise before the test intent is clear.

## Step 10 — Review with a QA checklist

Before accepting the adapted framework, ask:

- Does the folder structure still reflect POM and SOM boundaries?
- Are tests readable without opening Page Objects or Service Objects?
- Are selectors hidden inside Page Objects?
- Are endpoints hidden inside Service Objects?
- Is test data deterministic?
- Are environment-specific values outside the test logic?
- Are external tests marked?
- Does CI run only safe tests by default?
- Are business assertions meaningful?
- Could another QA engineer maintain this after onboarding?

## Minimal first real adaptation

A realistic first target is not a full enterprise test suite.

A good first target is:

```text
1 UI smoke test
1 UI business flow
1 API integration flow
1 negative API test
1 data setup fixture
1 CI-safe execution path
```

That is enough to prove the skeleton works in a real context without overbuilding.
