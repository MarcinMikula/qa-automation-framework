# Documentation index

This directory contains project-specific documentation for the
`qa-automation-framework` repository.

The root `README.md` is the public landing page.

This directory contains longer design notes, boundaries, gaps, testing rules,
and adaptation guidance.

---

## Recommended reading order

1. [Architecture decisions](architecture-decisions.md)
2. [Known limitations](known-limitations.md)
3. [Testing strategy](testing-strategy.md)
4. [Project map](project-map.md)
5. [POM guide](pom-guide.md)
6. [POM BasePage](pom-base-page.md)
7. [POM components](pom-components.md)
8. [POM foundation checkpoint](pom-foundation-checkpoint.md)
9. [SOM guide](som-guide.md)
10. [SOM foundation checkpoint](som-foundation-checkpoint.md)
11. [Adaptation guide](adaptation-guide.md)
12. [Human-led adaptation guide](human-led-adaptation.md)
13. [Framework filling instructions plan](framework-filling-instructions-plan.md)
14. [Example cases](example-cases.md)
15. [AI-assisted adaptation](ai-assisted-adaptation.md)
16. [Framework requirements](framework-requirements.md)
17. [Framework acceptance plan](framework-acceptance-plan.md)
18. [Framework acceptance evidence](framework-acceptance-evidence.md)
19. [Gaps](gaps.md)
20. [Future ideas](future-ideas.md)

---

## Document map

| Document | Purpose |
|---|---|
| [architecture-decisions.md](architecture-decisions.md) | Current design decisions and why they were made |
| [project-map.md](project-map.md) | Framework layers, status, and next boundaries |
| [gaps.md](gaps.md) | Open work, deferred validation, and recently closed gaps |
| [known-limitations.md](known-limitations.md) | Current boundaries and evidence limits |
| [testing-strategy.md](testing-strategy.md) | Consistency gates, test levels, markers, and CI |
| [future-ideas.md](future-ideas.md) | Ideas worth keeping outside current scope |
| [pom-guide.md](pom-guide.md) | Page Object Model rules |
| [pom-base-page.md](pom-base-page.md) | BasePage boundary and reusable mechanics |
| [pom-components.md](pom-components.md) | Component Object boundary |
| [pom-foundation-checkpoint.md](pom-foundation-checkpoint.md) | Current POM status and stop point |
| [som-guide.md](som-guide.md) | Service Object Model rules |
| [som-foundation-checkpoint.md](som-foundation-checkpoint.md) | Current SOM status and client boundary |
| [adaptation-guide.md](adaptation-guide.md) | Short purpose-first adaptation path |
| [human-led-adaptation.md](human-led-adaptation.md) | Detailed path from project need to human acceptance |
| [framework-filling-instructions-plan.md](framework-filling-instructions-plan.md) | Human-led and AI-assisted guidance plan |
| [example-cases.md](example-cases.md) | Current examples, acceptance boundary, and future reference repository |
| [ai-assisted-adaptation.md](ai-assisted-adaptation.md) | Preliminary AI guardrails and comparison boundary |
| [framework-requirements.md](framework-requirements.md) | Initial acceptance requirements, including practical usability and adoption-efficiency expectations |
| [framework-acceptance-plan.md](framework-acceptance-plan.md) | Risk-based incremental acceptance strategy, target-user boundaries, usability north star, and entry/exit criteria |
| [framework-acceptance-evidence.md](framework-acceptance-evidence.md) | Raw acceptance observations, evidence, working decisions, and re-test results |

---

## Current project status

```text
Framework-core POM/SOM foundation
→ completed for the current stage

Local execution targets
→ intentionally minimal and deterministic

Human-led adaptation guidance
→ initial guide implemented

Public documentation
→ aligned before framework acceptance

Framework acceptance
→ Iteration 0 test basis established: requirements, risks, plan, and evidence log

Next execution phase
→ select and run the first small human-led acceptance slice

AI-assisted adaptation
→ guarded future comparison after the human-led baseline
```

The repository should not evolve into a rich demo product.

---

## What belongs here

This directory should explain:

- architecture choices,
- current scope,
- known limitations,
- framework adaptation,
- testing strategy,
- current examples,
- acceptance gaps,
- future ideas.

Evergreen testing principles live in:

```text
AUTOMATION_PRINCIPLES.md
```
