# Human-led adaptation guide

This guide explains how to fill the framework skeleton with project-specific
content while keeping the important testing and architecture decisions under
human control.

"Human-led" does not mean that every selector, payload, or class must be typed
manually.

Useful tools may include:

- Playwright Codegen,
- browser developer tools,
- OpenAPI/Swagger,
- IDE refactoring,
- deterministic generators,
- LLM assistance.

The distinction is ownership:

```text
Tools accelerate discovery and drafting.
A human owns purpose, architecture, risk, assertions, and acceptance.
```

---

## Quick path

For a first adaptation, follow this shorter sequence:

```text
1. Write the real project need.
2. Decide whether the result is a test or a support workflow.
3. Select one small valuable scope.
4. Collect only the UI/API/data context needed for that scope.
5. Map the need to POM, SOM, fixtures, workflow, and test level.
6. Define expected results or useful workflow output.
7. Implement with Codegen, DevTools, Swagger, IDE, or AI assistance.
8. Add tests for meaningful logic and risks.
9. Run quality gates.
10. Perform human acceptance against the original need.
```

The remaining sections explain these decisions in more detail.

A first-time user does not need to apply every optional pattern.

---

## Who this guide is for

This guide is written for people who may understand:

- the tested application,
- business processes,
- system architecture,
- project risks,
- test analysis,
- expected behavior,

but may have less confidence in automation architecture or programming.

Possible users include:

- automation engineers,
- test analysts,
- test methodologists,
- domain specialists,
- QA leads,
- manual testers moving toward automation.

The framework should help these users translate project knowledge into
maintainable automation artifacts.

---

## Start with a project need, not a framework folder

Do not begin with:

```text
What can I put into pages/?
What can I put into api/?
What test can I add because the skeleton exists?
```

Begin with:

```text
What real project problem are we trying to solve?
```

The skeleton is not filled because its directories are empty.

It is filled because a project has a repeated need, a risk, or a costly manual
activity.

Core rule:

> The project need selects the automation.
> The framework only gives that automation a clear structure.

---

## Challenge larger decisions

Before committing to a larger automation idea, ask four questions:

```text
1. What problem are we really solving?
2. What is the simplest useful solution?
3. What could make this idea a bad solution?
4. What result or evidence would make us abandon it?
```

These questions are not meant to block progress.

They help avoid:

- automating work that has little value,
- selecting E2E when API would be enough,
- creating abstractions before a real need exists,
- building a tool because the architecture is interesting,
- continuing an approach after evidence shows that it is not useful.

Example:

```text
Idea:
Build a dedicated AI frontend exploration agent.

Problem:
General LLM-assisted adaptation may explore UI poorly or map observations
incorrectly into Page Objects.

Simplest useful solution:
First test normal LLM assistance together with Playwright tools and repository
context.

Risk:
A dedicated agent may duplicate existing tooling without a real advantage.

Abandon or defer condition:
The AI-assisted adaptation already produces acceptable results with ordinary
tools and human review.
```

---

## Step 1 — Write a project-need statement

Before writing code, capture the need in plain language.

Use this template:

```text
Need:
Who needs this automation?
What repeated problem or risk exists?
How often does it occur?
What is the current manual cost?
What outcome would make the automation useful?

Scope:
What is included?
What is intentionally excluded?

Acceptance:
How will we know that the solution works?
```

Example — regression protection:

```text
Need:
Protect the critical checkout flow before a release.

Current problem:
The flow is checked manually in every regression cycle.

Scope:
Product search, product details, add to cart, checkout, confirmation.

Acceptance:
The automation verifies the expected business outcome and reports a clear
PASS/FAIL result.
```

Example — test-support workflow:

```text
Need:
Create a Salesforce Account with required project data for manual testing.

Current problem:
A tester repeats the same UI or API setup before many scenarios.

Scope:
Create one valid Account and return its identifier.

Acceptance:
The workflow creates the record in the selected environment, returns the record
ID, and reports actionable failure information.
```

The second example is useful automation, but it is not automatically a
regression test.

---

## Step 2 — Classify the automation intent

The classification helps select the right artifacts and expected output.

### Verification automation

Purpose:

```text
Check system behavior against an expected result.
```

Typical examples:

- regression tests,
- smoke tests,
- API contract checks,
- integration checks,
- release gates,
- critical E2E flows.

Expected result:

```text
PASS / FAIL with meaningful evidence
```

### Test-support automation

Purpose:

```text
Prepare, execute, or clean up repeatable work needed by testers.
```

Typical examples:

- create a customer or Account,
- prepare an order in a required status,
- assign roles or permissions,
- clean up test records,
- reset a reusable test user,
- prepare a precondition for exploratory testing.

Expected result:

```text
Task result, created identifiers, and actionable error information
```

A test-support workflow may verify that its operation technically succeeded.

