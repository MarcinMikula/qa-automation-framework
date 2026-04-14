# Test Philosophy

## Kontekst projektu

Framework powstal na bazie doswiadczen z wdrozen enterprise-grade:
systemow billingowych (SERAT/BRM), platform CRM (Salesforce), ERP (SAP Fiori)
oraz portali e-commerce w srodowiskach telekomunikacyjnych i bankowych.

Duze systemy ucza jednej rzeczy: **test, który nie komunikuje jasno swojego celu, 
nie opisuje co weryfikuje ani dlaczego dana asercja jest kluczowa dla biznesu — jest bezużyteczny. 
Pada? Świetnie. 
Ale co to znaczy dla systemu? 
Co się zepsuło? 
Czyja funkcjonalność przestała działać? 
Dobry test odpowiada na te pytania zanim ktokolwiek zacznie debugować**.

---

## Wielka Trojka Automatyzacji (W3A)

Framework jest zbudowany wokol trzech filarow:

### 1. Konfiguracja
Srodowisko nigdy nie jest zahardkodowane w testach.
`testdata/settings.py` + zmienne srodowiskowe = jeden framework, wiele srodowisk (DEV/SIT/UAT/PROD-like).

### 2. Obiekt
Kazda warstwa systemu ma swoj model obiektowy:
- **POM** (Page Object Model) - warstwa UI (`pages/`)
- **SOM** (Service Object Model) - warstwa API (`api/`)
- **Komponenty** - reuzywalne fragmenty UI (`components/`)

Test nie zna selectorow. Test nie zna URL-i. Test mowi jezykiem biznesu:
```python
dashboard.search_customer(msisdn="48100200301")
```

### 3. Stan
Dane testowe sa zarzadzane, nie przypadkowe.
`testdata/testdb.py` dostarcza deterministyczny stan wyjsciowy.
Mocki (`mocks/`) izoluja testy od niestabilnego backendu.

---

## ISTQB w praktyce

| Zasada ISTQB | Realizacja w frameworku |
|---|---|
| Testowanie ujawnia defekty, nie ich brak | Testy negatywne i graniczne obok happy path |
| Wczesne testowanie | Testy API jako pierwsza linia weryfikacji |
| Grupowanie defektow | Scenariusze pogrupowane domenowo (auth, customer, billing) |
| Paradoks pestycydow | Dane parametryzowane (`@pytest.mark.parametrize`) |
| Testowanie zalezy od kontekstu | Konfiguracja przez env — jeden kod, wiele srodowisk |

---

## Piramida testow

```
        [E2E UI]          <- najmniej, najwolniejsze (Playwright)
      [Integracja API]    <- srodkowa warstwa (httpx + SOM)
    [Kontrakty / Mocki]   <- izolacja, szybkie (mocks/)
```

Testy UI weryfikuja przeplyw uzytkownika.
Testy API weryfikuja logike biznesowa.
Mocki chronia przed niestabilnoscia srodowiska.
