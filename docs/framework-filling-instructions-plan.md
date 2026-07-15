# Framework filling instructions plan

This document parks a future documentation task.

The framework will eventually need simple instructions for filling the skeleton
with application-specific and project-specific content.

This is not current implementation scope.

It belongs near the final validation phase, when the framework is tested
against real or realistic applications.

---

## Purpose

The repository is a reusable POM/SOM framework skeleton.

By itself, it does not know:

- the tested application,
- business flows,
- selectors,
- API endpoints,
- test data,
- roles,
- permissions,
- environment rules,
- project conventions,
- domain risks.

A user must fill the framework with project-specific content.

That filling process needs clear instructions.

---

## Two instruction paths

The project should eventually provide two versions of the instructions:

```text
manual filling
AI-assisted filling
```

These two paths should share the same framework principles, but they should be
written for different user profiles.

---

## Version 1 — Manual filling

Target user:

```text
A person with minimal automation experience.
```

Assumption:

The person may know testing, business flows, or the application, but may not be
very confident with automation architecture.

The manual guide should be simple, explicit, and step-by-step.

It should explain how to:

1. choose one small application flow,
2. decide whether the flow belongs to POM, SOM, or both,
3. identify pages, components, services, fixtures, and test data,
4. create Page Objects,
5. create Service Objects,
6. keep selectors out of tests,
7. keep assertions in tests,
8. keep business logic out of `BasePage` and `BaseComponent`,
9. configure environments safely,
10. run local checks,
11. understand what a green pipeline proves,
12. document remaining gaps.

The manual version should avoid assuming strong programming experience.

It should use short examples and clear file placement rules.

---

## Version 2 — AI-assisted filling

Target user:

```text
A person stronger in business, project context, ISTQB-style thinking, and risk
analysis, but weaker in programming.
```

Assumption:

The person can explain:

- what the system does,
- what the user flow is,
- what is risky,
- what should be tested,
- what data matters,
- what business rules should hold.

But the person may need AI help to translate that knowledge into framework
files.

The AI-assisted guide should explain how to provide AI with:

- repository structure,
- target application description,
- business flow,
- pages/screens,
- API endpoints,
- selectors or locator candidates,
- test data,
- roles and permissions,
- known risks,
- examples of expected assertions,
- constraints and non-goals.

AI may help generate:

- Page Object drafts,
- Service Object drafts,
- fixtures,
- test skeletons,
- selector candidates,
- documentation updates,
- gap notes.

But AI output must be reviewed.

The guide should strongly preserve this rule:

```text
AI can help fill the framework.
QA owns correctness.
```

---

## Manual-first validation rule

Before AI-assisted filling is treated as a capability, the framework should be
validated manually.

Reason:

```text
If AI fills the framework too early, we mix two questions:

1. Is the framework skeleton useful?
2. Did AI fill it correctly?
```

Manual filling gives a cleaner answer to the framework question.

AI-assisted filling can be tested later as a separate capability.

---

## Future deliverables

The future documentation set may include:

```text
docs/filling-manual.md
docs/filling-ai-assisted.md
docs/framework-uat-plan.md
```

Possible supporting checklists:

```text
manual filling checklist
AI prompt checklist
POM placement checklist
SOM placement checklist
test data checklist
environment checklist
review checklist
```

These documents should be created later, not during the current framework-core
phase.

---

## Framework UAT connection

The filling instructions should be validated during framework UAT.

Framework UAT means:

```text
Take a real or realistic application
fill the framework with project-specific content
check whether the framework helps the automation tester
document friction and improvements
```

This is UAT of the framework as a tool.

It is not UAT of the tested application.

---

## Parked decision

Do not build rich demo apps to simulate this process.

Instead:

```text
finish the framework skeleton
prepare simple filling instructions
validate on real or realistic applications
then improve the framework based on friction
```
