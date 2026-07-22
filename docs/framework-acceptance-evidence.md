# Framework acceptance evidence

Status: active log — Iteration 1 in progress

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

## Iteration 1 — Human-led POM adaptation

Iteration 1 tests the framework through a real, human-led adaptation rather
than through additional framework-core development.

The working branch is:

```text
acceptance/iteration-1-salesforce-account
```

The acceptance code is intentionally isolated from `main` while the experiment
is in progress.

Project-specific Salesforce code is not assumed to belong in the neutral
framework core.

---

### Acceptance Slice I1-S1 — Salesforce Create Account regression verification

**Project need**

As a tester, I want to automate Salesforce Account creation and verify that the
record was created successfully so that the basic Account creation flow can be
checked repeatedly as part of regression testing.

**Automation intent**

```text
VERIFICATION AUTOMATION
→ regression test
```

This slice deliberately tests verification automation first.

A later slice may reuse the same business operation — creating an Account —
as test-support automation in order to exercise `FR-06` without pretending
that data setup is itself a product-behavior test.

**Target**

Salesforce Lightning development/test org.

**Persona perspective**

Tester / test analyst who:

- understands software testing and the target business process,
- has basic Python and Playwright knowledge,
- understands basic POM concepts,
- is not assumed to be an automation-framework architect.

This persona is intentionally capable enough to automate, but should not need
to design the whole framework architecture from scratch.

**Precondition**

An authenticated Salesforce session is available.

Authentication and MFA automation are outside this slice.

A manual authentication bootstrap plus reusable Playwright authenticated state
may be used if needed.

**Minimal scope**

```text
GIVEN
an authenticated Salesforce user with permission to create Accounts

WHEN
the user navigates to Accounts
and creates a new Account with required test data

THEN
Salesforce confirms successful creation

AND
the created Account can be identified using the expected test data
```

**Out of scope**

- automated login and MFA,
- full Account CRUD,
- complete Salesforce regression,
- test-support Account creation,
- SOM/API adaptation,
- combined POM/SOM flow,
- Salesforce-wide component inventory,
- Salesforce-wide navigation mapping.

**Broader business context captured during adaptation**

Account creation may support a larger Salesforce business process such as
order creation, where an Account is a prerequisite.

This broader context is useful for understanding the need, but it does not
automatically expand the first acceptance slice.

**Primary requirements exercised**

```text
FR-01 Purpose-first adaptation
FR-02 Clear artifact mapping
FR-03 POM project adaptation
FR-07 Project-specific configuration
FR-08 Project-specific test data and state

QR-01 Readability
QR-02 Reusability
QR-03 Maintainability
QR-04 Diagnosability
QR-05 Learnability
QR-08 Practical usability and adoption efficiency
```

**Primary risks exercised**

```text
R1  Framework works only for its own demo
R2  Project-specific code leaks into framework core
R3  Target user cannot effectively apply the guidance
R4  POM responsibilities are unclear in real work
R10 Documentation creates more friction than it removes
R12 Framework overhead exceeds framework benefit
```

---

### Initial data and environment context

**Required records / state**

- authenticated Salesforce user,
- permission to view the relevant Account UI,
- permission to create Accounts.

Additional required records, record types, owners, validation dependencies, or
reference data remain unknown until the real flow proves they are needed.

**Reusable / generated data**

Use generated or otherwise unique Account test data where needed to avoid
collisions between repeated runs.

**Cleanup**

Not decided yet.

The actual Salesforce behavior, duplicate rules, retention needs, and project
constraints must be observed before defining a cleanup strategy.

Do not invent cleanup rules in advance.

**Environment**

Salesforce development/test org used for framework acceptance.

Only environment differences relevant to the selected flow need to be captured.

**Secrets and credentials**

Credentials and authenticated browser state must not be committed to Git.

**Restrictions on destructive operations**

- avoid repeated failed authentication attempts that could lock or disrupt the
  test user,
- do not perform broad or unsafe cleanup,
- do not delete records that are not known to have been created by the
  automation,
- do not add destructive behavior merely to make the test easier to repeat.

**Safe repeatability**

Not yet confirmed.

Verify whether duplicate rules, retained Accounts, generated data, login
policies, or other Salesforce rules affect repeated execution.

