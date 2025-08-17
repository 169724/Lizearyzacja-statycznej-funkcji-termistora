import math
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv


# Dane termistorów: rezystancja w temperaturze odniesienia (R0) oraz współczynnik B.
termistor_data = {
    "Murata NCP15XH103F03RC (10kΩ, B=3380K)": {"R0": 10000, "B": 3380},
    "EPCOS B57891M103J (10kΩ, B=3950K)": {"R0": 10000, "B": 3950},
    "Vishay NTCS0603E3103JLT (10kΩ, B=3435K)": {"R0": 10000, "B": 3435},
    "EPCOS B57540G0104J (100kΩ, B=3984K)": {"R0": 100000, "B": 3984},
    "Murata NCP18XH103J03RB (10kΩ, B=3435K)": {"R0": 10000, "B": 3435},
    "Panasonic ERT-J0ET104J (100kΩ, B=4250K)": {"R0": 100000, "B": 4250},
    "TDK NTCG104LH104JTDS (100kΩ, B=4100K)": {"R0": 100000, "B": 4100},
    "Samsung KNS10313 (10kΩ, B=3977K)": {"R0": 10000, "B": 3977},
    "Vishay NTCLE100E3103JB0 (10kΩ, B=3988K)": {"R0": 10000, "B": 3988},
    "TDK NTCG104LH103JTDS (10kΩ, B=3980K)": {"R0": 10000, "B": 3980},
    "TE Connectivity RL1005-582-97-D1 (10kΩ, B=3890K)": {"R0": 10000, "B": 3890},
    "EPCOS B57164K0103J (10kΩ, B=3960K)": {"R0": 10000, "B": 3960},
    "TDK NTCG104EF104FTDS (100kΩ, B=4550K)": {"R0": 100000, "B": 4550},
    "Murata NCP15WL104J03RC (100kΩ, B=4500K)": {"R0": 100000, "B": 4500},
    "Panasonic ERT-J1VG103JA (10kΩ, B=3435K)": {"R0": 10000, "B": 3435},
    "TDK NTCG104LH152JTDS (5kΩ, B=3500K)": {"R0": 5000, "B": 3500},
    "EPCOS B57345S509M (5kΩ, B=3980K)": {"R0": 5000, "B": 3980},
    "Murata NCP21XV103J03RA (1kΩ, B=3375K)": {"R0": 1000, "B": 3375},
    "TDK NTCG164LH102HTDS (1kΩ, B=3300K)": {"R0": 1000, "B": 3300},
    "Vishay NTCS0402E3102JXT (1kΩ, B=3700K)": {"R0": 1000, "B": 3700},
}

# Globalna zmienna dla rezystorów
nominal_resistors = []


def toggle_custom_rnom():
    if custom_rnom_var.get():
        entry_Rnom_custom.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        entry_Rnom_custom.config(state="normal")
        resistor_option.grid_remove()
    else:
        entry_Rnom_custom.grid_remove()
        entry_Rnom_custom.config(state="disabled")
        resistor_option.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        resistor_option.config(state="readonly")


def reset_program():
    global calculation_stage
    result_text.set("")  # Reset wyniku
    calculation_stage = 1  # Reset etapu kalkulacji

    # Reset pól w sekcji linearyzacji
    entry_Uzasil.config(state="normal")  # Upewnij się, że pole Uzas jest odblokowane
    entry_Uzasil.delete(0, tk.END)  # Usunięcie wpisanych wartości z pola Uzas

    # Reset opcji rezystora
    resistor_option.config(state="normal")
    resistor_option.delete(0, tk.END)  # Usunięcie wartości z wyboru rezystora

    # Resetowanie pól dla termistora (R0, B, Tmin, Tmax)
    entry_R0.config(state="normal")  # Ustaw stan na normalny
    entry_R0.delete(0, tk.END)  # Usunięcie wpisanej wartości R0

    entry_B.config(state="normal")  # Ustaw stan na normalny
    entry_B.delete(0, tk.END)  # Usunięcie wpisanej wartości B

    entry_Tmin.config(state="normal")  # Ustaw stan na normalny
    entry_Tmin.delete(0, tk.END)  # Usunięcie wpisanej wartości Tmin

    entry_Tmax.config(state="normal")  # Ustaw stan na normalny
    entry_Tmax.delete(0, tk.END)  # Usunięcie wpisanej wartości Tmax

    # Czyszczenie wykresów
    create_empty_plots()  # Ponownie utwórz puste wykresy

    # Przywrócenie stanu przycisku "Oblicz"
    calculate_button.config(text="Oblicz")

    # Zablokowanie pól, które nie powinny być edytowane po resetowaniu
    entry_Uzasil.config(state="disabled")
    resistor_option.config(state="disabled")


