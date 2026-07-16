# Framework filling instructions plan

This document tracks the documentation paths for filling the neutral framework
skeleton with application-specific and project-specific content.

The plan is now partially implemented.

---

## Purpose

The repository provides reusable POM/SOM structure.

It does not know:

- the tested application,
- the real project need,
- business flows,
- selectors,
- API endpoints,
- test data,
- roles,
- permissions,
- environment rules,
- project conventions,
- domain risks,
- meaningful expected results.

A user supplies that context during adaptation.

The adaptation must begin from a real project need, not from an empty framework
folder.

---

## Two adaptation paths

The project should support two comparable paths:

```text
human-led adaptation
AI-assisted adaptation
```

They share the same framework principles.

They differ in who drafts and structures the implementation.

In both paths, a human owns correctness and final acceptance.

---

## Path 1 — Human-led adaptation

Status:

```text
Initial guide implemented:
docs/human-led-adaptation.md
```

Target user:

```text
A person who understands the application, testing, architecture, or business
context but may have limited automation-programming confidence.
```

Human-led does not mean avoiding tools.

The user may use:

- Playwright Codegen,
- DevTools,
- OpenAPI/Swagger,
- IDE refactoring,
- deterministic generators,
- LLM assistance.

A human still decides:

- what problem should be solved,
- whether the result is a test or a support workflow,
- the correct test level,
- POM/SOM boundaries,
- scenario and risk selection,
- expected results and assertions,
- final acceptance.

The guide is purpose-first:

```text
project need
→ automation intent
→ artifact selection
→ implementation
→ evidence
→ human acceptance
```

It must be validated during framework acceptance.

---

## Path 2 — AI-assisted adaptation

Status:

```text
Future guide still required.
```

Target user:

```text
A person stronger in business, project context, test analysis, architecture,
and risk thinking than in programming.
```

The user should provide AI with:

- repository structure,
- project need,
- target application description,
- business flow,
- pages and screens,
- API contracts,
- locator candidates,
- test data,
- roles and permissions,
- known risks,
- expected results,
- constraints and non-goals.

AI may draft:

- Page Objects,
- Service Objects,
- workflows,
- fixtures,
- test skeletons,
- selector candidates,
- documentation,
- gap notes.

Core rule:

```text
AI can help fill the framework.
A human owns correctness.
```

---

## Human-led-first validation rule

The framework should first be adapted and accepted through a human-led process.

Reason:

```text
If AI fills the framework first, two questions are mixed:

1. Is the framework skeleton useful?
2. Did AI fill it correctly?
```

The human-led path provides a cleaner baseline.

The AI-assisted path can later be compared against the same target and
acceptance criteria.

---

## Reference implementation plan

After the neutral skeleton passes framework acceptance, create one separate
reference repository:

```text
qa-automation-framework-ecommerce-demo
```

The repository should contain a controlled comparison of:

```text
human-led adaptation
vs
AI-assisted adaptation
```

Both approaches should use:

- the same target shop,
- the same starting skeleton,
- the same scope,
- the same flows,
- the same acceptance criteria,
- the same quality gates.

Do not create two long-lived repositories for this comparison.

The comparison belongs in one reference implementation so that drift and
maintenance cost remain controlled.

---

## Deliverables

Current:

```text
docs/human-led-adaptation.md
```

Future:

```text
docs/ai-assisted-adaptation-guide.md
docs/framework-uat-plan.md
```

Possible supporting checklists:

```text
project-need checklist
POM placement checklist
SOM placement checklist
workflow-vs-test checklist
test-data checklist
environment checklist
AI context checklist
human review checklist
```

---

## Framework acceptance connection

The guides should be validated as part of framework acceptance.

Framework acceptance means:

```text
take a real or realistic application
start from a real testing or test-support need
fill the framework with project-specific content
check whether the framework helps the user
document friction and improvements
```

This is acceptance of the framework as a tool.

It is not UAT of the tested application.

---

## Boundary

Do not build rich local demo applications to simulate adaptation.

Instead:

```text
finish the neutral skeleton
prepare purpose-first filling guidance
validate it against real or realistic systems
improve the skeleton based on evidence
create the separate e-commerce reference implementation
```