**Unknowns**

Missing context must be recorded and verified rather than guessed.

---

### AE-0101 — The guide becomes actionable later than expected

**Type**

Iteration 1 usability observation.

**Expectation**

`human-led-adaptation.md` should help the target user move from a concrete
automation need to useful actions without requiring them to first consume a
long conceptual lecture.

**Observation / actual result**

The first user impression was that the early part of the guide felt more like
a lecture than a practical manual.

The user initially described the useful part as starting at Step 5, then
corrected this to Step 4.

From Step 4 onward, the guide started to feel materially more useful because it
asked for concrete project context and prompted real decisions.

The user's reaction changed during use from skepticism toward seeing practical
value.

**Evidence**

Direct execution of the guide during the Salesforce Create Account acceptance
slice.

User observation:

```text
earlier steps
→ "more lecture than manual"

Step 4 onward
→ more concrete
→ starts producing useful project context
```

**Usability comparison**

The guide did begin to reduce uncertainty once it reached concrete capture
steps.

However, the time-to-first-action may be too long for a user who expects a
manual rather than conceptual onboarding.

Would this have been easier without the framework?

```text
UNCLEAR
```

The guide has started to add value, but the exercise is still in progress.

**Impact**

MEDIUM

**Classification**

DOCUMENTATION / USABILITY

**Analysis**

The issue may be information order rather than missing content.

Conceptual rationale may still be valuable, but it may need to sit behind a
shorter actionable path.

Do not change the guide while the current exercise is still producing evidence.

**Decision**

```text
INVESTIGATE
```

**Follow-up**

Complete the human-led adaptation exercise before redesigning the document.

Later assess whether the guide should:

- lead with a short actionable path,
- move rationale into optional/deeper sections,
- use progressive disclosure rather than a single long reading path.

**Learning candidate**

NOT YET

---

### AE-0102 — UI context terminology assumes more automation vocabulary than the target persona may have

**Type**

Iteration 1 usability observation.

**Expectation**

The UI-context section should be understandable enough that the target user can
collect only the context needed for the selected flow.

**Observation / actual result**

Several checklist terms were understandable to an experienced automation
practitioner but ambiguous to a less technical user without examples of purpose
or expected output.

Questions raised during the exercise included:

```text
relevant screens
→ what will screenshots be used for?

reusable components
→ how does a less technical user identify what is actually reusable?

stable locator candidates
→ how does the user know whether a locator is stable?

navigation rules
→ URLs only, user navigation, redirects, tabs, or all underlying traffic?

loading behavior
→ what exactly should be observed?

frames / dialogs / tabs / Shadow DOM
→ what information is needed and why?

screenshots / traces
→ useful for what?
```

An informal second perspective was also collected from a colleague who works
with testing only sporadically and is less technical.

That feedback independently exposed confusion around reusable components,
navigation rules, loading behavior, and frames/Shadow DOM terminology.

This is exploratory feedback, not a representative usability study.

**Evidence**

Human-led guide walkthrough for the Salesforce acceptance slice plus informal
secondary review by a less technical colleague.

**Usability comparison**

The checklist currently says what to capture, but often does not tell the user:

```text
why?
how?
how much?
when can I skip this?
what will I do with the result?
```

Would this have been easier without the framework?

```text
UNCLEAR
```

Without the guide, the user may miss important context entirely.

With the current guide, the user may spend unnecessary time interpreting broad
technical terms.

**Impact**

HIGH

**Classification**

DOCUMENTATION / USABILITY

**Related requirements**

```text
FR-02 Clear artifact mapping
QR-01 Readability
QR-05 Learnability
QR-08 Practical usability and adoption efficiency
```

**Related risks**

```text
R3
R10
R12
```

**Analysis**

The likely problem is not lack of technical depth.

Adding long explanations directly under every checklist item could make the
guide worse by turning it into an even larger wall of text.

The stronger candidate is progressive disclosure:

```text
short main path
→ optional linked practical companion guide
→ examples and tooling only when needed
```

**Decision**

```text
DEFER
```

Do not edit the guide until the current exercise is complete.

**Follow-up**

Evaluate a linked companion document such as:

```text
docs/ui-context-discovery.md
```

