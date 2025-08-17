# Lizearyzacja-statycznej-funkcji-termistora

# Linearyzacja statycznej funkcji termistorów — aplikacja inżynierska (GUI, Python)

> Repozytorium zawiera aplikację do analizy i linearyzacji statycznej charakterystyki termistorów NTC. Program prowadzi użytkownika od modelowania R(T), przez dobór rezystora liniaryzującego oraz propozycje wartości z szeregów E24/E48/E96, po symulację dzielnika napięcia i eksport wyników (CSV/PNG). Dołączono pełny tekst pracy inżynierskiej w PDF.

---

## 🇵🇱 Wersja polska

### 🎯 Cel i zakres (rozwinięte)

Celem projektu jest dostarczenie praktycznego narzędzia inżynierskiego do projektowania torów pomiaru temperatury z termistorem NTC. Aplikacja łączy obliczenia, wizualizację oraz podpowiedzi doboru elementów, aby szybko przejść od danych katalogowych do konfiguracji dzielnika pod ADC.

Zakres funkcjonalny:

* Modelowanie rezystancji R(T) modelem Beta (parametry R0, B; T0 = 25 °C).
* Dobór rezystora liniaryzującego Ropt metodą trzech punktów (Tmin, Tmid, Tmax) w zadanym zakresie.
* Symulacja dzielnika napięcia i wykres Uwy(T) dla Ropt, Rnom oraz propozycji z E‑serii.
* Ocena liniowości na wykresach i eksport danych (CSV/PNG).

Założenia i ograniczenia:

* Analizowana jest statyczna charakterystyka (bez samonagrzewania i dynamiki cieplnej).
* Model Beta jest adekwatny w typowych zakresach; dla bardzo szerokich zakresów zalecany jest Steinhart–Hart (na roadmapie).
* Metoda trzech punktów minimalizuje błąd w środku zakresu; nie gwarantuje globalnego minimum RMS (planowana optymalizacja numeryczna).

---

### 🧠 Podstawy teoretyczne (szczegółowo)

**Charakterystyka NTC:** rezystancja maleje ze wzrostem temperatury. Popularne przybliżenia:

* **Model Beta:**

  ```
  R(T) = R0 * exp( B * (1/T - 1/T0) )
  ```

  gdzie T i T0 w kelwinach (T0 = 298.15 K), R0 = R(T0), B – stała materiałowa. Czułość dR/dT = -(B/T^2) \* R(T) rośnie w niskich temperaturach, co podkreśla nieliniowość.

* **Steinhart–Hart (S–H):**

  ```
  1/T = A + B * ln(R) + C * (ln(R))^3
  ```

  Dokładniejsze dopasowanie na szerokim zakresie kosztem estymacji trzech współczynników. W tej wersji aplikacji wykorzystywany jest model Beta (stabilność, prostota obliczeń w GUI).

**Dzielnik napięcia z NTC:** rozpatrujemy rezystor stały R w szeregu z NTC do masy. Wyjście z dzielnika (napięcie na R):

```
Uwy(T) = Uzasil * R / ( R + R(T) )
```

Nieliniowość R(T) przenosi się na Uwy(T). Celem liniaryzacji jest taki dobór R, aby Uwy(T) możliwie przypominała prostą w zakresie \[Tmin, Tmax].

**Kryterium trzech punktów i wzór na Ropt:**
Dla punktów Tmin, Tmid = (Tmin + Tmax)/2, Tmax wyznaczamy:

```
Rlow = R(Tmin),   Rmid = R(Tmid),   Rhigh = R(Tmax)
Ropt = ( 2*Rlow*Rhigh - Rmid*(Rlow + Rhigh) ) / ( 2*Rmid - (Rlow + Rhigh) )   [warunek: mianownik != 0]
```

Zapewnia to quasi‑liniowy przebieg w węzłach końcowych i środkowym. W praktyce należy sprawdzić dodatniość Ropt oraz unikać zakresów bliskich osobliwości (mianownik → 0).

