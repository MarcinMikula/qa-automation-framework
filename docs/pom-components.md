# POM components

A component object represents a reusable UI fragment inside one or more pages.

It is smaller than a Page Object.

Examples:

```text
HeaderNavigation
MiniCart
PriceSummary
ConfirmationBanner
ModalDialog
SearchResultCard
TableRow
```

Components help keep Page Objects smaller and avoid repeating UI fragment logic.

---

## Page Object vs Component Object

A Page Object models a screen or page-level area.

A Component Object models a reusable fragment of UI.

```text
Page Object
= page/screen-level behavior

Component Object
= reusable UI fragment behavior
```

Example:

```text
CartPage
→ owns cart page behavior

PriceSummary
→ owns reusable price summary behavior
```

---

## BaseComponent

`BaseComponent` is a small shared base class for reusable UI components.

It provides component-level helpers such as:

```text
locator(selector)
by_test_id(test_id)
click_by_test_id(test_id)
fill_by_test_id(test_id, value)
text_by_test_id(test_id)
texts_by_test_id(test_id)
is_visible_by_test_id(test_id)
```

It can work in two modes:

```text
page-scoped
root-scoped
```

---

## Page-scoped component

A page-scoped component uses the whole page as its search context.

This is enough when a component appears only once on a page.

```python
price_summary = PriceSummary(page, total_test_id="cart-total")
```

---

## Root-scoped component

A root-scoped component uses a root locator as its search context.

This is useful when the same component appears multiple times.

Example:

```python
row = page.get_by_test_id("order-row").first
order_row = OrderRow(page, root=row)
```

Inside that component, `by_test_id()` should search inside the row, not the
whole page.

This helps avoid accidental matches from other parts of the UI.

---

## What belongs in a component

Good candidates:

```text
MiniCart.open()
MiniCart.item_count()
PriceSummary.total()
ConfirmationBanner.message()
SearchResultCard.open()
TableRow.cell_text("Status")
```

Components should expose reusable UI fragment behavior.

---

## What does not belong in a component

Avoid putting full business workflows in components:

```text
complete_checkout()
approve_customer()
create_opportunity()
change_tariff_plan()
```

Those belong in Page Objects, Service Objects, fixtures, or tests depending on
the level and responsibility.

---

## Assertion boundary

Components may return state.

Tests should own business assertions.

Good:

```python
assert price_summary.total() == "4999.00 PLN"
```

Avoid:

```python
price_summary.assert_total_is("4999.00 PLN")
```

The same rule applies to Page Objects.

---

## Design rule

```text
BasePage provides page-level browser mechanics.
BaseComponent provides component-level browser mechanics.
Concrete Page Objects and components expose application-facing actions/state.
Tests provide business assertions.
```