without automatically committing to that design yet.

**Learning candidate**

NOT YET

---

### AE-0103 — UI context discovery should use tooling for mechanical collection and keep human judgement for decisions

**Type**

Iteration 1 improvement candidate.

**Expectation**

The framework should reduce unnecessary manual reverse-engineering work without
pretending that tools can make all architecture decisions automatically.

**Observation / actual result**

The Salesforce UI is too large for exhaustive manual discovery to be a
reasonable adaptation requirement.

Several parts of UI-context capture have practical tool-assisted approaches:

```text
stable locator candidates
→ Playwright Codegen
→ candidate validation through repeated checks

navigation behavior
→ Playwright-based navigation recorder / observer

loading behavior
→ Playwright Trace Viewer

frames / dialogs / tabs / Shadow DOM
→ DevTools and/or Playwright-assisted inventory

repeated UI structures
→ automated inventory can produce candidates
→ human or LLM decides whether abstraction is justified
```

A particularly useful candidate is a simple `locator candidate validator`
example that demonstrates:

```text
candidate locator
→ unique?
→ resolves repeatedly?
→ visible/actionable?
→ survives reload/repeated run?
```

**Evidence**

Questions raised during Step 4 of the Salesforce adaptation walkthrough and
evaluation of realistic ways to gather the requested context.

**Usability comparison**

Manual collection across a large Salesforce UI could take disproportionate
time and encourage unnecessary whole-application reverse engineering.

Tool-assisted collection can reduce mechanical work while preserving the
tester’s responsibility for scope and architecture decisions.

Would this have been easier without the framework?

```text
UNCLEAR
```

The current guide identifies useful context categories, but does not yet
provide a practical tool-assisted path for collecting them.

**Impact**

HIGH

**Classification**

USABILITY / DOCUMENTATION / TESTABILITY

**Decision**

```text
DEFER
```

Record as an improvement candidate.

Do not add new framework utilities merely because they are technically possible.

**Follow-up**

After the walkthrough, evaluate whether a concise companion guide should cover:

- Playwright Codegen for locator discovery,
- a small locator candidate validation example,
- navigation recording,
- Trace Viewer for loading investigation,
- optional discovery of frames/dialogs/tabs/Shadow DOM,
- flow-scoped reusable-component candidate discovery.

Prefer links from the main human-led guide over expanding it with large
technical sections.

**Learning candidate**

NOT YET

---

### AE-0104 — Context collection should be scoped to the selected automation path and irrelevant sections should be skippable

**Type**

Iteration 1 usability / scope observation.

**Expectation**

A purpose-first adaptation guide should help the user collect only the context
needed for the selected automation need.

**Observation / actual result**

The first acceptance slice is explicitly POM/UI-focused.

When the guide reached API context, most items were valid in general but not
needed for the Salesforce Create Account POM slice:

```text
base URLs
endpoints
HTTP methods
authentication mechanisms
request/response examples
status codes
async/polling behavior
rate limits
```

The exercise showed that the correct answer for much of this section is:

```text
not needed for this slice
→ skip
```

The same principle applies in the opposite direction for API-only work.

**Evidence**

Human-led adaptation walkthrough of the API-context section while executing a
POM-only acceptance slice.

**Usability comparison**

A universal checklist can protect users from missing context, but it can also
create unnecessary work if every section appears mandatory.

Would this have been easier without the framework?

```text
UNCLEAR
```

The guide gives useful categories, but stronger path selection and explicit
skip guidance may reduce cognitive load.

**Impact**

MEDIUM/HIGH

**Classification**

DOCUMENTATION / USABILITY / POM-BOUNDARY / SOM-BOUNDARY

**Related requirements**

```text
FR-01 Purpose-first adaptation
FR-02 Clear artifact mapping
FR-03 POM project adaptation
FR-04 SOM project adaptation
QR-05 Learnability
QR-08 Practical usability and adoption efficiency
```

**Analysis**

This supports, but does not yet prove, a more branched documentation model:

```text
human-led adaptation
        ↓
selected need
   /           \
UI/POM        API/SOM
```

Combined POM/SOM work can intentionally use both paths later.

**Decision**

```text
DEFER
```

Do not split POM and SOM documentation during the live exercise.