That does not automatically make it a product-behavior test.

### Data and environment automation

Purpose:

```text
Create, transform, reset, or validate project state.
```

Typical examples:

- seed test data,
- generate many records,
- compare data between systems,
- reconcile migration results,
- verify environment configuration,
- reset state before a test run.

### Diagnostic and reproduction automation

Purpose:

```text
Reproduce a problem or collect evidence.
```

Typical examples:

- reproduce a reported defect,
- capture screenshots and traces,
- collect API responses,
- compare expected and actual state,
- prepare diagnostic records,
- gather evidence for investigation.

These categories may overlap.

The important question is what the automation is expected to prove or produce.

---

## Test or workflow?

Use a test when:

- there is a defined expected behavior,
- a PASS/FAIL verdict is meaningful,
- a failure represents a tested risk,
- assertions protect an agreed contract or outcome.

Use a workflow or task when:

- the main goal is to perform repeatable work,
- the result is an identifier, prepared state, or evidence,
- the automation supports another test activity,
- product correctness is not the primary verdict.

Useful mental model:

```text
POM and SOM are reusable automation adapters.

Tests are one consumer.
Test-support workflows are another.
```

A workflow must not pretend to be a test when it does not verify behavior.

---

## Step 3 — Select the smallest useful scope

Do not adapt the whole application at once.

Choose one need that is:

- valuable,
- understandable,
- possible to observe,
- small enough to finish,
- representative enough to expose framework friction.

Good first scopes:

```text
one critical UI flow
one useful API workflow
one repeated data-setup task
one defect-reproduction path
```

Avoid beginning with:

```text
automate the entire regression suite
model the entire CRM
create every possible Page Object
generate Service Objects for every endpoint
```

A small completed adaptation teaches more than a large unfinished structure.

---

## Step 4 — Collect project context before coding

The framework cannot infer project truth.

Collect the minimum context needed for the selected scope.

### Business and testing context

Capture:

- user goal,
- business flow,
- expected outcome,
- important negative paths,
- known risks,
- acceptance criteria,
- required roles and permissions.

### UI context

Capture:

- relevant screens,
- reusable components,
- stable locator candidates,
- navigation rules,
- loading behavior,
- frames, dialogs, tabs, or Shadow DOM,
- screenshots or traces when useful.

### API context

Capture:

- base URLs,
- endpoints,
- HTTP methods,
- authentication,
- request and response examples,
- meaningful status codes,
- asynchronous or polling behavior,
- rate limits or provider-specific rules.

### Data and environment context

Capture:

- required records,
- reusable and generated data,
- cleanup rules,
- environment differences,
- secrets and credentials,
- restrictions on destructive operations,
- whether the workflow can be repeated safely.

Missing context should be recorded, not guessed.

---

## Step 5 — Map project concepts to framework artifacts

Use the simplest artifact that matches the need.

| Project concept | Framework artifact |
|---|---|
| application screen or view | Page Object in `pages/` |
| reusable UI fragment | Component Object in `components/` |
| operations of one API or service | Service Object in `api/` |
| request or response contract | Pydantic model |
| reusable test precondition | pytest fixture |
| repeated multi-step test-support process | project-specific workflow |
| environment URL or timeout | settings/environment configuration |
| deterministic reusable test data | `testdata/` |
| behavior that needs PASS/FAIL | test in the appropriate test level |
| non-trivial local transformation | unit-tested helper or model logic |
| known unresolved project constraint | project gap or limitation |

Do not create empty layers only because the skeleton contains them.

Examples:

```text
UI-only regression flow
→ Page Objects + E2E test

API-only contract or workflow
→ Service Objects + integration tests

API setup followed by UI verification
→ Service Objects + fixture/workflow + Page Objects + E2E test

Repeated record creation for manual testers
→ Service Objects or Page Objects + project workflow
```

---

## Step 6 — Choose POM, SOM, or both

### Choose POM when the need is about observable UI behavior

Examples:

- a user completes a business flow,
- validation messages are displayed,
- navigation or UI state matters,
- the browser itself is part of the risk.

Structure:

```text
tests/e2e/
→ concrete Page Objects
→ BasePage / BaseComponent
→ browser
```

### Choose SOM when the need is about service behavior or efficient setup

Examples:

- API contracts,
- service workflows,
- fast data creation,
- setup and cleanup,
- response mapping,
- status and error handling.

Structure:

```text
tests/integration/ or project workflow
→ concrete Service Objects
→ BaseClient or MicroserviceClient
→ API
```

### Choose both when each layer has a clear job

Example:

```text
Service Object creates test data
→ Page Object performs the user-facing action
→ E2E test verifies the business outcome
```

Do not use UI only because it is visible.

Do not use API only when the user-facing UI behavior is the actual risk.

---

## Step 7 — Define expected results before implementation

