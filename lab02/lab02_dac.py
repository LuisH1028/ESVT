# -*- coding: utf-8 -*-
"""
Created on Fri May 30 13:37:30 2025

@author: Torben Burandt, Jannis Rohleder
"""

# direction CIO3
# enable output CIO2
# data EIO0 - EIO07
# CLK CIO0


import numpy as np
import matplotlib.pyplot as plt
from labjack import ljm
from scipy import stats
import time

handle = ljm.openS("ANY", "ANY", "ANY")


data_pints = [f"EIO{i}" for i in range(8)]
dir_pin = "CIO3" # direction buffer
latch = "CIO0" # dac clock
enable_output = "CIO2" # output direction
adc_disable = "CIO1" # crtl line must be high

DAC_output = "AIN1"
ref_output = "AIN0"

dac_voltages = []
ref_voltages = []


def init():
    ljm.eWriteName(handle, adc_disable, 1) # disable ADC lines
    ljm.eWriteName(handle, dir_pin, 0)
    # output of flipflop is set with rising edge
    ljm.eWriteName(handle, latch, 0)
    ljm.eWriteName(handle, enable_output, 0)  # low active
    ljm.eWriteName(handle, dir_pin, 0)
    

    # TODO set inital 0 values to register to prevent magic things happening
    set_data(0)
    pulse_latch()  # set outputs from register to 0


# enable output
def set_dir_output():
    ljm.eWriteName(handle, dir_pin, 0)  # CIO3


def set_output(activation: bool = False):
    """
    Parameters
    ----------
    activation : bool
        DESCRIPTION: Activate (True) or Deactivate(False) output, the actual signal
        is low active therefore the logic is switched in the function
    """
    #if activation is True:
    #    ljm.eWriteName(handle, "EIO2", 0)  # low active activation
    #else:
    #    ljm.eWriteName(handle, "EIO2", 1)
    if activation is True:
        ljm.eWriteName(handle, enable_output, 0)  # low active activation
    else:
        ljm.eWriteName(handle, enable_output, 1)


def set_data(code):
    for i in range(8):
        ljm.eWriteName(handle, f"EIO{i}", (code >> i) & 1)

# more like a clock signal


def pulse_latch():
    time.sleep(0.0001)
    ljm.eWriteName(handle, "CIO0", 1)
    time.sleep(0.0001)
    ljm.eWriteName(handle, "CIO0", 0)


def write_dac_value(code):
    set_dir_output()
    set_output(True)
    set_data(code)
    pulse_latch()
    set_output(False)


def measure_ain(channel):
    return ljm.eReadName(handle, channel)


def run():
    init()
    codes = np.arange(256)

    for code in codes:
        write_dac_value(code)
        time.sleep(0.01)
        dac_v = measure_ain(DAC_output)
        ref_v = measure_ain(ref_output)
        dac_voltages.append(dac_v)
        ref_voltages.append(ref_v)
        print("Code {:3} | DAC: {:.2f} | REF: {:.2f}".format(code, dac_v, ref_v))
#        print(f"Code {code:3} | DAC: {dac_v.2f} | REF: {ref_v.2f}")

    analyze_results(codes, dac_voltages)


def analyze_results(codes, voltages):
    voltages = np.array(voltages)
    codes = np.array(codes)

    # Linear fit
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        codes, voltages)
    lsb_val_v = 5/256
    lsb = (5-lsb_val_v)/(2**8-1)# 2^-8 -1 but max val 5v
    print(f"lsb{lsb}, lsb_val{lsb_val_v}")
    #ideal_voltages = slope * codes + intercept
    #ideal_voltages=slope*codes
    ideal_voltages = lsb*codes
    ideal_diff = (ideal_voltages[1] - ideal_voltages[0])#/ lsb  # idle_step
    print(f"ideaL_diff {ideal_diff}")
 
    
    print(f"\nLinear fit: V = {lsb:.6f} * Code")
    print(f"Gain (LSB): {slope:.6f} V/Code")
    print(f"Offset: {intercept:.6f} V")

    # Ideal voltages from linear fit


    # DNL calculation
    code_diff = np.diff(voltages) # todo maybe matlab diff worng?
    #print(f"code_diff {code_diff}")
    dnl = (code_diff - ideal_diff)# / lsb
    dnl = np.insert(dnl, 0, 0)  # DNL[0] = 0 by definition
    dnl_norm = dnl/lsb
    

    # INL calculation
    inl = (voltages - ideal_voltages)# / lsb
    inl_norm = inl/lsb
    inl_dnl = np.cumsum(dnl)
    inl_intercept  = ((voltages-intercept)-ideal_voltages)
 

    # Report max DNL and INL
    print(f"Max DNL: {np.max(np.abs(dnl)):.6f} LSB")
    print(f"Max INL: {np.max(np.abs(inl)):.6f} LSB")

    # Plot characteristics
    plt.figure(figsize=(14, 8))

    # Transfer characteristic
    plt.subplot(3, 1, 1)
    plt.plot(codes, voltages, label="Measured")
    plt.plot(codes, ideal_voltages, label="Ideal", linestyle='--')
    plt.title("DAC Transfer Characteristic")
    plt.xlabel("DAC Code")
    plt.ylabel("Voltage (V)")
    plt.grid(True)
    plt.legend()

    # DNL plot
    plt.subplot(3, 1, 2)
    plt.plot(codes, dnl_norm)#, width=1.0)
    plt.title("Differential Non-Linearity (DNL) dnl_norm")
    plt.xlabel("DAC Code")
    plt.ylabel("DNL (LSB)")
    plt.grid(True)

    # INL plot
    plt.subplot(3, 1, 3)
    plt.plot(codes, inl_norm, label="INL")
    #plt.plot(codes, inl_dnl, label="INL from cumsum DNL")
    #plt.plot(codes, inl_intercept, label="INL without intercept")
    plt.title("Integral Non-Linearity (INL)")
    plt.xlabel("DAC Code")
    plt.ylabel("INL (LSB)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


run()

ljm.close(handle)


# Example: write 0xAA to DAC
# write_dac_value(0xAA)