def update_termistor_values(event=None):

    selected_termistor = termistor_var.get()
    if selected_termistor in termistor_data:
        R0_value = termistor_data[selected_termistor]["R0"]
        B_value = termistor_data[selected_termistor]["B"]
        entry_R0.config(state="normal")
        entry_B.config(state="normal")
        entry_R0.delete(0, tk.END)
        entry_R0.insert(0, str(R0_value))
        entry_B.delete(0, tk.END)
        entry_B.insert(0, str(B_value))
        entry_R0.config(state="readonly")
        entry_B.config(state="readonly")


    reset_to_first_stage()


def toggle_custom_data():
    termistor_option.config(state="disabled")
    reset_program()  # Resetuj dane
    if custom_data_var.get():
        entry_R0.config(state="normal")
        entry_B.config(state="normal")
        entry_Tmin.config(state="normal")
        entry_Tmax.config(state="normal")
        termistor_option.config(state="disabled")
    else:
        entry_R0.config(state="readonly")
        entry_B.config(state="readonly")
        termistor_option.config(state="readonly")
        update_termistor_values()  # Zaktualizuj, jeśli nie są to dane własne


def toggle_custom_resistor():
    """Toggle between resistor selection and custom input."""
    if custom_resistor_var.get():
        resistor_option.grid_remove()  # Hide resistor dropdown
        entry_custom_resistor.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        entry_custom_resistor.config(state="normal")
    else:
        entry_custom_resistor.grid_remove()  # Hide custom resistor field
        resistor_option.grid(row=2, column=1, padx=5, pady=5, sticky="ew")


def initialize_custom_resistor_option_state():
    """Initialize state based on custom resistor selection."""
    if custom_resistor_var.get():
        entry_custom_resistor.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        resistor_option.grid_remove()
    else:
        resistor_option.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        entry_custom_resistor.grid_remove()

def initialize_termistor_option_state():
    """Set state for termistor selection or custom entry."""
    if custom_data_var.get():
        termistor_option.config(state="disabled")
    else:
        termistor_option.config(state="readonly")


def termistor_resistance(T, R0, B, T0=298.15):
    if T == T0:
        return R0
    return R0 * math.exp(B * (1 / T - 1 / T0))


def optimal_resistor(R_low, R_mid, R_high):
    numerator = (2 * R_low * R_high) - (R_mid * (R_low + R_high))
    denominator = (2 * R_mid) - (R_low + R_high)
    if denominator == 0:
        return None
    R1 = numerator / denominator
    return R1 if R1 > 0 else None


def voltage_divider(U_zasil, R_opt, R_T):
    return U_zasil * (R_opt / (R_opt + R_T))

def linear_equation_from_two_points(x1, y1, x2, y2):
    A = (y2 - y1) / (x2 - x1)
    B = y1 - A * x1
    return A, B

e6_series = [10, 15, 22, 33, 47, 68]
e12_series = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
e24_series = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]
e48_series = [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261,
              274, 287, 301, 316, 332, 348, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715,
              750, 787, 825, 866, 909, 953]
e96_series = [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162,
              165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249, 255, 261, 267,
              274, 280, 287, 294, 301, 309, 316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442,
              453, 464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732,
              750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976]


# Funkcja do wyszukiwania najbliższej rezystancji w podanych seriach (E24, E48, E96)
# Funkcja do wyszukiwania najbliższej rezystancji w podanych seriach (E24, E48, E96)
def find_nearest_resistor_with_scaling(resistance, series):
    """
    Znajduje najbliższą rezystancję w podanym szeregu poprzez skalowanie wartości.
    """
    best_resistor = None
    min_difference = float('inf')

    # Skalowanie wartości do najbliższej dziesiętnej (10, 100, 1000)
    for value in series:
        for decade_multiplier in [1, 10, 100, 1000]:
            scaled_resistor = value * decade_multiplier
            difference = abs(scaled_resistor - resistance)
            if difference < min_difference:
                min_difference = difference
                best_resistor = scaled_resistor

    return best_resistor
