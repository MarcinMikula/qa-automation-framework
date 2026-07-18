# Framework acceptance evidence

Status: active log — Iteration 0 baseline

This file stores raw framework-acceptance evidence:

- observations,
- execution results,
- friction,
- defects,
- working decisions,
- pivots,
- unresolved questions,
- follow-up actions.

It is intentionally different from `LEARNINGS.md`.

```text
framework-acceptance-evidence.md
→ what happened and what evidence we collected

LEARNINGS.md
→ what we concluded after analysing that evidence
```

Core rule:

> Observation is not automatically a conclusion.
> One failure is not automatically a framework design rule.

---

## Evidence lifecycle

Use this flow:

```text
observation
→ classification
→ analysis
→ decision
→ follow-up or fix
→ re-test
→ distilled learning when justified
```

A single observation may remain unresolved.

A repeated pattern may justify a framework change.

A framework change does not automatically justify a general lesson.

---

## Evidence entry template

Copy this block for each meaningful acceptance observation.

```text
ID:
Iteration:
Date:
Target / context:
Persona perspective:

Related requirement(s):
Related risk(s):

Expectation:
What did we expect the framework, guidance, or workflow to enable?

Observation / actual result:
What actually happened?

Evidence:
Commands, files, screenshots, test output, timings, commits, or other
verifiable references.

Usability comparison:
What decisions did the framework remove?
What decisions or friction did it add?
What assistance was required?
What was the realistic without-framework alternative?
Would this have been easier without the framework? YES / NO / UNCLEAR
Why?

Impact:
LOW / MEDIUM / HIGH / CRITICAL

Classification:
FRAMEWORK-DESIGN / DOCUMENTATION / USABILITY / TESTABILITY /
CONFIGURATION / POM-BOUNDARY / SOM-BOUNDARY / TEST-DATA /
CI-TOOLING / LIMITATION-EXPECTED

Analysis:
Why might this have happened?
What is still uncertain?

Decision:
KEEP / CHANGE / DEFER / INVESTIGATE / ACCEPT-LIMITATION

Follow-up:
What happens next?

Re-test result:
Add only after the follow-up has been verified.

Learning candidate:
YES / NO / NOT YET
```

---

## Iteration 0 — baseline decisions

Iteration 0 creates the test basis before executing a real adaptation slice.

No framework acceptance verdict is issued in this iteration.

### AE-0001 — Separate raw evidence from curated learnings

**Expectation**

The acceptance phase is expected to generate many observations, working
hypotheses, changes of mind, and possible pivots.

The project needs a place to record them without turning every observation into
a permanent architecture principle.

**Observation / actual result**

A dedicated evidence log and the existing `LEARNINGS.md` have different jobs.

```text
Evidence log
→ chronological, specific, traceable

LEARNINGS.md
→ curated, durable conclusions
```

**Impact**

MEDIUM — without this separation, temporary observations could become false
design rules, while useful execution evidence could be lost.

**Classification**

TESTABILITY / DOCUMENTATION

**Related requirements**

```text
QR-07 Evidence honesty
```

**Related risks**

```text
R11 Reusability claims become broader than evidence
```

**Decision**

KEEP — use this file as the primary acceptance evidence log.

Only promote conclusions to `LEARNINGS.md` after analysis.

**Learning candidate**

YES — recorded as a framework-acceptance learning because this is an explicit
working rule for the acceptance process.

---

### AE-0002 — Framework value must be judged against the work it removes

**Type**

Iteration 0 acceptance hypothesis / decision.

This is not yet an execution result.

**Expectation**

A reusable framework should do more than make an automation task technically
possible.

For its intended users, it should make ordinary testing or test-support
automation easier, clearer, safer, or more maintainable than a realistic
without-framework approach.

**Observation / actual result**

Requirements review exposed a missing acceptance dimension.

`Readability` and `Learnability` alone do not answer the stronger question:

```text
Would the user actually be better off using this framework?
```

A highly capable framework can still fail as a practical tool if its adoption
cost exceeds the work it removes.

