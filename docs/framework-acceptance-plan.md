# Framework acceptance plan

Status: reviewed v0.3 — Iteration 0 baseline

This document defines a lightweight, risk-based acceptance approach for the
`qa-automation-framework` skeleton.

The goal is not to create a large formal test phase before learning anything.
The goal is to test the framework as a product/tool in small increments and
update the plan when evidence changes our understanding.

## 1. Test object

The test object is the framework skeleton itself:

```text
qa-automation-framework
```

This includes:
- POM structure and base abstractions,
- SOM structure and base abstractions,
- configuration and fixture conventions,
- test-data conventions,
- unit/integration/E2E placement guidance,
- human-led adaptation guidance,
- repository structure,
- CI and consistency gates,
- documentation needed to adapt the skeleton.

The local demo services and demo shop are support targets, not the main test object.

## 2. Acceptance objective

Main question:

```text
Does this framework skeleton actually help a user automate a concrete
testing or test-support need without fighting the framework structure?
```

North-star usability question:

```text
Would the target user be better off using this framework than starting
without it?
```

For the lower-programming-confidence persona, this means:

> Does the framework help a person who understands testing, risk, the domain,
> and the target system turn a concrete testing or test-support need into
> working, maintainable automation without requiring them to design the whole
> automation architecture from scratch?

Supporting questions:

```text
Can the user understand where project-specific code belongs?
Can the user adapt POM and SOM without leaking domain assumptions into core?
Can the user add the right tests at the right level?
Can the user run and diagnose the result?
Does the framework reduce unnecessary technical and architectural decisions?
Does it hide complexity the user does not need while keeping testing decisions visible?
Can the user do this with reasonable effort?
Is the benefit greater than the cost of learning and applying the framework?
```

A framework can be technically capable and still fail acceptance if ordinary
use creates more cognitive or technical work than it removes.

Green CI alone is not acceptance.

## 3. Primary users and stakeholders

### U1 — Automation engineer
Needs:
- reusable structure,
- clear extension points,
- low duplication,
- predictable fixtures/configuration,
- freedom to add project-specific logic without rewriting core.

### U2 — Test analyst / test methodologist / domain expert
Typical strengths:
- business and system context,
- test analysis,
- risk identification,
- expected behavior,
- project architecture.

Possible limitation:
- lower programming confidence.

Needs:
- readable naming,
- purpose-first guidance,
- clear mapping from project need to artifact,
- examples that do not require deep framework knowledge,
- guardrails against putting code in the wrong layer,
- fewer architectural decisions that must be invented from scratch,
- a path that turns testing/domain knowledge into maintainable automation
  without requiring framework-author-level programming skills.

### U3 — QA lead / framework maintainer
Needs:
- consistent structure,
- reviewability,
- scalable conventions,
- clear boundaries,
- maintainable CI,
- explicit limitations,
- predictable onboarding path.

### Stakeholder — framework owner
Needs:
- evidence that the framework solves a real problem,
- evidence of what remains unproven,
- feedback that can drive the next framework increment.

AI is not a primary acceptance user in this phase.
AI-assisted adaptation will be evaluated later against the human-led baseline.

### Target-user prerequisites and responsibility boundary

The framework is intended to reduce unnecessary complexity, not eliminate the
need for relevant competence.

A target user is expected to bring enough context to understand the task being
automated. Depending on the task, this may include:

- software-testing knowledge,
- domain and target-system understanding,
- basic automation concepts,
- basic familiarity with Python, Playwright, pytest, HTTP, or equivalent project tooling,
- willingness to inspect, adapt, and review generated or copied code.

The framework is not expected to:

- teach every prerequisite from first principles,
- turn any user into an automation architect,
- guarantee correct architecture when the user ignores the provided structure,
- detect every stale import, dead file, design smell, or hygiene problem,
- diagnose every root cause automatically,
- prevent misuse of the skeleton.

The framework is expected to:

- reduce avoidable architectural and organizational decisions,
- provide a coherent POM/SOM structure,
- make intended extension points visible,
- guide users toward maintainable placement of project-specific code,
- preserve useful failure context where practical,
- provide documentation and examples that lower the adoption barrier.