# Funkcja do wyszukiwania najbliższych rezystancji w szeregach E24, E48, E96
def find_nearest_resistors_with_scaling(R1):
    """
    Znajdź najbliższe rezystancje z szeregów (E24, E48, E96)
    """
    nearest_e24 = find_nearest_resistor_with_scaling(R1, e24_series)
    nearest_e48 = find_nearest_resistor_with_scaling(R1, e48_series)
    nearest_e96 = find_nearest_resistor_with_scaling(R1, e96_series)

    return [
        (nearest_e24, "Tolerancja 5% (E24)"),
        (nearest_e48, "Tolerancja 2% (E48)"),
        (nearest_e96, "Tolerancja 1% (E96)")
    ]
# Formatuj rezystancję
def format_resistance(value):
    if value >= 1000:
        return f"{value / 1000:.3f}".replace('.', ',') + " kΩ"
    else:
        return f"{value:.2f}".replace('.', ',') + " Ω"


def reset_calculations():
    """
    Funkcja resetująca wszystkie dane, wyniki, wykresy i zmienne między kalkulacjami.
    """
    global calculation_stage
    calculation_stage = 1
    result_text.set("")  # Resetuj tekst wyniku
    create_empty_plots()  # Resetuj wykresy
    calculate_button.config(text="Oblicz")  # Przywróć domyślny tekst przycisku
    entry_Uzasil.config(state="disabled")  # Zablokuj pole Uzas
    resistor_option.config(state="disabled")  # Zablokuj pole Rnom
    nominal_resistors.clear()  # Wyczyść listę nominalnych rezystorów


def reset_to_first_stage():
    """
    Funkcja wywoływana po każdej zmianie parametrów przez użytkownika.
    Przywraca stan kalkulacji do pierwszego etapu.
    """
    reset_calculations()

# Globalna flaga do śledzenia stanu obliczeń
calculation_stage = 1  # 1 = Pierwsze obliczenie, 2 = Linearyzacja i dzielnik


def calculate():
    global calculation_stage

    try:
        # Clear plots before each new calculation
        ax1.cla()  # Clear all plots for new results
        ax2.cla()
        ax3.cla()
        canvas.draw()  # Redraw the empty plots

        # Collect thermistor data
        R0 = float(entry_R0.get())
        B = float(entry_B.get())
        T_min = float(entry_Tmin.get())
        T_max = float(entry_Tmax.get())

        # Convert temperatures to Kelvin
        T_min_kelvin = T_min + 273.15
        T_max_kelvin = T_max + 273.15
        T_mid = (T_max + T_min) / 2
        T_mid_kelvin = T_mid + 273.15

        # Calculate resistances
        R_low = termistor_resistance(T_min_kelvin, R0, B)
        R_mid = termistor_resistance(T_mid_kelvin, R0, B)
        R_high = termistor_resistance(T_max_kelvin, R0, B)

        # Calculate optimal resistor
        R1 = optimal_resistor(R_low, R_mid, R_high)

        # Enable fields for second stage
        entry_Uzasil.config(state="normal")
        resistor_option.config(state="normal")

        # Update results for both stages
        if R1 is None:
            result_text.set("Nie można obliczyć optymalnego rezystora.")
        else:
            result_message = ""

            # Sprawdzamy, czy wprowadzono wartości Uzas i Rnom
            if entry_Uzasil.get() and resistor_option.get():
                # Obliczenia prądu Ilow i Ihigh (w mA)
                U_zasil = float(entry_Uzasil.get())
                Rnom = float(resistor_option.get())

                Ilow = (U_zasil / (Rnom + R_low)) * 1000  # Konwersja na miliampery (mA)
                Ihigh = (U_zasil / (Rnom + R_high)) * 1000  # Konwersja na miliampery (mA)

                # Wyświetlenie wyników dla Ilow i Ihigh w miliamperach z przecinkiem
                result_message += f"Rʟᴏᴡ = {format_resistance(R_low)} | Iʟᴏᴡ = {format_current(Ilow)} mA\n"
                result_message += f"Rʜɪɢʜ = {format_resistance(R_high)} | Iʜɪɢʜ = {format_current(Ihigh)} mA\n"
            else:
                # Wyświetlenie wyników bez Ilow i Ihigh na pierwszym etapie
                result_message += f"Rʟᴏᴡ = {format_resistance(R_low)} | Iʟᴏᴡ = \n"
                result_message += f"Rʜɪɢʜ = {format_resistance(R_high)} | Iʜɪɢʜ = \n"

            # Wyświetlenie wyniku Ropt
            result_message += f"Rᴏᴘᴛ = {format_resistance(R1)}\n"

            result_message += "\nRezystancje nominalne\n"

            # Clear the list of nominal resistors
            nominal_resistors.clear()

            # Find nearest resistors and update result message
            for value, series in find_nearest_resistors_with_scaling(R1):
                formatted_res = format_resistance(value)
                result_message += f"{series}: {formatted_res}\n"
                nominal_resistors.append((value, f"{series}: {formatted_res}"))

            # Display the results in the text box
            result_text.set(result_message)

            # Update plots for both stages
            if calculation_stage == 1:
                update_plot_with_divider(R0, B, T_min, T_max)
                # Move to stage 2
                calculation_stage = 2
                calculate_button.config(text="Oblicz")

            elif calculation_stage == 2:
                # Collect additional data for voltage divider
                if not entry_Uzasil.get() or not resistor_option.get():
                    messagebox.showerror("Błąd", "Proszę wprowadzić wartości dla Rnom i Uzas.")
                    return

                U_zasil = float(entry_Uzasil.get())
                Rnom = float(resistor_option.get())

                # Update plot with voltage divider calculations
                update_plot_with_divider(R0, B, T_min, T_max, Rnom, U_zasil)

    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawne dane.")

