# AI-assisted adaptation

This framework can be adapted with AI assistance, but generated output should not be trusted
without review.

---

## Useful AI inputs

When asking AI to adapt the framework, provide:

- application type,
- main user roles,
- key workflows,
- available environments,
- authentication method,
- UI locator strategy,
- API documentation,
- test data constraints,
- examples of existing manual test cases,
- known flaky or risky areas.

The more precise the context, the less the model has to invent.

---

## Good AI tasks

AI can help draft:

- Page Objects,
- Service Object methods,
- fixtures,
- data builders,
- mock responses,
- test skeletons,
- naming conventions,
- refactoring proposals,
- documentation updates.

---

## Dangerous AI tasks

Do not let AI decide alone:

- which business scenario matters,
- whether a test should exist,
- whether a generated assertion is meaningful,
- whether data is realistic,
- whether a locator is stable,
- whether an API contract is correct,
- whether a test belongs at UI, API, or unit level.

Those are QA decisions.

---

## Review checklist

Before accepting AI-generated automation, answer:

- What behavior does this test verify?
- Why does this behavior matter?
- What input data does it use?
- What is the expected result?
- Is this the right test level?
- Is the assertion meaningful?
- Are locators or endpoints verified?
- Can the test run repeatedly?
- Will the failure be useful to diagnose?

If you cannot explain the test, do not merge it.

---

## Safe workflow

1. Give AI the framework structure.
2. Add project-specific context.
3. Ask for a first draft.
4. Review assumptions.
5. Replace fake details with verified facts.
6. Run locally.
7. Add or adjust assertions.
8. Commit only reviewed code.

AI accelerates scaffolding.

QA owns correctness.
