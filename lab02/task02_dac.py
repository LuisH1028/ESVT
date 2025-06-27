# -*- coding: utf-8 -*-
"""
Created on Fri May 30 13:37:30 2025

@author: Student
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
dir_pin = "CIO3"
latch = "CIO0"
enable_output = "CIO2"

DAC_output = "AIN1"
ref_output = "AIN0"

dac_voltages = []
ref_voltages = []


def init():
    ljm.eWriteName(handle, dir_pin, 0)
    ljm.eWriteName(handle, latch, 0) # output of flipflop is set with rising edge
    ljm.eWriteName(handle, enable_output, 0) # low active
    ljm.eWriteName(handle, dir_pin, 0)
    
    # TODO set inital 0 values to register to prevent magic things happening
    set_data(0)
    pule_latch() # set outputs from register to 0
        
    

# enable output
def set_dir_output():
    ljm.eWriteName(handle, "CIO3", 1) # CIO3


def set_output(activation: bool = False):
    """
    Parameters
    ----------
    activation : bool
        DESCRIPTION: Activate (True) or Deactivate(False) output, the actual signal
        is low active therefore the logic is switched in the function
    """
    if activation is True:
        ljm.eWriteName(handle, "EIO2", 0) # low active activation
    else:
        ljm.eWriteName(handle, "EIO2", 1) # 


def set_data(code):
    for i in range(8):
        ljm.eWriteName(handle, f"EIO{i}", (code >> i) & 1)

# more like a clock signal
def pulse_latch():
    time.sleep(0.001)
    ljm.eWriteName(handle, "CIO0", 1)
    time.sleep(0.001)
    ljm.eWriteName(handle, "CIO0", 0)

def write_dac_value(code):
    set_dir_output()
    set_output(True)
    set_data(code)
    pulse_latch()
    set_output(False)

def measure_ain(channel):
    ljm.eReadName(handle, channel)

def run():
    init()
    codes = np.arange(256)
    
    
    for code in codes:
        write_dac_value(code)
        time.sleep(0.01)
        dac_v = measure_ain(DAC_output)
        ref_v = measure_ain(ref_output)
        dac_voltages.append(dac_v)
        ref_voltages.append(ref_v)a
        
        print(f"Code {code:3} | DAC: {dac_v.4f} | REF: {ref_v.4f}")

















# Example: write 0xAA to DAC
write_dac_value(0xAA)