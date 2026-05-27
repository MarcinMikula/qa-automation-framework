# LEARNINGS — Dziennik nauki AI-powered QA

Żywy dokument. Każda sekcja to lekcja wyciągnięta z praktyki.
Aktualizuj go za każdym razem, gdy coś zrozumiesz głębiej lub popełnisz błąd, który warto zapamiętać.

---

## Unit Testy + AI

### Trzy rzeczy, które QA musi rozumieć

Zanim zaakceptujesz test wygenerowany przez AI, upewnij się, że rozumiesz:

**1. KOD — co robi funkcja/metoda którą testujesz**
- Jaką odpowiedzialność ma ta metoda w systemie?
- Na jakich danych operuje i skąd je bierze?
- Jakie efekty uboczne wywołuje (zapis do bazy, zmiana stanu, wywołanie zewnętrzne)?

**2. TEST — co unit test sprawdza w tej funkcji**
- Jaką jedną rzecz weryfikuje ten konkretny test?
- Czy nazwa testu jednoznacznie opisuje scenariusz i oczekiwany rezultat?
- Czy asercja jest precyzyjna — sprawdza dokładnie to, co ważne biznesowo?

**3. SETUP — dane na których testy pracują**
- Skąd pochodzą dane testowe (seed, fixture, mock, generowane inline)?
- Czy dane są izolowane — test nie zmienia stanu innego testu?
- Czy zestaw danych pokrywa scenariusze, które faktycznie wystąpią w produkcji?

---

### Jak ocenić czy AI wygenerował sensowny test

Dla każdego testu zadaj sobie pięć pytań:

- **Co robi dana funkcja/metoda?**
  Jeśli nie potrafisz odpowiedzieć jednym zdaniem — wróć do kodu.

- **Jakie przyjmuje dane wejściowe?**
  Jakie typy, zakresy, wartości graniczne? Co się dzieje z `null`, pustym stringiem, duplikatem?

- **Co zwraca i w jakich warunkach?**
  Happy path, ścieżka błędu, wyjątek — czy test pokrywa tylko jeden z tych przypadków?

- **Czy test weryfikuje coś wartościowego?**
  Test, który zawsze przechodzi niezależnie od implementacji, jest gorszy niż brak testu.

- **Czy pokrywa przypadki brzegowe?**
  `null`, `empty`, `duplicate`, wartości poza zakresem, brak wymaganego pola — to miejsca, gdzie produkcja wybucha najczęściej.

---

### Rola QA w AI-powered świecie

> AI przyspiesza pisanie testów 10x.
> QA nadal musi rozumieć biznes, oceniać jakość tego co AI wygenerował
> i diagnozować gdy coś pada.

Konkretnie oznacza to:

- **AI generuje szkielet** — QA decyduje, czy scenariusze mają sens domenowo.
- **AI nie zna kontekstu biznesowego** — QA wie, że `OVERDUE` dla zawieszonego konta to inny priorytet niż `UNPAID` dla aktywnego.
- **AI nie diagnozuje** — gdy test pada o 3 w nocy w CI, to QA czyta logi i rozumie, co się zepsuło i dlaczego.
- **AI nie ocenia wartości testu** — test może być poprawny technicznie i bezużyteczny biznesowo jednocześnie.

Dobrze wygenerowany test to tylko punkt startowy. Wartościowy test to ten, który rozumiesz i potrafisz obronić na review.

---

## Piramida testów

Trzy poziomy — im wyżej, tym wolniej, drożej i trudniej o izolację.

```
            ▲
           /E2E\          <- najmniej testów, najwolniejsze
          / UI  \            Playwright, pełny flow przez przeglądarkę
         /-------\           Testuj krytyczne ścieżki biznesowe
        /   API   \       <- warstwa środkowa
       / Integracja\         httpx + Service Object Model
      /-------------\        Testuj kontrakty, kody HTTP, strukturę odpowiedzi
     /  Unit / Model  \   <- najwięcej testów, najszybsze
    /  Dane / Logika   \     pytest + SQLAlchemy :memory:
   /--------------------\    Testuj każdy constraint, default, edge case
```

### Poziom 1 — Unit

- **Co testuje:** pojedyncza funkcja, metoda, model danych — w izolacji.
- **Izolacja:** baza `sqlite:///:memory:`, mocki dla zewnętrznych zależności.
- **Kiedy pada:** błąd w logice domenowej, constraint bazy, nieprawidłowy default.
- **Prędkość:** milisekundy. Powinny działać przy każdym commicie.

### Poziom 2 — API / Integracja

- **Co testuje:** komunikacja między warstwami — klient HTTP, endpoint, format odpowiedzi.
- **Izolacja:** Service Object Model (`api/`), opcjonalnie mocki (`mocks/`).
- **Kiedy pada:** zmiana kontraktu API, błąd autoryzacji, nieoczekiwana struktura JSON.
- **Prędkość:** sekundy. Uruchamiaj przed mergem.

### Poziom 3 — E2E / UI

- **Co testuje:** pełny scenariusz użytkownika przez przeglądarkę — od logowania do wyniku.
- **Izolacja:** brak pełnej izolacji — test dotyka prawdziwego środowiska.
- **Kiedy pada:** zmiana selektorów, timeout sieci, problem z renderowaniem.
- **Prędkość:** minuty. Uruchamiaj na dedykowanym środowisku (SIT/UAT).

---

*— kolejne sekcje będą tu dodawane wraz z postępem projektu —*
