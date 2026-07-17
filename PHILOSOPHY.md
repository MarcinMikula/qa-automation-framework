# Framework philosophy

This document explains the project-specific rationale behind the repository.

General, evergreen testing principles live in
[`AUTOMATION_PRINCIPLES.md`](AUTOMATION_PRINCIPLES.md).

---

## 1. The repository is a skeleton, not a product

The framework provides reusable structure.

A real project supplies:

- application behavior,
- risks,
- locators,
- endpoints,
- authentication,
- test data,
- environment rules,
- expected results,
- domain language.

The framework provides the shape.

The project provides the truth.

---

## 2. Adaptation starts from a real need

Do not fill framework folders because they exist.

Start with:

```text
What real testing or test-support problem are we solving?
```

The need may be:

- regression protection,
- a smoke check,
- an API contract check,
- repeated data setup,
- environment preparation,
- defect reproduction,
- diagnostic evidence collection.

The need should determine the automation scope and architecture.

---

## 3. Not every automation is a test

Verification automation should produce a meaningful verdict against an
expected result.

Test-support automation may instead:

- create a record,
- prepare state,
- clean data,
- return identifiers,
- collect evidence.

POM and SOM are reusable adapters.

Tests and support workflows can both consume them.

A workflow must not pretend to be a product-behavior test when its main purpose
is only to perform repeatable work.

---

## 4. POM and SOM are separate adapter layers

```text
pages/ and components/
→ UI adapter layer

api/
→ API/service adapter layer
```

POM translates browser mechanics into readable application actions.

SOM translates HTTP mechanics into readable service operations.

Tests should remain focused on intent and expected results.

Workflows should remain focused on orchestration and useful output.

---

## 5. Neutral does not mean abstract

The skeleton uses readable examples such as:

```text
User
Product
Order
```

It avoids both:

```text
hidden assumptions from one industry
and
unhelpful names such as Entity or GenericResource
```

Project adaptation owns the real domain vocabulary.

The neutral examples exist to explain the pattern.

They are not universal business models.

---

## 6. Human-led does not mean tool-free

A human-led adaptation may use:

- Playwright Codegen,
- DevTools,
- OpenAPI/Swagger,
- IDE refactoring,
- deterministic generators,
- LLM assistance.

A human still owns:

- purpose,
- architecture,
- risk selection,
- test-level selection,
- assertions,
- final acceptance.

Tools accelerate work.

They do not own quality.

---

## 7. Test levels answer different questions

The repository separates:

- syntax and collection checks,
- unit tests,
- integration tests,
- E2E tests.

The test pyramid is a useful maintenance heuristic.

It is not a mandatory ratio and it is not a substitute for risk analysis.

The preferred level is the fastest level that can provide trustworthy evidence
for the risk being checked.

---

## 8. State and configuration are part of test design

Tests and workflows should make clear:

- what data they need,
- who creates it,
- whether it is isolated,
- whether cleanup is required,
- whether execution is repeatable,
- which environment is targeted.

URLs, credentials, tokens, and environment-specific values should not be hidden
inside generic base classes.

---

## 9. Local targets are replaceable

The local services and demo shop make the repository executable.

They demonstrate:

- structure,
- POM usage,
- SOM usage,
- fixtures,
- test levels,
- CI-safe execution.

They are not framework features and should not grow into a rich application.

```text
The demo target exists to exercise the framework.
It must not become the framework.
```

---

## 10. AI assistance is a capability to evaluate

AI may draft framework content, but it cannot safely invent project truth.

The human-led path should establish whether the skeleton itself is useful.

Only then should the AI-assisted path be compared against the same target,
scope, acceptance criteria, and quality gates.

The comparison belongs in one future reference repository:

```text
qa-automation-framework-ecommerce-demo
```

---

## 11. Green CI is necessary but insufficient

Green CI can prove that committed checks passed.

It cannot prove that:

- the correct project need was selected,
- important risks are covered,
- assertions are meaningful,
- adaptation instructions are usable,
- the framework helps a real user.

Framework acceptance must provide that evidence.

---

## 12. Larger ideas should be challengeable

For larger decisions, ask:

```text
1. What problem are we really solving?
2. What is the simplest useful solution?
3. What could make this idea a bad solution?
4. What result or evidence would make us abandon it?
```

The goal is not to reject ideas automatically.

The goal is to keep the repository evidence-driven.

---

## Summary

```text
Core repository
→ teaches the pattern

Framework acceptance
→ proves whether the pattern helps

Reference implementation
→ shows one complete adaptation

AI comparison
→ evaluates how well AI can help fill the same skeleton
```

The framework should make useful automation easier to structure, understand,
run, and maintain.

It should not automate everything or hide uncertainty.
