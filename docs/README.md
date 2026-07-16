# Documentation index

This directory contains project-specific documentation for the
`qa-automation-framework` repository.

The root `README.md` is the public landing page.

This directory holds the longer design notes, boundaries, gaps, and adaptation
guides.

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
16. [Gaps](gaps.md)
17. [Future ideas](future-ideas.md)

---

## Document map

| Document | Purpose |
|---|---|
| [architecture-decisions.md](architecture-decisions.md) | Key design decisions and why they were made |
| [project-map.md](project-map.md) | Current map of framework layers, status, and next boundaries |
| [gaps.md](gaps.md) | Open gaps that are known and intentionally tracked |
| [known-limitations.md](known-limitations.md) | Current boundaries, non-goals, and demo-only areas |
| [testing-strategy.md](testing-strategy.md) | Unit, integration, E2E, markers, and CI rules |
| [future-ideas.md](future-ideas.md) | Ideas worth keeping, but not part of the current scope |
| [pom-guide.md](pom-guide.md) | Page Object Model rules for UI automation |
| [pom-base-page.md](pom-base-page.md) | BasePage boundary and reusable POM mechanics |
| [pom-components.md](pom-components.md) | Component Object boundary and reusable UI fragment mechanics |
| [pom-foundation-checkpoint.md](pom-foundation-checkpoint.md) | Current POM foundation status and stop point |
| [som-guide.md](som-guide.md) | Service Object Model rules for API automation |
| [som-foundation-checkpoint.md](som-foundation-checkpoint.md) | Current SOM foundation status and BaseClient vs MicroserviceClient boundary |
| [adaptation-guide.md](adaptation-guide.md) | Short purpose-first orientation for adapting the skeleton |
| [human-led-adaptation.md](human-led-adaptation.md) | Detailed guide from project need to human acceptance |
| [framework-filling-instructions-plan.md](framework-filling-instructions-plan.md) | Status and plan for human-led and AI-assisted filling guidance |
| [example-cases.md](example-cases.md) | Planned UI and API case studies |
| [ai-assisted-adaptation.md](ai-assisted-adaptation.md) | Safe workflow for using AI to adapt the framework |

---

## Current project status

The framework-core POM/SOM foundation is completed for the current stage.

Current status:

```text
POM foundation
→ BasePage, BaseComponent, Page Objects, component example, E2E flow

SOM foundation
→ BaseClient, MicroserviceClient, Service Objects, models, workflow

Demo targets
→ minimal deterministic execution targets only

Adaptation guidance
→ initial human-led purpose-first guide

Future validation
→ framework acceptance on real or realistic applications
```

The repository should not evolve into a rich demo product.

---

## What belongs here

This directory should contain documentation that explains the project itself:

- architecture choices,
- current scope,
- known limitations,
- framework adaptation,
- test strategy,
- example case studies,
- project-specific gaps.

Evergreen testing principles live one level above, in:

```text
AUTOMATION_PRINCIPLES.md
```

That file is intentionally broader than this repository.
