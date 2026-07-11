# Testing strategy

The framework follows a practical test pyramid.

Different test levels answer different questions.

```text
        E2E / UI
      Playwright + POM
     critical user flows

    Integration / API
       httpx + SOM
 contracts, APIs, services

       Unit tests
 models, constraints, logic
```

---

## Unit tests

Unit tests verify small pieces of behavior in isolation.

Typical scope:

- model defaults,
- validation rules,
- constraints,
- deterministic data generation,
- helper functions,
- small domain rules.

Unit tests should be fast, deterministic, and independent from browsers or live
services.

---

## Integration tests

Integration tests verify boundaries between components or services.

Typical scope:

- API response structure,
- status codes,
- required fields,
- error handling,
- Service Object behavior,
- contract assumptions.

Integration tests should usually go through Service Objects instead of raw HTTP
calls from the test body.

---

## E2E tests

E2E tests verify critical user-visible flows through the browser.

Typical scope:

- login,
- search,
- create entity,
- submit form,
- verify visible result or status change.

E2E tests should be fewer than lower-level tests.

They are valuable, but more expensive to maintain.

---

## Markers

Recommended marker policy:

```python
@pytest.mark.unit
@pytest.mark.integration
@pytest.mark.e2e
@pytest.mark.external
```

External tests should be opt-in.

Default local and CI runs should avoid tests that require live third-party
systems, private credentials, or unstable environments.

---

## Recommended commands

Run everything deterministic:

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

Run external tests deliberately:

```bash
python -m pytest tests/ -v -m external
```

---

## CI rule

CI should run tests that are:

- deterministic,
- self-contained,
- safe for public execution,
- not dependent on private credentials,
- not dependent on unstable live systems.

Live or external tests may exist, but they should not block the default pipeline
unless explicitly configured for a trusted environment.
