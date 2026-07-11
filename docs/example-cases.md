# Example cases

Planned realistic case studies for the framework skeleton.

These examples should demonstrate the structure without pretending to automate
a private enterprise system out of the box.

---

## Case 1 — Salesforce-like UI flow with POM

Purpose: demonstrate how the POM layer can model a heavy CRM-style UI flow.

Candidate flow:

```text
Login
→ open Sales or Service area
→ create Case or Opportunity
→ fill required fields
→ save
→ verify record status or confirmation
```

Expected framework elements:

```text
pages/
├── login_page.py
├── dashboard_page.py
└── salesforce_like/
    ├── case_page.py
    └── opportunity_page.py

tests/e2e/
└── test_salesforce_like_case.py
```

Rules:

- no real corporate data,
- no private selectors,
- no credentials,
- no claim that this automates real Salesforce out of the box,
- focus on structure and maintainability.

---

## Case 2 — API / SOM flow

Purpose: demonstrate how the SOM layer can model business API operations.

Candidate flow:

```text
Create customer
→ create order
→ verify order status
→ fetch related customer data
→ validate response contract
```

Expected framework elements:

```text
api/
├── customer_service.py
├── order_service.py
└── product_service.py

tests/integration/
└── test_customer_order_flow.py
```

Rules:

- prefer deterministic local services for CI,
- mark live public APIs as `external`,
- keep raw HTTP details inside Service Objects,
- make tests describe business behavior.

---

## Case 3 — AI-assisted adaptation demo

Purpose: show how this skeleton can be provided to AI together with project
context to generate first-draft Page Objects or Service Objects.

The demo should include:

- safe prompt template,
- required project context,
- review checklist,
- example of correcting hallucinated assumptions.

This should stay documentation-first until the framework code is stable.
