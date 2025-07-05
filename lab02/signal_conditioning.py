from labjack import ljm
import time
import matplotlib.pyplot as plt

# LabJack öffnen
handle = ljm.openS("T7", "ANY", "ANY")

# Testkonfiguration
V_MIN = 0.0
V_MAX = 5.0
STEPS = 50

# Helper: Generiere Testspannungen
def generate_voltage_steps(vmin, vmax, steps):
    step_size = (vmax - vmin) / (steps - 1)
    voltages = []
    for i in range(steps):
        voltages.append(vmin + i * step_size)
    return voltages

# DAC schreiben
def set_dac(channel_name, voltage):
    ljm.eWriteName(handle, channel_name, voltage)

# AIN lesen
def read_ain(channel_index):
    return ljm.eReadName(handle, f"AIN{channel_index}")

# Lineare Regression (manuell, ohne NumPy)
def mean(vals):
    return sum(vals) / len(vals)

def linear_regression(x, y):
    n = len(x)
    x_mean = mean(x)
    y_mean = mean(y)
    num = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    den = sum((x[i] - x_mean)**2 for i in range(n))
    gain = num / den
    offset = y_mean - gain * x_mean
    return gain, offset

# Analyse und Plot
def analyze(vin, vout, title):
    gain, offset = linear_regression(vin, vout)
    fit = [gain * v + offset for v in vin]
    inl = [vout[i] - fit[i] for i in range(len(vin))]
    max_inl = max(abs(i) for i in inl)

    print(f"--- {title} ---")
    print(f"Gain     : {gain:.4f}")
    print(f"Offset   : {offset:.4f} V")
    print(f"Max INL  : {max_inl:.4f} V")

    # Plot
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(vin, vout, 'b-', label="Messung")
    plt.plot(vin, fit, 'r--', label="Lineare Regression")
    plt.title(title)
    plt.xlabel("Eingangsspannung (DAC) [V]")
    plt.ylabel("Ausgangsspannung (AIN) [V]")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(vin, inl, 'm-')
    plt.xlabel("Eingangsspannung (DAC) [V]")
    plt.ylabel("INL [V]")
    plt.title("Integrale Nichtlinearität (INL)")

    plt.tight_layout()
    plt.show()

# Testausführung pro Kanalpaar (DAC → AIN)
def test_channel_pair(dac_name, ain_channel, title):
    vin_list = []
    vout_list = []
    steps = generate_voltage_steps(V_MIN, V_MAX, STEPS)

    for vin in steps:
        set_dac(dac_name, vin)
        time.sleep(0.01)
        vout = read_ain(ain_channel)
        vin_list.append(vin)
        vout_list.append(vout)

    analyze(vin_list, vout_list, title)

# Hauptausführung
if __name__ == "__main__":
    try:
        # DAC0 → AIN0
        test_channel_pair("DAC0", 0, "Signalpfad Test: DAC0 → AIN0")
        # DAC1 → AIN1
        test_channel_pair("DAC1", 1, "Signalpfad Test: DAC1 → AIN1")
    finally:
        ljm.close(handle)
