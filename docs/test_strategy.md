# Test strategy

The framework follows a practical test pyramid.

The goal is not to maximize the number of tests. The goal is to place each test at the cheapest reliable level.

```text
        E2E / UI
      Playwright + POM
     critical user flows

    Integration / API
       httpx + SOM
 contracts, services, APIs

       Unit tests
 models, helpers, constraints
```

## Test levels

### Unit tests

Location:

```text
tests/unit/
```

Use unit tests for:

- pure functions,
- data models,
- validation rules,
- constraints,
- deterministic helpers,
- edge cases.

Unit tests should be fast, isolated, and safe to run on every commit.

They should not require:

- browser,
- live API,
- real database server,
- external environment,
- manual test data.

### Integration tests

Location:

```text
tests/integration/
```

Use integration tests for:

- API behavior,
- Service Object methods,
- contract assumptions,
- response structure,
- local microservice behavior,
- cross-layer communication.

Integration tests should usually go through Service Objects rather than raw HTTP calls.

They should answer:

```text
Does this service boundary behave the way the framework expects?
```

### E2E / UI tests

Location:

```text
tests/e2e/
```

Use E2E tests for:

- critical user journeys,
- browser-specific behavior,
- UI rendering and interaction,
- workflows that cannot be validated through API alone.

E2E tests should usually go through Page Objects.

They should be fewer than unit and integration tests because they are slower, more expensive, and more fragile.

## Where a test belongs

Ask one question first:

```text
What is the cheapest reliable layer that can verify this behavior?
```

| Scenario | Preferred level |
|---|---|
| Validate model default value | Unit |
| Validate required field rule in helper logic | Unit |
| Verify API returns expected status and fields | Integration |
| Verify service operation changes backend state | Integration |
| Verify login form can be submitted in browser | E2E |
| Verify user can create a business object through UI | E2E |
| Verify complete cross-system workflow | E2E or dedicated environment test |

## Pytest markers

Recommended marker strategy:

```python
@pytest.mark.unit
@pytest.mark.integration
@pytest.mark.e2e
@pytest.mark.external
@pytest.mark.smoke
@pytest.mark.regression
```

Meaning:

| Marker | Meaning |
|---|---|
| `unit` | Pure isolated unit test. |
| `integration` | API, service, or cross-layer test. |
| `e2e` | Browser-level user flow. |
| `external` | Requires live external dependency or non-local environment. |
| `smoke` | Small high-value test set for quick confidence. |
| `regression` | Broader suite for deeper validation. |

External tests should not run in default CI unless explicitly enabled.

## Default execution

Run all safe tests:

```bash
python -m pytest tests/ -v -m "not external"
```

Run only unit tests:

```bash
python -m pytest tests/unit/ -v
```

Run only integration tests:

```bash
python -m pytest tests/integration/ -v -m "not external"
```

Run only E2E tests:

```bash
python -m pytest tests/e2e/ -v
```

Run external tests explicitly:

```bash
python -m pytest tests/ -v -m external
```

## CI strategy

CI should run deterministic tests by default.

Default CI should include:

- dependency installation,
- Playwright browser installation if E2E tests run,
- test database initialization,
- local demo services startup,
- unit tests,
- integration tests excluding external tests,
- E2E tests that do not require private environments.

CI should avoid:

- real production systems,
- private UAT dependencies unless explicitly configured,
- destructive operations,
- unstable external APIs,
- secrets committed to the repository.

## Test data strategy

Stable tests need stable data.

Prefer:

- deterministic seed data,
- isolated fixtures,
- local test database,
- cleanup after test-created entities,
- unique identifiers when tests create data,
- mock data for scenarios outside current scope.

Avoid:

- assumptions about auto-increment IDs,
- shared mutable state,
- manually prepared data with unclear ownership,
- tests that depend on execution order,
- random values without traceability.

## UI test strategy

UI tests should focus on critical user journeys.

Good UI test candidates:

- login smoke,
- create Case,
- create Opportunity,
- search customer,
- submit order,
- verify visible status change.

Poor UI test candidates:

- every validation rule that can be tested through API,
- every field combination,
- visual layout checks without clear requirement,
- scenarios that require complex manual data setup.

## API test strategy

API tests should verify service behavior and contract assumptions.

Good API test candidates:

- create entity,
- fetch entity by ID,
- validate required fields,
- validate error response,
- verify status transitions,
- verify response schema,
- verify unauthorized access behavior.

API tests are often a better first layer than UI tests because they are faster and easier to diagnose.

## Failure interpretation

A good test failure should help answer:

- what scenario failed,
- what layer failed,
- what data was used,
- what expected behavior was violated,
- whether the failure is likely UI, API, data, environment, or test-code related.

If a failure only says `TimeoutError` or `AssertionError` without context, the test needs better structure or reporting.

## Definition of done for a new test

A new test is acceptable when:

- its level is correct,
- its name describes the scenario,
- its setup is explicit,
- its data is deterministic or marked external,
- it uses POM or SOM instead of raw mechanics,
- its assertions are meaningful,
- it can be run locally,
- it does not break default CI,
- its failure would be diagnosable.
