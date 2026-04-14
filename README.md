# qa-automation-framework

Szkielet frameworka automatyzacji testow w kontekscie systemow enterprise klasy telco/CRM/billing.

## Stack

| Warstwa | Technologia |
|---|---|
| UI (E2E) | Playwright + pytest |
| API | httpx + Service Object Model |
| Dane testowe | SQLAlchemy (SQLite) |
| Raportowanie | Allure |
| CI/CD | GitHub Actions |

## Struktura projektu

```
qa-automation-framework/
├── testdata/       # Konfiguracja srodowiska i baza danych testowych
├── pages/          # Page Object Model — warstwa UI
├── components/     # Reuzywalne komponenty UI
├── api/            # Service Object Model — warstwa API
├── mocks/          # Mockowane odpowiedzi API
└── tests/          # Przypadki testowe (pytest)
```

Szczegoly filozofii projektowej: [PHILOSOPHY.md](PHILOSOPHY.md)

## Uruchomienie

```bash
# Instalacja zaleznosci
pip install -r requirements.txt
playwright install chromium

# Inicjalizacja bazy danych testowych
python testdata/testdb.py

# Uruchomienie testow
pytest tests/ -v

# Raport Allure
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

## Generowanie Service Object ze Swaggera

```bash
python api/swagger_generator.py --swagger path/do/swagger.json --tag customers
```

Szczegoly dotyczace pozyskiwania selectorow: [CODEGEN.md](CODEGEN.md)

## Konfiguracja srodowiska

Zmienne srodowiskowe nadpisuja wartosci domyslne z `testdata/settings.py`:

```bash
BASE_URL=https://staging.telcobilling.com pytest tests/
```