**Budżet błędów – praktyka pomiarowa:**

* Tolerancja NTC (np. ±1…±5% przy 25 °C) i rozrzut B (np. ±1…±3%).
* Tolerancja i współczynnik temperaturowy rezystora, dryft Uzasil, kwantyzacja i nieliniowość ADC, szumy.
* Samonagrzewanie NTC (mW/K) – ograniczać moc (większe R, krótkie próbkowanie, prądy impulsowe) i zadbać o dobry kontakt termiczny.

---

### 🧮 Metodyka obliczeń (rozwinięta)

1. **Wejście i walidacja**: R0 \[Ω], B \[K], Tmin/Tmax \[°C], Uzasil \[V], opcjonalnie Rnom. Spójność zakresów i dodatniość parametrów.
2. **Konwersja jednostek**: °C → K (dodanie 273.15). T0 = 298.15 K.
3. **Siatka temperatur**: 101 równomiernie rozłożonych punktów w \[Tmin, Tmax].
4. **Model R(T)**: obliczenie Rlow, Rmid, Rhigh oraz pełnej serii R(T) modelem Beta.
5. **Dobór Ropt**: wzór trzech punktów; kontrola mianownika i dodatniości.
6. **Propozycje E‑serii**: funkcje `find_nearest_resistor_with_scaling` i `find_nearest_resistors_with_scaling` zwracają najbliższe wartości z E24/E48/E96 (z automatycznym przeskalowaniem dekady) i ich czytelne formatowanie (Ω/kΩ/MΩ).
7. **Symulacja dzielnika**: Uwy(T) dla Ropt, Rnom i propozycji E‑serii; wielowariantowe wykresy.
8. **Eksport**: CSV z kolumnami `T_C, R_Ohm, U_V` oraz PNG wykresów (wybór ścieżki w okienku dialogowym).

Uwaga numeryczna: zabezpieczenia przed dzieleniem przez zero we wzorze na Ropt oraz przed przepełnieniem exp() dla skrajnych parametrów.

---

### 🧱 Architektura i moduły

* **Core**: `termistor_resistance(T, R0, B)`, `optimal_resistor(Rlow, Rmid, Rhigh)`, `voltage_divider(Vs, R, R_T)`, `linear_equation_from_two_points`, `format_resistance`, funkcje doboru E‑serii.
* **GUI (Tkinter)**: dwustopniowy przepływ pracy, walidacja pól, reset, wybór sposobu doboru rezystora, zapis CSV/PNG.
* **Wizualizacja (Matplotlib)**: wykresy osadzone w oknie Tk (`FigureCanvasTkAgg`).
* **Eksport**: moduł `csv` dla danych tabelarycznych.

---

### 📦 Biblioteki i komponenty

**Standardowa biblioteka Pythona**

* `math` — obliczenia modelu Beta (exp, log).
* `csv` — zapis danych do pliku CSV.
* `tkinter`, `tkinter.ttk`, `tkinter.filedialog`, `tkinter.messagebox` — interfejs użytkownika, dialogi i komunikaty.

**Zewnętrzne**

* `matplotlib` — rysowanie wykresów; `pyplot` i backend `FigureCanvasTkAgg` do integracji z Tk.

Instalacja zależności:

```bash
pip install matplotlib
# Linux: doinstaluj python3-tk (np. apt install python3-tk)
```

---

### 🖱️ Instrukcja użytkownika (GUI)

1. Podaj R0, B oraz zakres temperatur (°C). 2) Oblicz — sprawdź R(T) i Ropt. 3) Dodaj Uzasil i ewentualny Rnom; porównaj z propozycjami E‑serii i zobacz Uwy(T). 4) Zapisz CSV/PNG.

---

### 📊 Rekomendowane metryki jakości