# Funkcja do formatowania prądu (mA) z przecinkiem jako separatorem dziesiętnym
def format_current(current):
    return f"{current:.3f}".replace('.', ',')



def create_empty_plots():
    global fig, ax1, ax2, ax3, canvas
    fig = plt.Figure(figsize=(15, 5))

    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)

    # Tytuły i podpisy osi dla wykresów
    ax1.set_title("Charakterystyka statyczna termistora NTC")
    ax1.set_xlabel("Temperatura (°C)")
    ax1.set_ylabel("Rezystancja termistora (Ω)")
    ax1.grid(True)

    ax2.set_title("Charakterystyka statyczna zlinearyzowana")
    ax2.set_xlabel("Temperatura (°C)")
    ax2.set_ylabel("Rezystancja układu (Ω)")
    ax2.grid(True)

    ax3.set_title("Dzielnik napięcia")
    ax3.set_xlabel("Temperatura (°C)")
    ax3.set_ylabel("Napięcie wyjściowe (V)")
    ax3.grid(True)

    fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1, wspace=0.4)

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    canvas.draw()  # Rysuj wykresy po utworzeniu


def save_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            T_min = float(entry_Tmin.get())
            T_max = float(entry_Tmax.get())
            R0 = float(entry_R0.get())
            B = float(entry_B.get())
            T_min_kelvin = T_min + 273.15
            T_max_kelvin = T_max + 273.15
            temperatures_celsius = [T_min + i * (T_max - T_min) / 100 for i in range(101)]
            temperatures_kelvin = [T + 273.15 for T in temperatures_celsius]

            resistances = [termistor_resistance(T, R0, B) for T in temperatures_kelvin]

            # Użycie obliczonego R1 z funkcji calculate() zamiast entry_Ropt
            if entry_Uzasil.get() and resistor_option.get():
                U_zasil = float(entry_Uzasil.get())
                R_opt = float(resistor_option.get())
                R_mid = termistor_resistance((T_min_kelvin + T_max_kelvin) / 2, R0, B)
                R1 = optimal_resistor(resistances[0], R_mid, resistances[-1])  # Oblicz R1 (optymalną rezystancję)
                linearized_resistances = [(R * R1) / (R + R1) for R in resistances]
                voltages = [voltage_divider(U_zasil, R_opt, R) for R in resistances]
            else:
                linearized_resistances = [""] * len(resistances)
                voltages = [""] * len(resistances)

            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Temperatura (st C)", "Rezystancja (Ohm)", "Rezystancja Zlinearyzowana (Ohm)", "Napiecie wyjsciowe (V)"])
                for T, R, LR, V in zip(temperatures_celsius, resistances, linearized_resistances, voltages):
                    writer.writerow([T, R, LR, V])

            messagebox.showinfo("Sukces", f"Dane zapisane do pliku CSV!\nLokalizacja: {file_path}")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać danych: {str(e)}")