For verification automation, write assertions before or together with the
implementation plan.

Ask:

- What exact outcome proves success?
- What would be a false positive?
- Which value must be checked?
- Which negative outcome matters?
- What evidence is needed when the check fails?

Weak:

```python
assert response is not None
```

Stronger:

```python
assert order.status == "CONFIRMED"
assert order.user_id == expected_user_id
```

For a UI flow, do not stop at:

```text
button was clicked
```

Verify the business-visible outcome:

```text
order confirmation is shown
record status changed
expected validation message is visible
```

For test-support workflows, define output instead of fake assertions:

```text
created record ID
environment
input summary
result status
cleanup information
diagnostic error
```

---

## Step 8 — Add configuration safely

Project-specific values belong in configuration or environment variables.

Typical values:

- application URL,
- API URL,
- timeout,
- environment name,
- usernames,
- tokens,
- feature flags.

Rules:

- do not commit real credentials,
- do not hide unrelated application defaults in generic base classes,
- make destructive environments explicit,
- fail clearly when required configuration is missing,
- keep local deterministic defaults only where they are genuinely safe.

Example:

```python
salesforce_base_url = os.environ["SALESFORCE_BASE_URL"]
```

A generic `BaseClient` should receive its target URL explicitly.

The project configuration decides which real API it uses.

---

## Step 9 — Create Page Objects from user responsibilities

A Page Object should describe what a user can do or observe on a screen.

Good:

```python
search_page.search_for("laptop")
product_page.add_to_cart()
confirmation_page.order_number()
```

Avoid exposing tests to raw locator details:

```python
page.locator("#submit").click()
```

Keep this boundary:

```text
BasePage
→ reusable browser mechanics

Concrete Page Object
→ screen actions and state

Test
→ business assertions
```

Use Playwright Codegen to discover interaction candidates.

Do not treat generated code as the final Page Object design.

Human review must decide:

- stable locator strategy,
- page and component boundaries,
- useful method names,
- synchronization,
- which observations belong in assertions.

---

## Step 10 — Create Service Objects from service responsibilities

A Service Object should describe useful operations of one API or service.

Good:

```python
user_service.create(user_payload)
order_service.update(order_id, status_update)
```

Avoid repeating raw HTTP details in business-facing tests:

```python
client.post("/orders", json=payload)
```

Keep this boundary:

```text
BaseClient / MicroserviceClient
→ reusable HTTP mechanics

Concrete Service Object
→ service operations and response mapping

Test or workflow
→ intent, expected result, and orchestration
```

Use OpenAPI/Swagger to discover:

- endpoints,
- methods,
- schemas,
- status codes.

Do not treat generated methods as validated business operations.

Human review must confirm:

- correct authentication,
- meaningful operation names,
- request and response models,
- error behavior,
- expected status handling,
- whether the operation belongs in a test or support workflow.

---

## Step 11 — Add workflows only when the project needs them

The neutral skeleton does not need an empty workflow layer.

A project may add one when it has repeated multi-step test-support operations.

Possible project structure:

```text
workflows/
├── create_test_user.py
├── prepare_order.py
└── reproduce_reported_defect.py
```

A workflow may orchestrate:

- several Service Objects,
- several Page Objects,
- configuration,
- test data,
- cleanup.

It should return a useful result and fail diagnostically.

Example result:

```text
Task: create Salesforce Account
Environment: UAT
Status: SUCCESS
Account ID: 001XXXXXXXXXXXX
```

Do not place reusable browser or HTTP mechanics in workflows.

Those still belong in POM or SOM.

---

## Step 12 — Add fixtures and test data intentionally

Use fixtures for reusable test preconditions, not to hide the scenario.

A fixture may:

- start a local service,
- create a user,
- prepare an authenticated page,
- clean records,
- provide configuration,
- return created identifiers.

A fixture should not make the test impossible to understand.

Weak:

```python
def test_checkout(prepared_everything):
    ...
```

Stronger:

```python
def test_checkout(active_user, available_product):
    ...
```

Test data rules:

- make ownership clear,
- control cleanup,
- avoid fragile fixed identifiers,
- use unique values where required,
- document records that must be shared,
- distinguish generated data from reference data.

---

## Step 13 — Add project-specific tests where they add confidence

A filled project will normally add more tests than the neutral skeleton.

That does not mean every wrapper method needs its own unit test.

### Add unit tests for

- payload builders,
- response mapping,
- parsers,
- data transformations,
- validation rules,
- reusable helpers,
- branching logic,
- retry or polling decisions,
- configuration rules.

### Add integration tests for

- API contracts,
- Service Object behavior,
- multi-service workflows,
- status and error handling,
- authentication boundaries,
- project data setup through APIs.

### Add E2E tests for

