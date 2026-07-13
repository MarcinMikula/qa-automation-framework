# Testing strategy

This project follows a practical test pyramid, but the pipeline does not start
with behavioral tests immediately.

Before the framework checks whether behavior is correct, it first checks whether
the repository is technically consistent.

This is useful for learning and for real framework work: a test framework can
have passing tests and still contain broken files, stale imports, or code that
pytest cannot even collect.

---

## Framework consistency gates

These checks run before the main test suites.

They are not a replacement for the test pyramid. They are a foundation under it.

```text
0. Python syntax check
1. Pytest collection check
2. Unit tests
3. Integration tests
4. E2E tests
```

The first two steps are especially important in framework repositories, because
framework code often contains helpers, generators, examples, adapters, and
future-facing modules that may not be executed by the normal test suite yet.

---

## Gate 0 — Python syntax check

Command:

```bash
python -m compileall -q api pages components services testdata tests
```

Question answered:

```text
Can Python compile all project files?
```

This check catches:

- invalid Python syntax,
- broken files that are not imported by normal tests,
- stale helper modules,
- partially edited files,
- generator/helper code that has no direct test coverage yet.

Example from this project:

`compileall` exposed a syntax error in `api/swagger_generator.py`. The regular
pytest suite had not executed that file, so the issue stayed hidden until the
hygiene check was added.

This is not a unit test. It does not verify behavior. It verifies that the code
can be parsed and compiled.

---

## Gate 1 — Pytest collection check

Command:

```bash
python -m pytest --collect-only -q
```

Question answered:

```text
Can pytest discover and import the test suite?
```

This check catches:

- broken test imports,
- missing modules,
- missing fixtures,
- invalid pytest markers or parametrization,
- tests that exist but cannot be collected,
- stale references after file renames or package changes.

This is also not a behavioral test. It proves that the test suite is
importable, discoverable, and structurally valid.

It is valuable because a repository can have good individual tests, but still
fail before running them if collection is broken.

---

## Gate 2 — Unit tests

Command:

```bash
python -m pytest tests/unit/ -v
```

Question answered:

```text
Do small framework elements behave according to their contracts?
```

Typical scope:

- model defaults,
- validation rules,
- constraints,
- deterministic data generation,
- helper functions,
- small domain rules,
- reusable in-memory stores,
- router factories,
- Service Object helpers,
- request/response parsing.

In this project, unit tests should not only verify `testdata/testdb.py`.

They should also grow around reusable framework pieces such as:

- `InMemoryStore`,
- `create_crud_router`,
- `MicroserviceClient`,
- Pydantic service models,
- `BaseClient`,
- `api/swagger_generator.py`.

Unit tests should be fast, deterministic, and independent from browsers or live
services.

---

## Integration tests

Command:

```bash
python -m pytest tests/integration/ -v -m "not external"
```

Question answered:

```text
Do components or services work together through their intended boundaries?
```

Typical scope:

- API response structure,
- status codes,
- required fields,
- error handling,
- Service Object behavior,
- contract assumptions,
- local service workflows.

Integration tests should usually go through Service Objects instead of raw HTTP
calls from the test body.

This keeps tests aligned with the SOM pattern:

```text
test
→ Service Object
→ service/API boundary
```

---

## E2E tests

Command:

```bash
python -m pytest tests/e2e/ -v -m "not external"
```

Question answered:

```text
Does a critical user-visible flow work through the browser?
```

Typical scope:

- login,
- search,
- create entity,
- submit form,
- verify visible result or status change.

E2E tests should be fewer than lower-level tests. They are valuable, but more
expensive to maintain.

They should go through Page Objects instead of raw Playwright calls directly in
the test body.

This keeps tests aligned with the POM pattern:

```text
test
→ Page Object
→ browser/UI boundary
```

The current E2E layer is still a lightweight smoke example. A stronger
Salesforce-like or CRM-like POM case study is planned separately.

---

## How this extends the test pyramid

The classic test pyramid focuses on behavioral confidence:

```text
        E2E
   Integration
      Unit
```

This project adds consistency checks underneath that pyramid:

```text
        E2E
   Integration
      Unit
 Collection check
 Syntax check
```

The lower gates do not prove that business behavior is correct.

They prove that the project is structurally healthy enough for meaningful tests
to run.

That matters in automation framework work, because framework repositories often
contain:

- reusable helpers,
- adapters,
- generators,
- examples,
- external-test placeholders,
- code intended for future case studies.

Without hygiene checks, these areas can silently rot while the visible test
suite remains green.

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

Default local and CI runs should avoid tests that require:

- live third-party systems,
- private credentials,
- unstable environments,
- private application data,
- NDA-protected systems.

External tests may exist, but they should not block the default pipeline unless
explicitly configured for a trusted environment.

---

## Recommended local commands

Run syntax check:

```bash
python -m compileall -q api pages components services testdata tests
```

Run collection check:

```bash
python -m pytest --collect-only -q
```

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
python -m pytest tests/e2e/ -v -m "not external"
```

Run external tests deliberately:

```bash
python -m pytest tests/ -v -m external
```

---

## CI rule

CI should run checks in this order:

```text
1. install dependencies
2. prepare reports directory
3. compile Python files
4. collect pytest tests
5. initialize local test data
6. start local services
7. smoke-check local services
8. run unit tests
9. run integration tests
10. run E2E tests
11. upload lightweight reports
```

CI should run tests that are:

- deterministic,
- self-contained,
- safe for public execution,
- not dependent on private credentials,
- not dependent on unstable live systems.

The goal is not only to get a green pipeline.

The goal is to know what the green pipeline actually proves.