def save_plot_to_png():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        fig.savefig(file_path, format='png')
        messagebox.showinfo("Sukces", "Wykres zapisany do pliku PNG!")


# Aktualizacja wykresu z aproksymacją prostych
# Aktualizacja wykresu z aproksymacją prostych
def update_plot_with_divider(R0, B, T_min, T_max, Rnom=None, U_zasil=None):
    """Funkcja rysująca wykresy."""
    temperatures_celsius = [T_min + i * (T_max - T_min) / 100 for i in range(101)]
    temperatures_kelvin = [T + 273.15 for T in temperatures_celsius]

    # Czyszczenie i ponowne ustawienie tytułów oraz osi dla wszystkich wykresów
    ax1.cla()
    ax2.cla()
    ax3.cla()

    # Wykres 1: Charakterystyka statyczna termistora
    resistances = [termistor_resistance(T, R0, B) for T in temperatures_kelvin]
    ax1.plot(temperatures_celsius, resistances, label="R(T) - Oryginalna", color="blue")
    ax1.set_title("Charakterystyka statyczna termistora NTC")
    ax1.set_xlabel("Temperatura (°C)")
    ax1.set_ylabel("Rezystancja termistora (Ω)")
    ax1.grid(True)

    # Dodaj równanie R(T) bez aproksymacji
    equation_text = f"R(T) = R₀ * exp[B * (1/(T + 273.15) - 1/298.15)]\nR₀ = {R0} Ω, B = {B} K"
    ax1.text(0.12, 0.9, equation_text, transform=ax1.transAxes, fontsize=10, va='top')

    # Ustawienie tytułów i osi dla pozostałych wykresów, nawet jeśli nie są rysowane na pierwszym etapie
    ax2.set_title("Charakterystyka statyczna zlinearyzowana")
    ax2.set_xlabel("Temperatura (°C)")
    ax2.set_ylabel("Rezystancja układu (Ω)")
    ax2.grid(True)

    ax3.set_title("Dzielnik napięcia")
    ax3.set_xlabel("Temperatura (°C)")
    ax3.set_ylabel("Napięcie wyjściowe (V)")
    ax3.grid(True)

    # Po pierwszym kliknięciu pokazujemy tylko pierwszy wykres
    if calculation_stage == 1:
        canvas.draw()  # Rysuje tylko pierwszy wykres, pozostałe zostają puste, ale mają podpisy osi i tytuły
        return

    # Jeśli jesteśmy w drugim etapie, rysujemy pozostałe wykresy
    if Rnom is not None:
        # Obliczamy zlinearyzowane rezystancje, używając Rnom zamiast Roptymalnego
        linearized_resistances = [(R * Rnom) / (R + Rnom) for R in resistances]

        # Wykres 2: Zlinearyzowana charakterystyka
        ax2.plot(temperatures_celsius, linearized_resistances, label="R(T) - Zlinearyzowana", color="green")

        # Aproksymacja zlinearyzowanych rezystancji
        Rmin = linearized_resistances[0]
        Rmax = linearized_resistances[-1]

        # Obliczenie prostej z dwóch punktów na podstawie zlinearyzowanych rezystancji
        A, B_lin = linear_equation_from_two_points(T_min, Rmin, T_max, Rmax)

        # Rysowanie prostej aproksymacji dla zlinearyzowanych rezystancji
        approximated_resistances = [A * T + B_lin for T in temperatures_celsius]
        ax2.plot(temperatures_celsius, approximated_resistances, '--', label="Aproksymacja R(T)", color="orange")
        ax2.grid(True)

        # Dodanie równania prostej na wykresie z trzema miejscami po przecinku
        ax2.text(0.3, 0.9, f"R(T) = {A:.3f} * T + {B_lin:.3f}", transform=ax2.transAxes, fontsize=10, va='top')

    if U_zasil is not None and Rnom is not None:
        # Wykres 3: Dzielnik napięcia
        Rmin_original = termistor_resistance(T_min + 273.15, R0, B)
        Rmax_original = termistor_resistance(T_max + 273.15, R0, B)

        Umin = voltage_divider(U_zasil, Rnom, Rmin_original)
        Umax = voltage_divider(U_zasil, Rnom, Rmax_original)

        # Obliczenie prostej z dwóch punktów dla napięcia
        C, D = linear_equation_from_two_points(T_min, Umin, T_max, Umax)

        # Rysowanie prostej aproksymacji napięcia
        approximated_voltages = [C * T + D for T in temperatures_celsius]
        voltages = [voltage_divider(U_zasil, Rnom, R) for R in resistances]
        ax3.plot(temperatures_celsius, voltages, label="Uwy(T)", color="red")
        ax3.plot(temperatures_celsius, approximated_voltages, '--', label="Aproksymacja U(T)", color="purple")
        ax3.grid(True)

        # Dodanie równania prostej na wykresie z trzema miejscami po przecinku
        ax3.text(0.1, 0.9, f"U(T) = {C:.3f} * T + {D:.3f}", transform=ax3.transAxes, fontsize=10, va='top')

    canvas.draw()