**Impact**

HIGH — this changes how usability acceptance must be evaluated.

**Classification**

USABILITY / FRAMEWORK-DESIGN

**Related requirements**

```text
QR-01 Readability
QR-05 Learnability
QR-08 Practical usability and adoption efficiency
```

**Related risks**

```text
R3  Lower-programming-skills user cannot apply the guidance
R10 Documentation creates more friction than it removes
R12 Framework overhead exceeds framework benefit
```

**Decision**

KEEP AS ACCEPTANCE HYPOTHESIS.

For representative acceptance slices, collect comparative evidence about:

- cognitive load,
- architectural/technical decisions removed or added,
- documentation needed,
- assistance required,
- recovery from mistakes,
- resulting maintainability,
- whether the user would realistically choose the framework again.

Do not require an artificial time benchmark in Iteration 0.

**Learning candidate**

NOT YET — promote this to `LEARNINGS.md` only after acceptance evidence shows
whether the hypothesis holds, fails, or needs qualification.

---

### AE-0003 — Remove unfulfillable framework consistency promise

**Type**

Iteration 0 requirements review decision.

**Expectation**

Functional requirements should describe capabilities the framework itself can
reasonably provide or enable.

**Observation / actual result**

The original requirement `FR-10 — Framework consistency gates` implied that the
framework could provide executable consistency protection against problems such
as syntax failures and stale imports.

Review showed that this mixed two different responsibilities:

```text
framework capability
vs.
repository-development hygiene
```

Tools such as `compileall`, `pytest --collect-only`, IDE inspections, linters,
manual review, or LLM-assisted hygiene checks can detect some classes of
problem.

They do not make the framework itself responsible for finding every stale
import, dead file, architecture inconsistency, or maintenance defect.

**Impact**

MEDIUM — keeping the requirement would overstate what the framework can honestly
promise.

**Classification**

FRAMEWORK-DESIGN / TESTABILITY

**Decision**

REMOVE the original `FR-10 — Framework consistency gates`.

Keep hygiene checks as development and CI practices where useful.

Renumber the original `FR-11 — CI execution` to `FR-10`.

**Learning candidate**

YES — candidate for later promotion after the acceptance baseline is committed
and the distinction remains useful in practice.

---

### AE-0004 — Define target-user prerequisites and tool responsibility boundary

**Type**

Iteration 0 requirements review decision.

**Expectation**

Usability requirements should be ambitious without promising that the framework
can remove every prerequisite skill.

**Observation / actual result**

Review of `FR-02`, `QR-01`, `QR-03`, `QR-04`, and `QR-05` exposed an important
boundary:

```text
reduce unnecessary complexity
!=
eliminate necessary competence
```

The framework should help a tester or automation practitioner avoid reinventing
architecture and structure.

It cannot guarantee correct use by a person with no relevant testing, domain,
automation, or technical foundation.

Likewise, maintainability and diagnosability are supported qualities, not
absolute guarantees. A user can still misuse the structure or create code that
is difficult to maintain.

**Impact**

HIGH — this boundary prevents unrealistic acceptance expectations and prevents
the framework from being judged against an impossible universal-user promise.

**Classification**

USABILITY / FRAMEWORK-DESIGN

**Related requirements**

```text
FR-02 Clear artifact mapping
QR-01 Readability
QR-03 Maintainability
QR-04 Diagnosability
QR-05 Learnability
QR-08 Practical usability and adoption efficiency
```

**Decision**

KEEP the requirements at their current level of abstraction.

Add a separate `Target-user prerequisites and responsibility boundary` section
to the acceptance plan.

Do not inflate individual requirements with prerequisite clauses or detailed
process instructions.

**Learning candidate**

YES — candidate for later promotion if acceptance evidence confirms that this
boundary is useful and sufficient.

---

## Iteration 1

Not started.

The first entry should be created only after the first real or realistic
human-led adaptation slice is selected and executed.

Do not pre-fill observations before evidence exists.
