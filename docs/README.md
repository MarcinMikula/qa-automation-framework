# Documentation index

This directory contains project-specific documentation for the
`qa-automation-framework` repository.

The root `README.md` is the public landing page. This directory holds the
longer design notes, boundaries, gaps, and adaptation guides.

The documentation style intentionally follows the structure used in PhoenixQA:
separate documents for architecture decisions, gaps, known limitations, testing
strategy, and future ideas.

---

## Recommended reading order

1. [Architecture decisions](architecture-decisions.md)
2. [Known limitations](known-limitations.md)
3. [Testing strategy](testing-strategy.md)
4. [POM guide](pom-guide.md)
5. [SOM guide](som-guide.md)
6. [Adaptation guide](adaptation-guide.md)
7. [Example cases](example-cases.md)
8. [AI-assisted adaptation](ai-assisted-adaptation.md)
9. [Gaps](gaps.md)
10. [Future ideas](future-ideas.md)

---

## Document map

| Document | Purpose |
|---|---|
| [architecture-decisions.md](architecture-decisions.md) | Key design decisions and why they were made |
| [gaps.md](gaps.md) | Open gaps that are known and intentionally tracked |
| [known-limitations.md](known-limitations.md) | Current boundaries, non-goals, and demo-only areas |
| [testing-strategy.md](testing-strategy.md) | Unit, integration, E2E, markers, and CI rules |
| [future-ideas.md](future-ideas.md) | Ideas worth keeping, but not part of the current scope |
| [pom-guide.md](pom-guide.md) | Page Object Model rules for UI automation |
| [som-guide.md](som-guide.md) | Service Object Model rules for API automation |
| [adaptation-guide.md](adaptation-guide.md) | How to adapt the skeleton to a real project |
| [example-cases.md](example-cases.md) | Planned UI and API case studies |
| [ai-assisted-adaptation.md](ai-assisted-adaptation.md) | Safe workflow for using AI to adapt the framework |

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
