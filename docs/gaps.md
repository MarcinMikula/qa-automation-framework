# Gaps

Known gaps that are incomplete, intentionally deferred, or still need a clear
decision.

This file tracks work that should not be forgotten. It is not a bug list.

The repository is now past the initial POM/SOM foundation stage.

Current framework baseline:

- CI syntax check through `compileall`,
- pytest collection check,
- unit coverage for reusable framework helpers,
- integration coverage for local Service Object examples,
- self-starting local E2E services,
- first POM browser flow,
- first multi-service SOM workflow,
- `BasePage`,
- `BaseComponent`,
- `BaseClient`,
- `MicroserviceClient`,
- documented POM foundation checkpoint,
- documented SOM foundation checkpoint,
- documented demo-target boundary,
- documented future manual and AI-assisted filling plan.

Important boundary:

```text
The project should not evolve into a demo shop, demo CRM, demo ERP, or demo
Salesforce clone.
```

The repository should remain a reusable POM/SOM framework skeleton.

Demo targets may exist only to make the framework executable and reviewable.

---

## Gap 1 — Adaptation workflow still needs final practical instructions

The framework has the core POM/SOM structure, but a future user still needs a
clear path for filling it with application-specific content.

Future instructions should explain how to add:

- application-specific Page Objects,
- application-specific components,
- application-specific Service Objects,
- fixtures,
- configuration,
- test data,
- environment rules,
- business assertions,
- project-specific gaps and limitations.

This should eventually exist in two versions:

```text
manual filling
AI-assisted filling
```

Manual filling should be written for a person with minimal automation
experience.

AI-assisted filling should be written for a person stronger in business,
project context, ISTQB-style thinking, and risk analysis, but weaker in
programming.

Status: parked, documented in `framework-filling-instructions-plan.md`.

---

## Gap 2 — Framework UAT is still open

The final validation question remains:

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

This should be treated as UAT of the framework as a tool.

It is not UAT of the tested application.

Planned validation approach:

```text
Choose a realistic application context
→ manually fill the framework with application-specific content
→ add Page Objects / Service Objects / fixtures / test data
→ write meaningful tests
→ observe where the framework helps or gets in the way
→ document gaps, friction, and improvements
```

Manual adaptation should happen before AI-assisted adaptation, so that the
framework question is not mixed with the question of whether AI filled it
correctly.

Status: parked for final validation phase.

---

## Gap 3 — Reporting and Allure dashboard are still future work

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

## Gap 4 — Dependency and runner compatibility should be revisited later

The CI runner is currently pinned to `ubuntu-22.04` for compatibility with the
pinned Playwright version.

Future cleanup:

- review pinned dependency versions,
- decide when to update Playwright,
- decide whether the CI runner can safely return to `ubuntu-latest`,
- keep dependency changes separate from framework behavior changes.

Status: deferred.

---

## Gap 5 — Formal framework testing phase should be designed later

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
- first E2E POM flow,
- first multi-service SOM workflow.

Status: parked for later.

---

## Gap 6 — Salesforce/ERP/CRM hard POM validation is future work

E-commerce is the first public demo context, but it is not the hardest possible
POM target.

A future hard POM validation could use Salesforce/ERP/CRM-style UI ideas.

That should happen later by applying the framework to a real or realistic
application context.

It should not be done by building a fake Salesforce, fake ERP, or fake CRM
inside this repository.

Status: future hard validation target.

---

## Gap 7 — Context-aware framework filler is parked

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

Status: future idea, not current scope.

---

## Gap 8 — Demo target boundary must continue to be protected

The repository currently has minimal deterministic demo targets that make the
framework executable.

They must not become product roadmaps.

Out of scope for local demo targets:

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
- realistic checkout engine,
- fake Salesforce modules,
- fake ERP modules,
- fake CRM lifecycle.

Status: boundary documented; keep enforcing it.

---

## Recently closed or improved gaps

### Legacy external placeholders removed

The inactive telco-style auth/customer/login/dashboard chain was removed from
the framework instead of being quarantined as a legacy example.

Removed areas included:

- unvalidated auth and customer Service Objects,
- login and dashboard Page Objects tied to an unavailable application contract,
- external placeholder tests,
- the root fixture chain used only by those tests,
- unrelated default external URLs and demo credentials,
- unused static telco mock payloads.

The decision was intentional:

```text
Git history preserves the implementation history.
LEARNINGS.md preserves the reasoning.
The active repository keeps only maintained framework code.
```

The generic `external` pytest marker remains available for future real-project
adaptation. The repository no longer ships unvalidated external placeholder
tests.

### POM foundation closed for current framework-core stage

The POM foundation now includes:

- `BasePage`,
- concrete Page Objects,
- `BaseComponent`,
- concrete component example,
- tests owning assertions,
- documentation for Page Objects,
- documentation for components,
- POM foundation checkpoint.

Current POM responsibility split:

```text
BasePage
→ page-level browser mechanics

Concrete Page Objects
→ application-facing page actions and state

BaseComponent
→ component-level browser mechanics

Concrete Components
→ reusable UI fragment behavior and state

Tests
→ business assertions
```

Do not add more demo components such as `MiniCart`, `HeaderNavigation`,
`ProductCard`, or `PaymentWidget` during the framework-core phase.

### SOM foundation closed for current framework-core stage

The SOM foundation now includes:

- `BaseClient`,
- `MicroserviceClient`,
- concrete Service Objects,
- Pydantic request/response models,
- Service Object integration tests,
- multi-service workflow test,
- Swagger/OpenAPI generator helper,
- SOM foundation checkpoint.

Current SOM responsibility split:

```text
BaseClient / MicroserviceClient
→ reusable HTTP mechanics

Concrete Service Objects
→ application-facing service actions and state

Pydantic models
→ request/response structure and validation

Tests
→ business assertions
```

The `BaseClient` / `MicroserviceClient` distinction is now documented:

```text
BaseClient
→ generic low-level HTTP foundation for Service Objects

MicroserviceClient
→ convenience client for simple local JSON microservices
```

Do not add more demo microservices such as `PaymentService`,
`InventoryService`, `PromoService`, `ShippingService`, or `TaxService` during
the framework-core phase.

### Unit coverage for reusable framework pieces

Added or improved unit coverage for:

- `BasePage`,
- `BaseComponent`,
- `BaseClient`,
- `InMemoryStore`,
- `create_crud_router`,
- `MicroserviceClient`,
- local service Pydantic models,
- `api/swagger_generator.py`.

### First POM browser flow

The E2E suite now includes a local browser flow:

```text
product search
→ product details
→ add to cart
→ cart total
→ checkout
→ order confirmation
```

This demonstrates a business-readable browser flow through Page Objects.

It does not justify expanding the local demo target beyond what is needed to
exercise the framework.

### First multi-service SOM workflow

The integration suite now includes a small workflow using:

- `UserService`,
- `ProductService`,
- `OrderService`.

This demonstrates business-readable API orchestration through the SOM layer,
while keeping the limitation explicit: the demo services do not yet model full
cross-service business consistency.

### Self-starting E2E services

E2E fixtures now start local services needed by browser tests.

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