**Follow-up**

After the current walkthrough, assess whether:

- irrelevant context should be explicitly skippable,
- the main guide should link to `ui-context-discovery.md`,
- a later `api-context-discovery.md` is justified,
- POM and SOM paths should be more visibly separated without duplicating the
  whole guide.

**Learning candidate**

NOT YET

---

### AE-0105 — Data and environment context exposed concrete operational risks and useful unknowns

**Type**

Iteration 1 positive usability observation.

**Expectation**

The guide should help the user identify data, environment, safety, and
repeatability concerns before implementation.

**Observation / actual result**

The Data and environment context section triggered concrete project questions:

```text
required records
→ what must already exist before the test?

reusable/generated data
→ what can be reused and what should be unique per run?

cleanup rules
→ what happens to records created by automation?

environment differences
→ which environment differences actually matter to this flow?

secrets and credentials
→ where are they stored and how are they protected?

destructive restrictions
→ could repeated failed login lock the user?
→ could unsafe cleanup remove the wrong data?

safe repeatability
→ can the flow run repeatedly without collisions or harmful side effects?

missing context
→ record unknowns instead of guessing
```

For the Salesforce slice this produced actionable context without requiring the
implementation to start first.

**Evidence**

Human-led adaptation walkthrough of the Data and environment context section.

**Usability comparison**

This part of the guide surfaced risks that could easily be missed in a
script-first approach.

Examples include:

- authentication lockout risk,
- unsafe cleanup,
- duplicate/collision risk,
- retained test data,
- unknown Salesforce rules that should be verified rather than guessed.

Would this have been easier without the framework?

```text
NO — for this specific analysis step, the guide added useful structure.
```

This is not yet a verdict on the whole framework.

**Impact**

HIGH

**Classification**

USABILITY / TEST-DATA / CONFIGURATION

**Related requirements**

```text
FR-07 Project-specific configuration
FR-08 Project-specific test data and state
QR-06 Safety
QR-08 Practical usability and adoption efficiency
```

**Decision**

```text
KEEP
```

The section is useful.

Its wording may still need examples or linked support, but the underlying
questions are producing valuable risk discovery.

**Follow-up**

Continue the walkthrough without changing the guide.

Verify unknowns only when they become relevant to the selected slice.

**Learning candidate**

NOT YET

---

### AE-0106 — Context discovery can expand scope unless the selected slice is actively protected

**Type**

Iteration 1 scope observation.

**Expectation**

The guide should reveal relevant business context without silently expanding a
small acceptance slice into a larger project.

**Observation / actual result**

During business/test context capture, the user naturally connected Account
creation to a broader Salesforce order-creation process.

The user also described an expected result that included both Salesforce UI
visibility and database visibility.

The original acceptance slice, however, was intentionally defined as a small
POM/UI regression verification.

This created a useful distinction:

```text
broader business context
!=
current automation scope
```

**Evidence**

Human-led adaptation walkthrough before implementation.

**Usability comparison**

Broader context is valuable because it explains why the Account matters.

Without explicit scope protection, however, the same analysis could lead to:

```text
Create Account UI test
→ DB verification
→ order process
→ API/SOM work
→ combined architecture
```

before the first small slice has been learned from.

Would this have been easier without the framework?

```text
UNCLEAR
```

The guide successfully elicited context, but the experiment must continue to
check whether later steps help narrow the implementation scope again.

**Impact**

MEDIUM

**Classification**

USABILITY / DOCUMENTATION / POM-BOUNDARY

**Decision**

```text
KEEP SCOPE
```

Keep the broader context recorded, but do not automatically add DB verification
or order creation to I1-S1.

**Follow-up**

Continue the guide and observe whether it naturally protects the smallest useful
scope or whether stronger scope-freezing guidance is needed.

**Learning candidate**

NOT YET

---

## Iteration 1 working status

```text
Acceptance slice selected: YES
Branch created: YES
Human-led guide walkthrough: IN PROGRESS
Implementation started: NO
Framework core changes made: NO
Guide changes made during exercise: NO
Acceptance verdict: NOT YET
```

Current discipline:

> Keep observing before redesigning.

The next evidence entries should continue from the actual walkthrough and
implementation rather than pre-fill expected findings.
