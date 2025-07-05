from labjack import ljm
import time
import numpy as np
import matplotlib.pyplot as plt

# ---------------- LabJack Setup ----------------
handle = ljm.openS("T7", "ANY", "ANY")

# DIO Konfiguration (siehe vorherige Sub-Task)
CIO_CLK = "CIO0"  # DAC Clock
CIO_DIR = "CIO3"  # Buffer Direction
CIO_OE = "CIO2"   # Output Enable
CIO_CTRL = "CIO1" # Controlline must be HIGH
EIO_PINS = [f"EIO{i}" for i in range(0, 8)]  # EIO0–EIO7

# ---------------- DAC Write Low-Level ----------------
def setup_direction():
    ljm.eWriteName(handle,CIO_CTRL, 1)
    ljm.eWriteName(handle, CIO_DIR, 0)
    ljm.eWriteName(handle, CIO_OE, 0)

def set_data(byte_val):
    for i, pin in enumerate(EIO_PINS):
        bit = (byte_val >> i) & 1
        ljm.eWriteName(handle, pin, bit)

def trigger_dac_clock():
    ljm.eWriteName(handle, CIO_CLK, 1)
    time.sleep(0.01)                    # 10 ms pulsbreite
    ljm.eWriteName(handle, CIO_CLK, 0)

def write_dac_code(code):
    setup_direction()
    set_data(code)
    trigger_dac_clock()
    #ljm.eWriteName(handle, CIO_OE, 1)  # Bus freigeben

# ---------------- Mess- und Analysefunktion ----------------
def measure_response(channel):
    return ljm.eReadName(handle, f"AIN{channel}")

def dac_test(channel=0):
    codes = []
    volts = []

    for code in range(256):
        write_dac_code(code)
        time.sleep(0.01)  # Zeit für Stabilität
        v = measure_response(channel)
        codes.append(code)
        volts.append(v)

    return np.array(codes), np.array(volts)

def analyze_and_plot(codes, volts, title):
    # Lineare Regression
    coeffs = np.polyfit(codes, volts, 1)
    fit_line = np.polyval(coeffs, codes)
    gain, offset = coeffs

    # DNL (Differential Non-Linearity)
    ideal_step = (fit_line[-1] - fit_line[0]) / 255
    actual_steps = np.diff(volts)
    dnl = actual_steps - ideal_step

    # INL (Integral Non-Linearity)
    inl = volts - fit_line

    print(f"--- {title} ---")
    print(f"Gain: {gain:.4f} V/Code")
    print(f"Offset: {offset:.4f} V")
    print(f"Max DNL: {np.max(np.abs(dnl)):.4f} V")
    print(f"Max INL: {np.max(np.abs(inl)):.4f} V")

    # Plot
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(codes, volts, label="Gemessen")
    plt.plot(codes, fit_line, '--', label="Linearer Fit")
    plt.ylabel("Spannung [V]")  
    plt.title(f"{title}: Spannung vs. Code")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(codes[1:], dnl)
    plt.ylabel("DNL [V]")
    plt.title("Differenzielle Nichtlinearität")

    plt.subplot(3, 1, 3)
    plt.plot(codes, inl)
    plt.ylabel("INL [V]")
    plt.xlabel("DAC-Code")
    plt.title("Integrale Nichtlinearität")

    plt.tight_layout()
    plt.show()

# ---------------- Haupttest ----------------
if __name__ == "__main__":
    try:
        # Kanal 0: DAC
        codes, volts = dac_test(channel=0)
        analyze_and_plot(codes, volts, "DAC-Kanal (AIN0)")

        # Optional: Kanal 1 für Vref
        codes_ref, volts_ref = dac_test(channel=1)
        analyze_and_plot(codes_ref, volts_ref, "Referenzkanal (AIN1)")
    finally:
        ljm.close(handle)
