# Future ideas

Ideas that may be useful later, but are intentionally not part of the current scope.

This file prevents ideas from being lost while keeping the present project focused.

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

This should remain a safe demo or training flow, not a copy of any private work system.

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