def set_maximized_window(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.state('zoomed')

def on_enter(event):
    """Funkcja wywoływana po naciśnięciu klawisza Enter."""
    calculate_button.invoke()  # Symulacja naciśnięcia przycisku "Oblicz"

# Główne okno
root = tk.Tk()
root.title("Linearyzacja Statycznej Funkcji Termistora")
root.configure(bg="#2E2E2E")  # Tło główne ciemnoszare

# Maksymalizuj okno
set_maximized_window(root)

custom_data_var = tk.BooleanVar(value=True)

# Bind klawisza Enter do funkcji on_enter
root.bind('<Return>', on_enter)  # Wiązanie Enter z przyciskiem "Oblicz"

# Ustawienia okna
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.state('zoomed')

# Czcionki i kolory
label_font = ("Times New Roman", 12, "bold")
entry_font = ("Palatino Linotype", 11)
button_font = ("Arial", 12, "bold")
fg_color = "white"  # Kolor tekstu
result_text = tk.StringVar()

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=0)
root.grid_columnconfigure(3, weight=0)

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(4, weight=1)

frame_plot = tk.Frame(root, bg="#1C1C1C", bd=2, relief="groove")  # Ciemne tło ramek
frame_plot.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
frame_plot.grid_rowconfigure(0, weight=1)
frame_plot.grid_columnconfigure(0, weight=1)
create_empty_plots()

# Sekcja wyboru termistora
frame_termistor = tk.LabelFrame(root, text="Wybór termistora", font=("Times New Roman", 14, "bold"), bg="#1d5286", fg=fg_color)
frame_termistor.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nw")

termistor_var = tk.StringVar(value=list(termistor_data.keys())[0])

# Ustawienie listy rozwijanej na tylko do odczytu
termistor_option = ttk.Combobox(frame_termistor, textvariable=termistor_var, values=list(termistor_data.keys()), state="disable")
termistor_option.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
termistor_option.bind("<<ComboboxSelected>>", update_termistor_values)

# Tworzymy styl dla Checkbutton
style = ttk.Style()

# Konfiguracja niestandardowego stylu z niebieskim tłem i białą czcionką
style.configure(
    "Custom.TCheckbutton",
    background="#1d5286",  # Niebieskie tło
    foreground="white",     # Biała czcionka
    font=("Arial", 11)      # Opcjonalnie: możesz ustawić niestandardową czcionkę
)

# Stworzenie Checkbutton z niestandardowym stylem
custom_data_checkbox = ttk.Checkbutton(
    frame_termistor, text="Własne dane", variable=custom_data_var, command=toggle_custom_data, style="Custom.TCheckbutton"
)
custom_data_checkbox.grid(row=1, column=0, sticky="w", padx=5, pady=5)

# Sekcja linearyzacji
frame_input = tk.LabelFrame(root, text="Parametry termistora", font=("Times New Roman", 14, "bold"), bg="#1d5286", fg=fg_color)
frame_input.grid(row=0, column=0, padx=180, pady=(10, 5), sticky="nw")

