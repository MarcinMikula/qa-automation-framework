# Architecture decisions

This file records the main design decisions behind the framework.

It is not a complete architecture specification.

---

## Decision 1 — Treat the repository as a skeleton, not a product

**Decision**

The repository is a reusable POM/SOM framework skeleton.

**Reasoning**

A real project needs verified application and domain context that a neutral
public repository cannot supply honestly.

**Consequence**

The repository provides structure, mechanics, examples, and guidance.

The user supplies project truth.

---

## Decision 2 — Start adaptation from a real project need

**Decision**

Framework filling begins with a testing or test-support need, not with an empty
folder.

**Reasoning**

Creating classes without a real need produces speculative architecture and
low-value automation.

**Consequence**

The adaptation sequence is:

```text
need
→ intent
→ scope
→ context
→ artifacts
→ expected result or output
→ evidence
→ acceptance
```

---

## Decision 3 — Keep POM and SOM together but separate

**Decision**

POM and SOM live in one repository as separate adapter layers.

**Consequence**

```text
pages/ and components/
→ UI mechanics

api/
→ API/service mechanics

tests/
→ verification and assertions

optional project workflows
→ repeated test-support orchestration
```

Shared configuration, fixtures, reporting, and test structure may support both
layers.

---

## Decision 4 — Support tests and test-support workflows

**Decision**

POM and SOM may be consumed by executable tests and by non-test workflows.

**Reasoning**

Projects automate both verification and repeated work such as setup, cleanup,
record creation, reproduction, and evidence collection.

**Consequence**

A workflow must not pretend to be a test when it does not verify product
behavior.

Tests own PASS/FAIL assertions.

Support workflows own useful outputs and diagnostic failures.

---

## Decision 5 — Keep examples neutral but readable

**Decision**

Use understandable examples such as `User`, `Product`, and `Order`.

Remove assumptions tied to one industry.

**Reasoning**

Names such as `Entity` and `GenericResource` are formally neutral but difficult
for users with stronger testing or domain skills than programming skills.

**Consequence**

The skeleton teaches the pattern with readable nouns.

Project adaptation owns real domain vocabulary.

---

## Decision 6 — Treat local applications as replaceable targets

**Decision**

`services/` and the demo shop are execution targets, not framework core.

**Consequence**

They may be removed or replaced in a real adaptation.

They should not grow into:

```text
a full shop
a fake CRM
a fake ERP
a domain product
```

Guiding rule:

```text
The demo target exists to exercise the framework.
It must not become the framework.
```

---

## Decision 7 — Separate consistency gates and behavioral tests

**Decision**

Run syntax and collection checks before unit, integration, and E2E tests.

**Reasoning**

A framework repository can contain stale imports, broken optional modules, or
uncollectable tests even when a smaller visible subset is green.

**Consequence**

Current order:

```text
syntax
→ collection
→ unit
→ integration
→ E2E
```

The test pyramid remains a maintenance heuristic, not a mandatory ratio or an
ISTQB requirement.

---

## Decision 8 — Keep default CI deterministic

**Decision**

Default CI runs local, self-contained checks.

**Reasoning**

The public skeleton should not require private credentials, VPN access, or
unstable third-party systems.

**Consequence**

Live and external tests must be explicit and opt-in.

---

## Decision 9 — Use human-led adaptation as the first baseline

**Decision**

Framework acceptance should begin with a human-led adaptation.

**Reasoning**

A human-led path separates:

```text
Is the skeleton useful?
```

from:

```text
Did AI fill it correctly?
```

Human-led does not mean tool-free.

Playwright Codegen, DevTools, Swagger/OpenAPI, IDE tools, generators, and LLM
assistance may still be used.

**Consequence**

A human owns architecture, risk selection, assertions, and acceptance.

---

## Decision 10 — Treat AI assistance as a capability to evaluate

**Decision**

AI output is not correct by default.

**Consequence**

AI may draft artifacts, but project facts, test-level decisions, assertions,
and final acceptance remain human-owned.

The detailed AI-assisted process stays preliminary until the human-led
framework baseline is validated.

---

## Decision 11 — Use one future reference repository

**Decision**

After framework acceptance, create one separate reference repository:

```text
qa-automation-framework-ecommerce-demo
```

**Reasoning**

One repository reduces drift and supports a controlled comparison.

**Consequence**

The repository may compare:

```text
human-led adaptation
vs
AI-assisted adaptation
```

under the same target, scope, acceptance criteria, and quality gates.

This core repository remains neutral.

---

## Decision 12 — Require framework acceptance before stronger claims

**Decision**

Green CI and local examples are not sufficient evidence of framework
usefulness.

**Reasoning**

Internal consistency does not prove that a user can adapt the skeleton to a
concrete project need.

**Consequence**

The next major phase should define:

- framework requirements,
- acceptance risks,
- test conditions and cases,
- evidence,
- entry and exit criteria,
- defects and improvements,
- acceptance conclusions.

The phase should be incremental, risk-based, and transparent about what each
test proves.
