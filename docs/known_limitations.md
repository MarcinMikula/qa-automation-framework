# Known limitations

Things that are known to be incomplete, simplified, fragile, or intentionally out of scope right now.

This file is a thematic index, not an apology. The repository is a framework skeleton, so some limitations are part of the design.

## Scope boundaries

### This is a skeleton, not a plug-and-play product

The framework does not know a real project's:

- application structure,
- UI locators,
- API contracts,
- authentication flow,
- environment strategy,
- business rules,
- test data ownership,
- failure triage process.

Those must be supplied during adaptation.

Tracked as future TODO: no. This is an intentional scope boundary.

### The repository is not a Salesforce framework

Salesforce-like examples may be added to demonstrate enterprise UI automation patterns, but the repository is not a complete Salesforce automation framework.

Real Salesforce automation requires project-specific decisions around:

- authentication,
- profiles and permissions,
- environment setup,
- object model,
- Lightning UI behavior,
- test data creation,
- organization-specific configuration.

Tracked as future TODO: partially. A Salesforce-like case study is planned, but not a full Salesforce product.

### POM and SOM are both included, but they are not one abstraction

The repository contains both Page Object Model and Service Object Model because realistic enterprise testing often needs UI and API layers.

They should remain separate adapter layers.

Tracked as future TODO: no. This is an intentional architecture decision.

## Current implementation limitations

### Example services are intentionally small

The local FastAPI services exist to make the framework executable and CI-safe.

They do not simulate a full enterprise backend.

Tracked as future TODO: no. They are replaceable examples.

### E2E examples are still demo-level

The current E2E layer demonstrates the POM structure, but it does not yet include a heavy enterprise UI flow such as creating a Case or Opportunity.

Tracked as future TODO: yes. A Salesforce-like POM case study is planned.

### API examples need a stronger business flow

The current API layer demonstrates Service Object usage, but the next iteration should make the flow more business-readable.

Example target:

```text
Create customer
→ create order
→ verify order status
→ fetch related customer data
```

Tracked as future TODO: yes. A clearer SOM case study is planned.

### Authentication is simplified

The skeleton does not implement a complete enterprise authentication strategy.

Real projects may require:

- OAuth,
- SSO,
- MFA handling,
- saved browser storage state,
- token refresh,
- service accounts,
- role-specific users,
- secret management in CI.

Tracked as future TODO: yes. Authentication guidance can be expanded once real case studies are added.

### Environment management is basic

The framework supports the idea of environment configuration, but it does not yet provide a complete multi-environment strategy.

Real projects may need:

- DEV/SIT/UAT/PROD-like separation,
- per-environment credentials,
- feature flags,
- test data availability checks,
- environment health checks,
- safe guards against destructive tests.

Tracked as future TODO: yes.

### Test data strategy is illustrative

The local test data layer demonstrates deterministic data, but real projects require deeper decisions around ownership, cleanup, refresh, masking, and safe creation.

Tracked as future TODO: yes.

### External tests are opt-in by design

Tests that require live systems should be marked as external and should not block default CI.

This means default CI does not prove that every possible live integration works.

Tracked as future TODO: no. This is intentional.

### Code generation is not test design

Swagger/OpenAPI generation and Playwright codegen can speed up scaffolding, but generated code still needs manual review.

Generated code may contain:

- weak names,
- low-level mechanics,
- unstable selectors,
- missing waits,
- missing business assertions,
- wrong assumptions about data.

Tracked as future TODO: no. This is an intentional quality rule.

## Out of scope

The repository currently does not aim to provide:

- self-healing locators,
- AI-driven autonomous test repair,
- full visual regression testing,
- performance testing,
- security testing,
- production monitoring,
- complete contract testing platform,
- full test management integration,
- full Salesforce implementation,
- automatic domain understanding.

These topics may be connected to other tools or future projects, but they are not part of this framework skeleton.

## Risks to watch

### Risk: the skeleton becomes too broad

Because the framework touches UI, API, data, mocks, CI, and example services, it can start looking like a collection of unrelated ideas.

Mitigation:

- keep README focused,
- keep docs explicit,
- separate framework core from examples,
- avoid adding features without a real test-design reason.

### Risk: examples become mistaken for production patterns

Demo code is useful, but it can become misleading if it looks more complete than it is.

Mitigation:

- label examples clearly,
- document what must be replaced,
- avoid fake enterprise claims,
- mark future case studies as case studies, not product support.

### Risk: AI-generated adaptation hides false assumptions

AI can generate plausible Page Objects, Service Objects, and tests that are technically valid but wrong for the business.

Mitigation:

- require manual QA review,
- provide project context explicitly,
- verify selectors and endpoints,
- review business assertions,
- keep generated code out of main without inspection.

## Update rule

Add a limitation here when:

- a behavior is intentionally incomplete,
- a feature is deferred,
- an example is simplified,
- a real project would require manual adaptation,
- a future reader could otherwise overestimate what the framework does.