Repository hygiene, code review, architectural judgement, and validation remain
shared responsibilities of the tester, automation engineer, maintainer, or
supporting tools such as IDE inspections and LLM-assisted reviews.

The acceptance question is therefore not:

```text
Can absolutely anyone use the framework without prerequisite knowledge?
```

It is:

```text
For the intended user, does the framework remove more unnecessary complexity
than it adds?
```

## 4. Test basis

Current test basis:
- root `README.md`,
- `PHILOSOPHY.md`,
- `AUTOMATION_PRINCIPLES.md`,
- `docs/architecture-decisions.md`,
- `docs/testing-strategy.md`,
- `docs/human-led-adaptation.md`,
- POM and SOM guides/checkpoints,
- `docs/known-limitations.md`,
- `docs/gaps.md`,
- current executable framework implementation.

The requirements backlog is maintained in:

```text
docs/framework-requirements.md
```

Requirements may change when acceptance testing exposes missing or incorrect
assumptions.

## 5. Test approach

The acceptance phase is:

```text
incremental
risk-based
evidence-driven
human-led
ISTQB-informed without unnecessary ceremony
```

Working loop:

```text
requirements and risks
→ select a small acceptance slice
→ derive test conditions
→ design only the needed cases
→ execute
→ record evidence and defects
→ update framework or requirements
→ run the next slice
```

## 6. Acceptance risk backlog

### R1 — Framework works only for its own demo
Priority: HIGH

Risk:
The structure may look reusable but require hidden assumptions from the local
demo implementation.

Evidence needed:
Adaptation to a target that was not designed around the framework.

### R2 — Project-specific code leaks into framework core
Priority: HIGH

Risk:
A user may need to modify base classes or generic modules for ordinary project
customization.

Evidence needed:
A real adaptation should add project artifacts without unnecessary core edits.

### R3 — Lower-programming-skills user cannot apply the guidance
Priority: HIGH

Risk:
Documentation may be technically correct but too abstract, long, or
programmer-oriented.

Evidence needed:
A user can start from a project need and identify the correct artifact and test
level with limited assistance.

### R4 — POM/SOM responsibilities are unclear in real work
Priority: HIGH

Evidence needed:
Real UI/API scenarios can be mapped without duplicated responsibilities or raw
mechanics leaking into tests.

### R5 — Framework encourages automation without a real test purpose
Priority: MEDIUM/HIGH

Evidence needed:
Adaptation begins from a written need, expected result, or useful workflow output.

### R6 — Test vs test-support workflow boundary is confusing
Priority: MEDIUM

Evidence needed:
The user can classify the automation intent and choose appropriate output and
assertions.

### R7 — Fixtures, configuration, and test data become coupled or opaque
Priority: HIGH

Evidence needed:
A concrete adaptation has understandable setup, configuration, ownership, and cleanup.

### R8 — Test-level guidance does not work in practice
Priority: HIGH

Evidence needed:
Real project risks are mapped to unit, integration, E2E, or workflow checks for clear reasons.

### R9 — Failures are hard to diagnose
Priority: MEDIUM/HIGH

Evidence needed:
Selected negative/failure scenarios produce actionable evidence.

### R10 — Documentation creates more friction than it removes
Priority: MEDIUM/HIGH

Evidence needed:
The user can follow a short happy path and consult deeper guidance only when needed.

### R11 — Reusability claims become broader than evidence
Priority: MEDIUM

Evidence needed:
Acceptance conclusions distinguish proven, partially proven, and unproven claims.

### R12 — Framework overhead exceeds framework benefit
Priority: HIGH

Risk:
The framework may be capable and internally well designed but still require so
much reading, configuration, architectural knowledge, or ceremony that the
target user would be faster or more confident starting without it.

This is the "powerful but impractical tool" failure mode.

Evidence needed:
For selected acceptance slices, compare the experience with the realistic
without-framework alternative.

Look for:
- time to understand how to start,
- number and difficulty of decisions the framework removes or adds,
- amount of documentation required before useful work begins,
- need to understand or modify core abstractions,
- assistance required,
- recovery from mistakes,
- maintainability/readability of the result,
- user judgement: "Did the framework make this task easier?"

The goal is not a laboratory benchmark.

The goal is credible evidence that framework adoption reduces net effort for
its intended users.

