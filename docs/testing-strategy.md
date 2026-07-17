# Testing strategy

This document describes the current repository checks and test levels.

The formal framework-acceptance strategy will be defined in the next project
phase.

---

## Evidence layers

The current pipeline uses five layers:

```text
0. Python syntax check
1. Pytest collection check
2. Unit tests
3. Integration tests
4. E2E tests
```

The first two are framework consistency gates.

The remaining layers verify executable behavior at different boundaries.

---

## Gate 0 — Python syntax

```bash
python -m compileall -q api pages components services testdata tests
```

Question:

```text
Can Python compile the active project files?
```

This can expose broken files that normal test imports do not reach.

It does not prove behavior.

---

## Gate 1 — Pytest collection

```bash
python -m pytest --collect-only -q
```

Question:

```text
Can pytest discover and import the test suite?
```

This can expose:

- stale imports,
- missing fixtures,
- broken parametrization,
- invalid markers,
- references left after file renames.

It does not prove behavior.

---

## Unit tests

```bash
python -m pytest tests/unit/ -v
```

Question:

```text
Do small deterministic elements satisfy their local contracts?
```

Typical scope:

- base-class mechanics,
- Pydantic validation,
- response parsing,
- stores and router factories,
- payload builders,
- transformations,
- configuration rules,
- non-trivial reusable helpers.

A filled project should add unit tests for meaningful logic.

It does not need a separate unit test for every trivial locator wrapper.

---

## Integration tests

```bash
python -m pytest tests/integration/ -v -m "not external"
```

Question:

```text
Do Service Objects and service boundaries work together as intended?
```

Typical scope:

- API behavior,
- request and response contracts,
- status and error handling,
- Service Object mapping,
- local multi-service workflows,
- setup through APIs.

Business-facing tests should normally use Service Objects rather than repeat
raw HTTP mechanics.

---

## E2E tests

```bash
python -m pytest tests/e2e/ -v -m "not external"
```

Question:

```text
Does a selected user-visible flow work through the browser?
```

Typical scope:

- critical UI flows,
- browser-specific risks,
- visible outcomes,
- cross-layer scenarios that cannot be trusted at a lower level.

Tests should use Page Objects rather than raw selectors in the test body.

E2E tests should be selected for value, not added to satisfy a fixed pyramid
shape.

---

## Test pyramid boundary

The test pyramid is a useful maintenance heuristic:

```text
more fast and focused checks
fewer slow and broad checks
```

It is not:

- a fixed percentage,
- an ISTQB requirement,
- a substitute for risk analysis,
- proof that every system needs the same test distribution.

Choose the fastest level that can provide trustworthy evidence for the risk.

---

## Verification tests vs support workflows

A verification test has:

- an expected behavior,
- meaningful assertions,
- a PASS/FAIL verdict linked to a risk.

A support workflow primarily:

- prepares data,
- changes state,
- returns identifiers,
- cleans records,
- reproduces a condition,
- collects evidence.

Support workflows may check that their task succeeded.

That does not automatically make them product-behavior tests.

They should be evaluated for usefulness, repeatability, safety, and diagnostic
output.

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

Default CI should avoid tests requiring:

- private credentials,
- VPN access,
- unstable third parties,
- NDA-protected systems,
- destructive real-environment operations.

---

## Current local commands

```bash
python -m compileall -q api pages components services testdata tests
python -m pytest --collect-only -q
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v -m "not external"
python -m pytest tests/e2e/ -v -m "not external"
```

Run deliberately marked external tests separately:

```bash
python -m pytest tests/ -v -m external
```

---

## CI order

```text
install dependencies
→ prepare reports
→ syntax check
→ collection check
→ initialize local data
→ start and smoke-check local services
→ unit tests
→ integration tests
→ E2E tests
→ upload reports
```

Default CI should remain:

- deterministic,
- self-contained,
- public-safe,
- independent from private systems.

---

## What green CI proves

Green CI supports claims about:

- active Python syntax,
- test-suite collectability,
- tested reusable mechanics,
- local service integration,
- local POM/SOM examples,
- the configured runner and dependency combination.

It does not prove:

- complete requirements coverage,
- correct risk selection,
- meaningful assertions in an unknown project,
- usability of adaptation guidance,
- reusability across all application types,
- framework acceptance.

---

## Next formal testing phase

Framework acceptance should add an agile, risk-based layer above the current
technical baseline.

Expected work includes:

- define framework stakeholders and users,
- define requirements and quality characteristics,
- identify acceptance risks,
- derive test conditions and cases,
- decide test levels and evidence,
- execute small acceptance increments,
- record defects and framework friction,
- update requirements and tests as learning occurs,
- summarize what is accepted, rejected, or still unproven.

The approach should be ISTQB-informed without turning the work into excessive
ceremony.

Traceability should help decisions.

It should not become paperwork without value.
