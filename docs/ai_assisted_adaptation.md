# AI-assisted adaptation

This framework is designed to work well with AI-assisted development.

The intended use is not to let AI blindly generate a complete test framework.

The intended use is:

```text
provide framework skeleton
+ provide project context
+ ask AI for a focused adaptation
+ manually review and correct the result
```

AI can accelerate boilerplate. QA still owns correctness.

## Safe use cases

AI is useful for:

- proposing Page Object class structure,
- transforming recorded Playwright actions into Page Object methods,
- proposing Service Object methods from API documentation,
- generating initial pytest test skeletons,
- suggesting fixture structure,
- identifying duplicated test mechanics,
- drafting documentation,
- explaining unfamiliar code.

AI is risky for:

- inventing business rules,
- inventing selectors,
- inventing API contracts,
- deciding what is important to test,
- handling secrets,
- making destructive operations,
- bypassing review,
- diagnosing live production failures without evidence.

## Context package for AI

When adapting the framework with AI, provide a focused context package.

Useful context:

```text
1. Application type
2. Main user roles
3. Critical workflows
4. Environment names and restrictions
5. Authentication method, without secrets
6. Locator strategy
7. API documentation or example requests
8. Test data rules
9. What must not be automated
10. Current folder structure
```

Do not provide:

- real passwords,
- private tokens,
- customer data,
- production secrets,
- confidential screenshots unless allowed,
- business data that violates NDA or policy.

## Prompt pattern for POM adaptation

Example prompt:

```text
You are adapting a Python Playwright pytest framework that uses Page Object Model.

Goal:
Create Page Objects for the following UI flow:
- login as service agent
- open Service area
- create Case
- fill required fields
- save
- verify created status

Constraints:
- Keep selectors inside Page Objects.
- Keep assertions in tests.
- Do not hardcode credentials.
- Use environment variables for URLs and users.
- Prefer data-testid or role-based locators.
- Mark uncertain selectors with TODO comments.
- Do not invent business rules beyond the context below.

Project context:
[paste verified context here]

Existing framework structure:
[paste relevant tree here]

Return:
- proposed Page Object files
- proposed pytest test file
- list of assumptions
- list of TODOs requiring manual verification
```

## Prompt pattern for SOM adaptation

Example prompt:

```text
You are adapting a Python pytest framework that uses Service Object Model.

Goal:
Create Service Objects and integration tests for the following API flow:
- create customer
- create order
- fetch order status
- verify customer relationship

Constraints:
- Keep raw HTTP calls inside Service Objects or BaseClient.
- Tests should use domain-level methods.
- Do not hardcode tokens or environment URLs.
- Mark external/live tests with pytest markers.
- Do not invent endpoints beyond the API documentation.

API documentation:
[paste OpenAPI fragment or verified examples]

Existing framework structure:
[paste relevant tree here]

Return:
- proposed Service Object files
- proposed pytest tests
- list of assumptions
- list of TODOs requiring manual verification
```

## Review checklist for AI output

Before accepting AI-generated code, verify:

- Does it fit the existing folder structure?
- Does it preserve POM/SOM boundaries?
- Are selectors real or clearly marked as TODO?
- Are endpoints real or clearly marked as TODO?
- Are credentials and tokens excluded?
- Are assertions meaningful?
- Is test data deterministic?
- Are external dependencies marked?
- Does the code run locally?
- Would a failure be diagnosable?

## Assumption handling

AI-generated code should explicitly label assumptions.

Good assumption comment:

```python
# TODO: verify selector in target application.
BUTTON_SAVE = "[data-testid='save-case']"
```

Bad assumption:

```python
BUTTON_SAVE = "#save"
```

The first version warns the reviewer. The second version looks falsely complete.

## Secrets rule

Never ask AI to process or store real secrets.

Use placeholders:

```text
SALESFORCE_USERNAME=<provided by environment>
SALESFORCE_PASSWORD=<provided by environment>
API_TOKEN=<provided by CI secret>
```

Real values should live in:

- local `.env` excluded from Git,
- CI secrets,
- secret manager,
- secure environment configuration.

## When to stop AI generation

Stop and manually inspect when:

- the model invents endpoints,
- the model invents selectors,
- the model hides assertions in Page Objects,
- the model writes raw HTTP calls directly in tests,
- the model hardcodes credentials,
- the model adds broad abstractions without a real use case,
- the model creates tests that pass but verify nothing important.

## Good AI-assisted outcome

A good AI-assisted adaptation is not perfect code.

A good outcome is:

- a useful first draft,
- visible assumptions,
- clear TODOs,
- preserved architecture boundaries,
- no secrets,
- no fake certainty,
- easy manual review.

The QA engineer remains responsible for turning the draft into reliable automation.