- critical user-facing flows,
- browser-specific risks,
- cross-layer outcomes that cannot be trusted at a lower level,
- a small number of high-value regression scenarios.

Avoid:

```text
unit-testing every trivial click wrapper
and
using E2E for every requirement
```

Test the contract, risk, and non-trivial behavior.

---

## Step 14 — Use tools without surrendering decisions

### Playwright Codegen

Useful for:

- discovering locator candidates,
- recording a first interaction path,
- learning how the page behaves.

Does not decide:

- Page Object boundaries,
- scenario value,
- locator stability,
- assertions,
- correct test level.

### DevTools

Useful for:

- DOM inspection,
- network calls,
- storage and cookies,
- timing,
- frames and Shadow DOM,
- request and response evidence.

### OpenAPI/Swagger

Useful for:

- endpoint discovery,
- schemas,
- methods,
- sample payloads,
- documented response codes.

Does not prove:

- actual business behavior,
- production compatibility,
- meaningful test scenarios,
- complete error behavior.

### IDE and deterministic generators

Useful for:

- refactoring,
- rename safety,
- scaffolding,
- repetitive structural work.

### LLM assistance

Useful for:

- drafts,
- file-placement suggestions,
- code review,
- missing-context questions,
- test-case proposals,
- documentation updates.

Human review remains required.

```text
AI proposes.
Tests provide evidence.
A human accepts or rejects.
```

---

## Step 15 — Run framework quality gates

Before accepting the adaptation, run the checks relevant to the project.

Core repository checks:

```powershell
python -m compileall -q api pages components services testdata tests
python -m pytest --collect-only -q
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/e2e/ -v
```

A real project may separate:

- local deterministic tests,
- external tests,
- destructive tests,
- smoke tests,
- long-running regression tests.

Green checks prove only what they actually execute.

They do not prove that:

- the correct risks were selected,
- assertions are meaningful,
- external contracts are current,
- the workflow is useful to testers,
- the framework is easy to adapt.

---

## Step 16 — Perform human acceptance review

Before calling the adaptation ready, review it from four perspectives.

### Project value

- Does it solve the original need?
- Is the result useful to its intended user?
- Is the manual cost or risk actually reduced?
- Is the scope still appropriate?

### Test design

- Is this automation a test, support workflow, data task, or diagnostic tool?
- Is the selected test level appropriate?
- Are assertions meaningful?
- Could the solution pass while the real behavior is wrong?

### Architecture

- Are selectors kept in Page Objects?
- Are HTTP details kept in Service Objects?
- Are base classes still domain-neutral?
- Are workflows orchestrating rather than duplicating adapters?
- Are fixtures understandable?

### Maintainability and safety

- Is configuration explicit?
- Are credentials protected?
- Is test data controlled?
- Is cleanup safe?
- Are failures diagnostic?
- Is the code small enough to change?

---

## Step 17 — Record friction, gaps, and decisions

Adaptation is also a test of the framework.

Record:

- where file placement was unclear,
- which helper was missing,
- where a base class was too weak or too broad,
- which instruction was confusing,
- what required a workaround,
- which proposed abstraction was unnecessary.

Do not automatically add every project workaround to framework core.

Ask:

```text
Is this a reusable framework need?
Or is this project-specific behavior?
```

Use the four decision questions before expanding the skeleton.

---

## Minimal human-led adaptation checklist

```text
[ ] A real project need is written down.
[ ] The automation intent is classified.
[ ] The smallest useful scope is selected.
[ ] Expected results or workflow outputs are defined.
[ ] Required UI/API/data/environment context is collected.
[ ] POM, SOM, workflow, fixtures, and tests have clear responsibilities.
[ ] Project-specific configuration is explicit and safe.
[ ] Assertions protect the intended risk.
[ ] Non-trivial project logic has appropriate unit coverage.
[ ] Integration and E2E coverage are used at the right level.
[ ] Codegen, Swagger, and AI output have been reviewed.
[ ] Quality gates are green.
[ ] A human has accepted the result against the original need.
[ ] Friction and remaining gaps are documented.
```

---

## Connection to framework acceptance

This guide itself must be validated.

Framework acceptance should check:

```text
Can a user start from a real project need?
Can they identify the correct framework artifacts?
Can they fill the skeleton without fighting its structure?
Does the result help them test or support testing?
```

The first acceptance adaptation should be human-led.

Reason:

```text
First question:
Is the skeleton useful?

Later question:
How well can AI help fill it?
```

After the skeleton passes acceptance, one separate reference repository is
planned:

```text
qa-automation-framework-ecommerce-demo
```

That repository may contain a controlled comparison of:

```text
human-led adaptation
vs
AI-assisted adaptation
```

Both approaches should use:

- the same target application,
- the same starting skeleton,
- the same scope,
- the same acceptance criteria,
- the same quality gates.

This core repository remains the neutral skeleton.