## 7. Acceptance increments

### Iteration 0 — Test basis and risk model
Goal:
Agree what the framework is expected to do before designing acceptance cases.

Outputs:
- user/stakeholder model,
- initial requirements backlog,
- quality risks,
- acceptance boundaries,
- first test slice candidate.

### Iteration 1 — First human-led adaptation slice
Select one small, real or realistic project need.

Possible categories:

```text
UI regression need
API verification need
test-support setup workflow
```

Expected evidence:
- time and friction notes,
- files added/changed,
- core files that had to be modified,
- unclear guidance,
- failed assumptions,
- test results,
- defects found in the framework.

### Iteration 2 — Opposite layer / second need
If Iteration 1 is UI-heavy, select an API/SOM-oriented need.
If Iteration 1 is API-heavy, select a UI/POM-oriented need.

### Iteration 3 — Lower-programming-confidence usability pass

Use the framework from the perspective of a strong tester/domain expert who is
less confident in programming and automation architecture.

Focus:
- terminology,
- knowing where to start,
- artifact selection,
- technical and architectural decisions the framework removes or adds,
- required programming assumptions,
- amount of documentation needed before useful work begins,
- missing examples,
- decision points,
- assistance required,
- recoverability after mistakes,
- whether the final automation is easier to understand and maintain,
- whether the user would realistically choose the framework again for a
  similar task.

The pass should explicitly ask:

```text
Would this task have been easier without the framework?
```

A technically successful task is not enough if the framework created more
friction than value.

### Iteration 4 — Consolidation and acceptance conclusion
Classify each important claim:

```text
ACCEPTED
PARTIALLY ACCEPTED
NOT ACCEPTED
NOT YET TESTED
```

Do not force a binary "framework passed" conclusion when evidence is mixed.

## 8. Entry criteria

Before the first adaptation slice:
- framework-core POM and SOM foundations are stable for the current stage,
- public documentation is internally consistent,
- local unit/integration/E2E baseline is green,
- CI is green,
- requirements backlog exists,
- top acceptance risks are agreed,
- selected target and need are documented,
- expected outcome is defined.

## 9. Exit criteria

The acceptance phase can be closed when:
- all HIGH acceptance risks have meaningful evidence,
- critical framework defects are resolved or explicitly accepted,
- human-led adaptation has covered relevant POM and SOM needs,
- documentation has been updated from observed friction,
- requirements have acceptance status,
- remaining limitations are documented,
- the final acceptance conclusion is evidence-based.

A test count is not an exit criterion.

## 10. Evidence to collect

For each acceptance slice record:

```text
Need
Target system
User/persona perspective
Requirements exercised
Risks exercised
Files added
Core files modified
Time/effort notes
Questions or blockers
Assistance required
Architecture/technical decisions removed by the framework
Architecture/technical decisions added by the framework
Documentation needed before useful work started
Tests/checks executed
Observed failures
Framework defects
Documentation defects
Workarounds
Without-framework alternative
Would this have been easier without the framework? YES / NO / UNCLEAR
Why?
Decision
```

Do not turn these fields into artificial metrics.

They are lightweight evidence for the central usability question: whether the
framework reduces net effort and cognitive load for the intended user.

## 11. Defect classification

Suggested categories:

```text
FRAMEWORK-DESIGN
DOCUMENTATION
USABILITY
TESTABILITY
CONFIGURATION
POM-BOUNDARY
SOM-BOUNDARY
TEST-DATA
CI-TOOLING
LIMITATION / EXPECTED
```

Severity should describe impact on adaptation, not technical novelty.

## 12. Change policy during acceptance

When a problem is found:

```text
1. Record the evidence.
2. Decide whether it is a framework defect, project-specific need, or limitation.
3. Make the smallest justified change.
4. Add or update automated regression coverage when appropriate.
5. Re-run the affected acceptance condition.
6. Update documentation and requirements if needed.
```

Avoid large redesigns based on one isolated inconvenience.

## 13. First decision gate

Before Iteration 1, agree:

```text
A. Which real project need will be the first acceptance slice?
B. Which target system/application will be used?
C. Which persona are we testing first?
D. Which HIGH risks will that slice exercise?
```

The first slice should maximize learning, not test count.
