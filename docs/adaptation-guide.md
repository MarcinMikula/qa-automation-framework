# Adaptation guide

How to adapt this framework skeleton to a real project.

This is the short orientation guide.

For the detailed purpose-first workflow, use:

```text
docs/human-led-adaptation.md
```

---

## Start with the need

Do not begin by creating files only because the skeleton contains folders.

Begin with:

```text
What project problem or testing need are we trying to solve?
```

Typical needs include:

- regression protection,
- smoke verification,
- API contract checking,
- repeated test-data setup,
- environment preparation,
- defect reproduction,
- diagnostic evidence collection,
- cleanup after testing.

Not every useful automation is a test.

POM and SOM can support:

```text
verification tests
and
test-support workflows
```

A workflow should not pretend to be a test when it does not verify product
behavior.

---

## Use the decision sequence

```text
project need
→ automation intent
→ smallest useful scope
→ required context
→ POM / SOM / workflow / fixture
→ expected result or output
→ implementation
→ quality gates
→ human acceptance
```

For larger decisions, ask:

```text
1. What problem are we really solving?
2. What is the simplest useful solution?
3. What could make this idea a bad solution?
4. What result or evidence would make us abandon it?
```

---

## Map project concepts to the framework

| Project concept | Framework location |
|---|---|
| screen or view | `pages/` |
| reusable UI fragment | `components/` |
| API/service operations | `api/` |
| request/response contract | Pydantic model |
| reusable precondition | pytest fixture |
| repeated test-support process | optional project `workflows/` |
| deterministic data | `testdata/` |
| verification | appropriate `tests/` level |
| project configuration | settings/environment variables |

Do not create an empty layer without a real need.

---

## Keep responsibilities explicit

```text
BasePage / BaseComponent
→ reusable browser mechanics

Concrete Page Objects / Components
→ application-facing UI actions and state

BaseClient / MicroserviceClient
→ reusable HTTP mechanics

Concrete Service Objects
→ application-facing API operations

Tests
→ expected behavior and assertions

Workflows
→ repeated orchestration for test support
```

---

## Add project-specific tests intentionally

Add unit tests for non-trivial:

- transformations,
- validation,
- parsing,
- payload building,
- mapping,
- branching,
- retry or polling behavior.

Add integration tests for:

- service contracts,
- Service Object behavior,
- multi-service flows,
- status and error handling.

Add E2E tests for:

- critical user-facing flows,
- browser-specific risks,
- outcomes that cannot be trusted at a lower level.

Do not require a unit test for every trivial wrapper.

Do not use E2E for everything.

---

## Use tools, keep human ownership

Allowed and useful aids include:

- Playwright Codegen,
- DevTools,
- OpenAPI/Swagger,
- IDE refactoring,
- deterministic generators,
- LLM assistance.

These tools may discover or draft.

A human still owns:

- the project need,
- architecture,
- POM/SOM boundaries,
- test level,
- risk selection,
- assertions,
- final acceptance.

---

## Validate the adaptation

Run the relevant checks and review the result against the original need.

The skeleton helps with structure.

The project supplies:

- application truth,
- domain meaning,
- environment rules,
- risks,
- expected results.

See `human-led-adaptation.md` for the full checklist and examples.
