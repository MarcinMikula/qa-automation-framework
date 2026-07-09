# Documentation index

This directory contains the project-level documentation for `qa-automation-framework`.

The repository is intentionally positioned as a reusable QA automation framework skeleton, not as a plug-and-play product. The docs explain how the skeleton is structured, what belongs to the reusable framework core, what belongs to the replaceable example implementation, and how to adapt the project to a real application.

## Documents

| Document | Purpose |
|---|---|
| [architecture.md](architecture.md) | Explains the framework layers, responsibilities, boundaries, and design decisions. |
| [pom_guide.md](pom_guide.md) | Describes how to use Page Object Model for UI and E2E testing. |
| [som_guide.md](som_guide.md) | Describes how to use Service Object Model for API and integration testing. |
| [adaptation_guide.md](adaptation_guide.md) | Shows how to adapt the skeleton to a real project. |
| [test_strategy.md](test_strategy.md) | Defines the test pyramid, pytest structure, markers, and CI strategy. |
| [example_cases.md](example_cases.md) | Documents current and planned realistic example cases. |
| [known_limitations.md](known_limitations.md) | Lists intentional limitations, deferred work, and scope boundaries. |
| [ai_assisted_adaptation.md](ai_assisted_adaptation.md) | Describes safe AI-assisted adaptation of the framework. |

## Reading order

Recommended order for a new reader:

1. `README.md` in the repository root.
2. `docs/architecture.md`.
3. `docs/pom_guide.md` and `docs/som_guide.md`.
4. `docs/adaptation_guide.md`.
5. `docs/test_strategy.md`.
6. `docs/known_limitations.md`.

## Documentation principle

The root `README.md` should stay concise and explain the repository at a high level.

Detailed reasoning belongs here in `docs/`.

Learning notes and personal development history remain in `LEARNINGS.md`.
