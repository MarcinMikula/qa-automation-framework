# Playwright Codegen — szybkie pozyskiwanie selectorow

Codegen to wbudowane narzedzie Playwrighta, ktore nagrywa interakcje
w przegladarce i generuje gotowy kod z selectorami.

---

## Uruchomienie

```bash
playwright codegen https://twoja-aplikacja.local
```

Otworzy sie przegladarka + okno z kodem. Klikasz w aplikacji — kod sie generuje.

---

## Uzycie z autoryzacja (zapisany stan sesji)

```bash
# Krok 1 — zapisz stan po zalogowaniu
playwright codegen --save-storage=auth.json https://twoja-aplikacja.local

# Krok 2 — uzyj zapisanego stanu w kolejnych sesjach
playwright codegen --load-storage=auth.json https://twoja-aplikacja.local/dashboard
```

---

## Wskazowki

- Preferuj selektory `data-testid` — sa odporne na zmiany CSS i struktury HTML.
  Jesli aplikacja ich nie ma, negocjuj z dev teamem ich dodanie.
- Unikaj selectorow XPath generowanych przez codegen — sa kruche.
- Wygenerowany kod traktuj jako **punkt startowy**, nie gotowy test.
  Przenies selektory do odpowiedniej klasy POM, nie zostawiaj ich w tescie.

---

## Przyklad — co robi codegen vs co powinno trafic do POM

**Codegen generuje:**
```python
page.locator("[data-testid='username']").fill("agent01")
page.locator("[data-testid='btn-login']").click()
```

**Co trafia do `login_page.py`:**
```python
INPUT_USERNAME = "[data-testid='username']"
BTN_LOGIN = "[data-testid='btn-login']"

def login(self, username: str, password: str):
    self.fill(self.INPUT_USERNAME, username)
    self.click(self.BTN_LOGIN)
```

**Co zostaje w tescie:**
```python
login_page.login(AGENT_USER, AGENT_PASS)
```
