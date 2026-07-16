# Future ideas

Ideas that may be useful later, but are intentionally not part of the current
scope.

This file prevents ideas from being lost while keeping the present project
focused.

---

## Salesforce-like UI case study

Add a realistic POM example based on a CRM flow:

```text
Login
→ open Sales or Service area
→ create Case or Opportunity
→ fill required fields
→ save
→ verify record status or confirmation
```

This should remain a safe demo or training flow, not a copy of any private work
system.

---

## Stronger SOM case study

Add a fuller API scenario:

```text
Create customer
→ create order
→ verify order status
→ fetch related customer data
→ validate response contract
```

This can use local FastAPI services or a public API marked as external.

---

## Parallel filled reference implementations

After the neutral skeleton is completed and successfully validated through
framework acceptance, consider two separate e-commerce reference
implementations.

### Quasi-manual filled version

Working concept:

```text
qa-automation-framework-ecommerce-demo
```

"Manual" does not mean avoiding normal automation tools.

The adaptation may use:

- Playwright Codegen for locator discovery,
- browser developer tools,
- OpenAPI/Swagger documentation,
- IDE refactoring,
- deterministic generators.

A human still owns:

- Page Object and Service Object boundaries,
- test-level decisions,
- business meaning,
- risk selection,
- assertions,
- final review.

### AI-filled version

A second repository may use AI to fill the same neutral skeleton.

It should use:

- the same target application,
- the same scope,
- the same acceptance criteria,
- the same quality gates.

This creates a useful comparison:

```text
quasi-manual adaptation
vs
AI-assisted adaptation
```

The final repository name is not decided yet.

Do not create either reference implementation before framework acceptance has
stabilized the skeleton.

---

## Conditional frontend exploratory-testing agent

Park a possible separate repository for an AI agent that:

- explores a frontend application,
- records observed screens and flows,
- proposes Page Objects and components,
- suggests test scenarios and risks,
- fills or drafts the POM part of this skeleton,
- asks for missing business context,
- leaves final correctness decisions to a human.

This idea is conditional.

First evaluate the AI-filled reference implementation.

If general LLM-assisted tooling already fills the skeleton well enough, a
dedicated agent may add unnecessary complexity.

Build the agent only if the comparison reveals a concrete gap, such as:

- weak exploration coverage,
- poor mapping from UI observations to framework structure,
- missing-context handling,
- unstable locator choices,
- weak risk-based scenario selection,
- inability to maintain a coherent repository over multiple iterations.

The agent should be a response to validated friction, not only to an
interesting architecture idea.

---

## Context-aware framework filler

A possible future tool that uses this framework skeleton together with
application context to propose project-specific automation artifacts.

This would not be Playwright Codegen 2.0.

Playwright Codegen mainly answers:

> How can Playwright interact with this element?

A context-aware framework filler should answer a different question:

> Where should this element, action, endpoint, or flow live in the framework so
> it becomes useful automation?

The tool would not work in isolation from the framework or the tested
application. It would need both:

```text
framework structure
+ application context
+ explored UI/API behavior
+ human QA review
```

Possible outputs:

- proposed Page Objects,
- proposed Service Objects,
- selector placement suggestions,
- endpoint-to-service mapping,
- fixture suggestions,
- test skeletons,
- missing-context questions,
- warnings about weak selectors or unclear assertions.

Example for UI/POM:

```text
Detected flow: create Case

Suggested structure:
pages/salesforce_like/case_page.py
tests/e2e/test_create_case.py
testdata/case_data.py

Suggested Page Object methods:
case_page.open_new_case_form()
case_page.fill_required_case_fields(...)
case_page.save_case()
case_page.current_status()

Human review still needed:
- confirm stable locators,
- confirm required fields,
- confirm expected post-save status,
- confirm whether this flow is worth E2E coverage.
```

Example for API/SOM:

```text
Detected API operation: create customer order

Suggested structure:
api/customer_service.py
api/order_service.py
tests/integration/test_customer_order_flow.py

Suggested Service Object methods:
customer_service.create_customer(...)
order_service.create_order(...)
order_service.get_order_status(...)

Human review still needed:
- confirm contract shape,
- confirm authentication,
- confirm test data strategy,
- confirm meaningful assertions.
```

The key difference from simple recording is that the tool should understand the
target architecture.

It should know that:

- selectors belong in Page Objects, not directly in tests,
- raw HTTP calls belong under Service Objects, not directly in tests,
- assertions belong in tests,
- fixtures should prepare state without hiding scenario meaning,
- generated code is a draft until reviewed by QA.

This idea is a logical extension of the framework skeleton, but it is not part
of the current scope.

It should be revisited only after the framework has been tested against a
realistic UI and API case study.

---

## Contract validation

Add schema or contract-level checks for API responses.

Possible options:

- Pydantic models,
- JSON Schema,
- OpenAPI-based validation,
- lightweight custom validators.

---

## Authentication patterns

Document and demonstrate common authentication patterns:

- bearer token,
- session cookie,
- OAuth-like flow,
- API key,
- test-only local auth.

---

## Data lifecycle helpers

Add clearer helpers for:

- seed data,
- cleanup,
- test isolation,
- unique identifiers,
- safe reuse of known records.

---

## Reporting conventions

Improve Allure story:

- standard step names,
- attachment conventions,
- request/response attachments for API failures,
- screenshot/trace attachments for UI failures.

---

## Template mode

Make it easier to copy this repository as a starting point for another project.

Possible additions:

- checklist for deleting demo services,
- checklist for replacing domain markers,
- sample `.env.example`,
- adaptation prompt for AI tools.
