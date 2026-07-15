# Gaps

Known gaps that are incomplete, intentionally deferred, or still need a clear
decision.

This file tracks work that should not be forgotten. It is not a bug list.

The project now has a stronger framework baseline than before:

- CI syntax check through `compileall`,
- pytest collection check,
- unit coverage for the core SOM helpers,
- integration coverage for local FastAPI services,
- a first multi-service SOM workflow,
- a first e-commerce POM browser flow,
- self-starting local E2E services,
- lightweight CI report artifacts,
- documented framework consistency gates.

Important boundary:

```text
The project should not evolve into a demo shop, demo CRM, demo ERP, or demo
Salesforce clone.
```

The repository should remain a reusable POM/SOM framework skeleton.

Demo targets may exist only to make the framework executable and reviewable.

The remaining gaps are mostly about framework structure, adaptation workflow,
documentation clarity, external examples, reporting, dependency compatibility,
and final usefulness validation.

---

## Gap 1 — POM case study exists, but must stay minimal

The framework now has a first realistic POM slice based on a local e-commerce
demo UI.

Current implemented flow:

```text
product search
→ product details
→ add to cart
→ cart total
→ checkout
→ order confirmation
```

The flow is expressed through Page Objects and a reusable component:

```text
EcommerceSearchPage
EcommerceProductPage
EcommerceCartPage
EcommerceCheckoutPage
EcommerceOrderConfirmationPage
PriceSummary
```

This is an important improvement over the earlier Swagger UI smoke test,
because the browser flow now represents a recognizable business journey.

However, this is still not a final POM validation.

It is also not a product roadmap for the local demo shop.

Current limitation:

- the demo shop is intentionally small,
- there is no login,
- there is no real payment flow,
- there is no inventory rule,
- there is no promotion logic,
- there is no responsive/mobile coverage,
- there is no visual regression coverage,
- the UI is local and deterministic by design,
- it does not prove readiness for complex enterprise UI.

These are not necessarily features to add to the local demo.

Most of them should remain out of scope for the repository's demo target.

What the current POM flow proves:

- Playwright can execute a deterministic browser flow,
- the test can stay business-readable,
- raw selectors can stay outside the test body,
- Page Objects can model user actions,
- assertions can remain in the test,
- a replaceable local demo UI can support POM work in CI.

What it does not prove:

- that the framework is ready for Salesforce,
- that the framework is ready for a production e-commerce platform,
- that the local demo should be expanded into a realistic shop.

Status: partially addressed and intentionally capped.

---

## Gap 2 — SOM case study exists, but should remain framework-focused

The SOM layer now has:

- local FastAPI service examples,
- unit coverage for reusable SOM helpers,
- integration coverage for individual services,
- a first multi-service telco order workflow.

The first workflow shows:

```text
customer
→ product
→ order
→ order status change
```

through:

```text
UserService
→ ProductService
→ OrderService
```

This is an important improvement because the tests no longer exercise only
isolated CRUD endpoints.

However, this is still not a final SOM validation.

Current limitation:

- the local demo services are intentionally simple,
- they do not enforce real cross-service referential integrity,
- the workflow proves expression through Service Objects, not full business
  consistency,
- the scenario is still small and local-demo oriented.

Future direction should focus on framework usefulness, not on building richer
fake services.

Useful next work:

- clarify Service Object conventions,
- clarify API fixture patterns,
- clarify test data boundaries,
- document what SOM examples prove and do not prove,
- keep external/live API tests opt-in,
- validate against a real or realistic API later.

Avoid:

- building a complex fake microservice platform,
- adding realistic payment/inventory/order engines only for the demo,
- turning the repository into a sample application.

Status: partially addressed and intentionally bounded.

---

## Gap 3 — Demo target boundary must be protected

The repository now uses a local e-commerce-like target for the first public POM
example.

This is useful because e-commerce is recognizable and naturally maps to:

- Product search,
- Product details,
- Cart,
- Checkout,
- Order confirmation,
- Catalog/Search/Cart/Order/Payment-style services.

However, this does not mean the repository should become an e-commerce demo
application.

The following are out of scope for the local demo target unless a future
architecture decision explicitly changes this:

- payment provider sandbox,
- promo code rules,
- stock reservation,
- concurrent cart updates,
- refund/return flows,
- event-driven order processing,
- logistics/tracking,
- account/order history,
- authorization and user roles,
- mobile/responsive flows,
- accessibility suite,
- realistic product catalog,
- realistic checkout engine.

Those topics may be valuable during final validation against a real or
realistic application.

They should not be implemented as local demo-product features just to make the
demo look richer.

Status: boundary needs discipline.

---

## Gap 4 — External/live examples need cleanup and clear policy

The repository contains tests and services that appear to belong to an external
or legacy demo path, such as auth/customer examples and login-related browser
tests.

These examples may still be useful, but their role must stay explicit.

They should be one of:

- documented external examples,
- moved into an examples area,
- rewritten against local demo services,
- or removed if they no longer support the framework story.

Rules to preserve:

- external/live tests must be opt-in,
- default CI must not depend on live third-party systems,
- external examples must not make the framework look less reusable,
- tests that require private credentials must never be part of default CI.

Status: partially addressed through markers and CI, but still needs cleanup.

---

## Gap 5 — Swagger UI E2E remains a technical smoke test

The Swagger UI E2E tests are now self-starting because the E2E fixtures can
start the local users service.

This makes the local E2E suite more deterministic.

However, Swagger UI is still only a technical smoke test.

It proves:

- a browser can open a local service UI,
- a Page Object can interact with the Swagger UI,
- the service can answer a basic request.

It does not prove:

- realistic POM structure,
- business UI automation,
- e-commerce readiness,
- enterprise UI readiness.

The main POM demonstration should remain the small e-commerce flow, but that
flow should also stay bounded as a framework example.

Status: acceptable as technical smoke.

---

## Gap 6 — Reporting and Allure dashboard are still future work

The CI now produces lightweight pytest reports and workflow summaries.

That improves visibility, but it is not the same as a full Allure dashboard.

Current lightweight reporting:

- JUnit XML files,
- captured pytest output,
- GitHub Actions step summary,
- downloadable `pytest-reports` artifact.

Future reporting work:

- generate Allure results,
- generate a static Allure HTML report,
- decide whether to publish it through GitHub Pages,
- decide which artifacts are useful for UI and API failures,
- document the local and CI reporting workflow.

Status: lightweight reporting added; Allure dashboard deferred.

---

## Gap 7 — Dependency and runner compatibility should be revisited later

The CI runner is currently pinned to `ubuntu-22.04` for compatibility with the
pinned Playwright version.

This is acceptable as a focused fix, but it should not be forgotten.

Future cleanup:

- review pinned dependency versions,
- decide when to update Playwright,
- decide whether the CI runner can safely return to `ubuntu-latest`,
- keep dependency changes separate from framework behavior changes.

Status: deferred.

---

## Gap 8 — Final framework usefulness validation is still open

This is the most important final project question:

```text
Does this framework skeleton actually help automate a concrete application?
```

The project should not be judged only by:

- green CI,
- number of tests,
- documentation quality,
- nice folder structure,
- internal unit/integration coverage,
- local demo applications.

The final validation should apply the skeleton to a concrete or realistic
application context and check whether it actually helps.

This should be treated as a specific UAT-like phase for the framework itself.

It is not UAT of the tested application.

It is acceptance validation of the framework as a tool for an automation tester.

Planned validation approach:

```text
Choose a realistic application context
→ manually fill the framework with application-specific content
→ add Page Objects / Service Objects / fixtures / test data
→ write meaningful tests
→ observe where the framework helps or gets in the way
→ document gaps, friction, and improvements
```

For this validation phase, the framework should be filled manually first.

Reason:

```text
If LLM-generated filling is used too early,
we would mix two questions:

1. Is the framework skeleton useful?
2. Did the LLM fill it correctly?
```

Manual adaptation gives a cleaner answer to the framework question.

AI-powered adaptation can be tested later as a separate capability.

Status: parked for final validation phase.

---

## Gap 9 — Formal framework testing phase should be designed later

After the current development phase, the framework should be tested more
systematically.

This should be closer to ISTQB-style thinking:

- define framework requirements,
- separate test levels,
- define what each level proves,
- map tests to requirements or risks,
- identify gaps,
- execute and summarize results.

Some test levels already exist:

- syntax check,
- collection check,
- unit tests,
- integration tests,
- E2E smoke tests,
- first E2E POM flow.

But the final framework testing phase should be more explicit.

Possible questions:

- What are the functional requirements of the framework?
- What are its non-functional requirements?
- Which requirements are covered by unit tests?
- Which require integration tests?
- Which require a realistic app-context validation?
- Which parts remain out of scope?

Status: parked for later.

---

## Gap 10 — Salesforce/ERP/CRM hard POM validation is future work

E-commerce is the first public demo context, but it is not the hardest possible
POM target.

A future hard POM validation could use Salesforce/ERP/CRM-style UI ideas.

That would be useful because enterprise systems may include:

- highly dynamic UI,
- Shadow DOM,
- complex component trees,
- iframes or overlays,
- long asynchronous loading,
- unstable selectors,
- complex authentication,
- bot-detection or login friction,
- enterprise-specific workflows and permissions.

This future validation would answer a different question:

```text
Can this framework handle a difficult enterprise UI?
```

The current e-commerce demo answers a simpler public-repo question:

```text
Can this framework show a clear, understandable POM/SOM structure on a
realistic business domain?
```

This should happen later by applying the framework to a real or realistic
application context.

It should not be done by building a fake Salesforce, fake ERP, or fake CRM
inside this repository.

Status: future hard validation target.

---

## Gap 11 — Context-aware framework filler is parked

A possible future tool could use this framework skeleton together with
application context to propose project-specific automation artifacts.

This would not be Playwright Codegen 2.0.

It should answer:

```text
Where should this element, action, endpoint, or flow live in the framework?
```

not only:

```text
How can Playwright interact with this element?
```

Possible future architecture:

- local CLI agent,
- replaceable LLM backend,
- repository context,
- application context,
- deterministic UI/API collectors,
- structured JSON output,
- human QA review loop.

This idea should stay parked until the framework has been manually validated
against a realistic application context.

Status: future idea, not current scope.

---

## Recently closed or improved gaps

The following gaps were reduced by recent commits:

### Unit coverage for reusable SOM framework pieces

Added or improved unit coverage for:

- `InMemoryStore`,
- `create_crud_router`,
- `MicroserviceClient`,
- local service Pydantic models,
- `BaseClient`,
- `api/swagger_generator.py`.

### CRUD create contract

Unit tests exposed that `create_item()` was storing only explicitly provided
fields, which dropped Pydantic defaults.

The create path now stores full validated payloads, while the update path still
uses partial updates.

### `BaseClient` HTTP method coverage

`BaseClient` now supports:

- `GET`,
- `POST`,
- `PUT`,
- `PATCH`,
- `DELETE`.

This aligns it with methods that the OpenAPI/Swagger generator may emit.

### Swagger/OpenAPI generator behavior

`api/swagger_generator.py` now has behavior tests for:

- name normalization,
- class name generation,
- tag filtering,
- method name generation,
- generated method rendering,
- unsupported method filtering,
- empty-tag fallback behavior.

### First multi-service SOM workflow

The integration suite now includes a small telco order workflow using:

- `UserService`,
- `ProductService`,
- `OrderService`.

This demonstrates business-readable API orchestration through the SOM layer,
while keeping the limitation explicit: the demo services do not yet model full
cross-service business consistency.

### First e-commerce POM flow

The E2E suite now includes a local e-commerce browser flow:

```text
product search
→ product details
→ add to cart
→ cart total
→ checkout
→ order confirmation
```

This demonstrates a business-readable browser flow through Page Objects.

It does not justify expanding the local demo shop beyond what is needed to
exercise the framework.

### Self-starting E2E services

E2E fixtures now start local services needed by browser tests, including:

- local demo shop,
- local users service for Swagger UI smoke tests.

This makes local E2E execution more deterministic.

### Framework consistency gates

Testing strategy now explicitly documents:

```text
syntax check
→ collection check
→ unit tests
→ integration tests
→ E2E tests
```

This helps explain what the green pipeline actually proves.