Błąd maksymalny |Uwy(T) − Ulin(T)|, błąd RMS w zakresie, płaskość czułości dU/dT oraz marginesy saturacji. Metryki można wyznaczyć na podstawie CSV.

---

### 🧪 Walidacja i testy

Porównanie punktów referencyjnych z danymi katalogowymi (0/25/85 °C), testy skrajnych B i zakresów temperatur, weryfikacja plików CSV/PNG.

---

### ⚙️ Wydajność i niezawodność

Siatka 101 punktów zapewnia płynne wykresy; czas dominuje renderowanie. Zabezpieczenia: walidacja wejścia, kontrola mianownika, obsługa wyjątków I/O.

---

### 🚀 Roadmap

Steinhart–Hart (A,B,C), optymalizacja numeryczna R (kryteria RMS/MAE, ograniczenie do E‑serii), kompensacja tolerancji i dryftów, eksport XLSX/raport PDF, tryb CLI/batch.

---

### 📁 Struktura repozytorium

```
/
├─ Linearyzacja.py
└─ Dawid Małek-169724-Lineazryzacja statycznej funkcji termistorów.pdf
```

---

### 📦 Wymagania i uruchomienie

* Python >= 3.9
* Zależności: matplotlib (+ python3‑tk na Linuksie)

```bash
pip install matplotlib
python Linearyzacja.py
```

---

### 📄 Licencja

Brak jawnej licencji — wszystkie prawa zastrzeżone przez autora projektu. Aby udostępnić projekt jako open‑source, dodaj plik LICENSE (np. MIT).

---

## 🇬🇧 English version

### 🎯 Purpose and scope (expanded)

Engineering tool for designing NTC‑based temperature front‑ends: from datasheet parameters to an ADC‑ready divider. The app combines modelling, linearization and plotting with E‑series suggestions and data export.

Scope:

* Modelling R(T) with the Beta model (R0, B; T0 = 25 °C).
* Three‑point linearization on \[Tmin, Tmax]: Ropt from Tmin, Tmid, Tmax.
* Divider simulation and Uout(T) for Ropt, Rnom and E‑series candidates.
* CSV/PNG export.

Assumptions: static transfer only; Steinhart–Hart planned for wide ranges.

---

### 🧠 Theory (detailed)

* **Beta model**

  ```
  R(T) = R0 * exp( B * (1/T − 1/T0) )
  dR/dT = −(B/T^2) * R(T)
  ```

  Strong nonlinearity, higher sensitivity at low T.
* **Steinhart–Hart**

  ```
  1/T = A + B * ln(R) + C * (ln R)^3
  ```
* **Divider**

  ```
  Uout(T) = Vs * R / ( R + R(T) )
  ```
* **Three‑point Ropt**

  ```
  Ropt = ( 2*Rlow*Rhigh − Rmid*(Rlow + Rhigh) ) / ( 2*Rmid − (Rlow + Rhigh) )
  ```

---

### 🧮 Computational methodology (expanded)

Input/validation → °C→K → 101‑point grid → Beta R(T) → Ropt (denominator and positivity checks) → E24/E48/E96 suggestions with decade scaling → divider simulation → plots and CSV/PNG export.

---

### 🧱 Architecture

Core math (termistor\_resistance, optimal\_resistor, voltage\_divider), Tkinter GUI (two stages), Matplotlib visualization (FigureCanvasTkAgg), CSV export.

---

### 📦 Libraries

* stdlib: math, csv, tkinter (ttk, filedialog, messagebox)
* third‑party: matplotlib (pyplot, FigureCanvasTkAgg)

Install:

```bash
pip install matplotlib
```

---

### 🧪 Validation & metrics

Reference points vs. datasheets; stress B and temperature spans; report max/RMS linearization error and dU/dT flatness from CSV.

---

### 📄 License

All rights reserved. Add an open‑source LICENSE (e.g., MIT) if needed.