for i, label in enumerate([("R₀ (Ω)", "entry_R0"), ("B (K)", "entry_B"), ("Tₘᵢₙ (°C)", "entry_Tmin"), ("Tₘₐₓ (°C)", "entry_Tmax")]):
    lbl = tk.Label(frame_input, text=label[0], font=label_font, fg=fg_color, bg="#1d5286")
    lbl.grid(row=i, column=0, sticky="e", padx=5, pady=2)
    entry = tk.Entry(frame_input, font=entry_font, bg="#505050", fg=fg_color)  # Wpisy ciemne
    entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
    globals()[label[1]] = entry

# Sekcja Wykresy i dzielnik napięcia
frame_divider_inputs = tk.LabelFrame(root, text="Linearyzacja i dzielnik napięcia", font=("Times New Roman", 14, "bold"), bg="#1d5286", fg=fg_color)
frame_divider_inputs.grid(row=0, column=0, padx=180, pady=(170,1), sticky="nw")
frame_divider_inputs.grid_columnconfigure(1, weight=1)

# Pole dla Rnom
tk.Label(frame_divider_inputs, text="Rɴᴏᴍ (Ω)", font=("Times New Roman", 12, "bold"), bg="#1d5286", fg=fg_color).grid(row=0, column=0, padx=5, pady=5, sticky="e")
resistor_option = tk.Entry(frame_divider_inputs, font=("Times New Roman", 12), bg="#505050", fg=fg_color)
resistor_option.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Dodaj pole entry_Rnom_custom do sekcji GUI
entry_Rnom_custom = tk.Entry(frame_divider_inputs, font=("Times New Roman", 12), bg="#505050", fg=fg_color)
entry_Rnom_custom.grid(row=0, column=1, padx=5, pady=5, sticky="w")
entry_Rnom_custom.grid_remove()  # Początkowo ukryte, gdyż używane tylko dla własnych danych


# Pole wyboru U zas (V)
tk.Label(frame_divider_inputs, text="Uᴢᴀs (V)", font=("Times New Roman", 12, "bold"), bg="#1d5286", fg=fg_color).grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_Uzasil = tk.Entry(frame_divider_inputs, font=("Times New Roman", 12), bg="#505050", fg=fg_color)
entry_Uzasil.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Teraz ustawiamy na disabled te pola, po ich utworzeniu
resistor_option.config(state="disabled")
entry_Uzasil.config(state="disabled")

# Przycisk do obliczeń
calculate_button = tk.Button(root, text="Oblicz", bg="#4CAF50", fg="white", font=button_font, relief="raised", bd=2, command=calculate)
calculate_button.grid(row=0, column=0, pady=110, padx=10, sticky="w")

# Przycisk resetowania
reset_button = tk.Button(root, text="Reset", bg="#8aa4b7", fg="white", font=button_font, relief="raised", bd=2, command=lambda: reset_program())
reset_button.grid(row=0, column=0, pady=110, padx=(90, 10), sticky="w")

# Sekcja wyników
frame_result = tk.LabelFrame(root, text="Okno wyników", font=("Times New Roman", 14, "bold"), bg="#1d5286", fg=fg_color)
frame_result.grid(row=0, column=3, padx=10, pady=10, sticky="ne")
frame_result.grid_propagate(True)

result_label = tk.Label(frame_result, textvariable=result_text, justify="left", font=("Cambria", 14, "bold"), bg="#1d5286", fg=fg_color)
result_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

frame_buttons = tk.Frame(root, bg="#2E2E2E")  # Ciemne tło dla dolnej sekcji
frame_buttons.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

save_csv_button = tk.Button(frame_buttons, text="Zapisz dane do CSV", bg="#4169e1", fg="white", font=button_font, relief="raised", bd=2, command=save_to_csv)
save_csv_button.pack(side="left", expand=True, fill="x", padx=(10, 5), pady=10)

save_png_button = tk.Button(frame_buttons, text="Zapisz wykres do PNG", bg="#4169e1", fg="white", font=button_font, relief="raised", bd=2, command=save_plot_to_png)
save_png_button.pack(side="left", expand=True, fill="x", padx=(5, 10), pady=10)

# Add signature label with larger, elegant font and semi-transparent effect
signature_label = tk.Label(root, text="Dawid Małek - Projekt inżynierski", font=("Georgia", 14, "italic"),
                           fg="#696969", bg="#2E2E2F")  # Softer gray font for transparent-like effect
signature_label.grid(row=3, column=0, columnspan=4, pady=(5, 10), sticky="se")


root.mainloop()
