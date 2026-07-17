# AI-assisted adaptation

Status:

```text
Preliminary guardrails.
Not yet a validated adaptation process.
```

The human-led path should be validated first.

Reason:

```text
Question 1:
Is the framework skeleton useful?

Question 2:
How well can AI help fill it?
```

Testing AI first would mix those two questions.

---

## Purpose-first input

Do not ask AI to fill empty folders without a real need.

Provide:

- the project need,
- intended user,
- automation intent,
- smallest useful scope,
- expected result or useful workflow output,
- application architecture,
- UI and API context,
- environment rules,
- test-data constraints,
- known risks,
- non-goals.

Missing project truth should be reported as missing.

It should not be invented.

---

## Useful AI tasks

AI may help draft:

- Page Objects,
- Component Objects,
- Service Objects,
- Pydantic models,
- fixtures,
- project workflows,
- data builders,
- test skeletons,
- documentation,
- refactoring proposals,
- questions about missing context.

It may also review:

- file placement,
- naming,
- duplicated mechanics,
- likely architecture boundary violations,
- untested non-trivial logic.

---

## Decisions AI does not own

AI should not decide alone:

- whether the project need is worth automating,
- which business risk matters,
- whether the result should be a test or support workflow,
- which test level is appropriate,
- whether a locator is stable,
- whether an API contract is correct,
- whether data is valid,
- whether an assertion protects the intended outcome,
- whether generated code is maintainable,
- whether the adaptation is accepted.

Those decisions remain human-owned.

---

## Safe working loop

```text
1. Define the project need and acceptance criteria.
2. Provide verified context.
3. Ask AI for a small draft.
4. Inspect assumptions and missing information.
5. Correct invented or unverified details.
6. Run syntax, collection, and relevant tests.
7. Review architecture, risk, and assertions.
8. Accept, revise, or reject the change.
9. Record friction and lessons.
```

AI output should remain small enough to review.

Large repository-wide generations make assumptions harder to detect.

---

## Human acceptance gate

Before accepting AI-assisted automation, answer:

- What problem does it solve?
- Is the result a verification test or support workflow?
- Why is this the right layer?
- Which facts were verified?
- Which assumptions remain?
- What exact outcome is asserted or returned?
- Could the automation pass while the real behavior is wrong?
- Can it run repeatedly?
- Is failure information actionable?
- Does the result fit the framework without expanding core unnecessarily?

```text
AI proposes.
Tests provide evidence.
A human accepts or rejects.
```

---

## Future controlled comparison

After framework acceptance, one separate repository is planned:

```text
qa-automation-framework-ecommerce-demo
```

It should compare:

```text
human-led adaptation
vs
AI-assisted adaptation
```

Both paths should use:

- the same target,
- the same starting skeleton,
- the same scope,
- the same flows,
- the same acceptance criteria,
- the same quality gates.

Useful comparison evidence may include:

- time spent,
- amount of rework,
- incorrect assumptions,
- locator quality,
- architecture violations,
- assertion quality,
- missing risk coverage,
- maintainability,
- human review effort.

The goal is not to prove that AI is good or bad in advance.

The goal is to collect evidence.

---

## Exploratory-agent boundary

A dedicated frontend exploratory-testing agent is not part of the current
roadmap.

It remains a conditional future repository.

Build it only if the controlled comparison reveals a repeatable gap that normal
LLM assistance, Playwright tooling, and human review do not solve well enough.

---

## Related guidance

Start with:

- [Adaptation guide](adaptation-guide.md)
- [Human-led adaptation guide](human-led-adaptation.md)
- [Framework filling instructions plan](framework-filling-instructions-plan.md)
