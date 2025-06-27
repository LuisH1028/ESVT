# -*- coding: utf-8 -*-
"""
Created on Fri May 30 13:37:30 2025

@author: Student
"""

# direction CIO3
# enable output CIO2
# data EIO0 - EIO07
# CLK CIO0



import ljm
import time

handle = ljm.openS("ANY", "USB", "ANY")

def set_dir_output():
    ljm.eWriteName(handle, "CIO3", 1) # CIO3

def enable_buffer():
    ljm.eWriteName(handle, "EIO5", 0)

def disable_buffer():
    ljm.eWriteName(handle, "EIO5", 1)

def set_data(code):
    for i in range(8):
        ljm.eWriteName(handle, f"EIO{i}", (code >> i) & 1)

def pulse_latch():
    ljm.eWriteName(handle, "EIO6", 0)
    time.sleep(0.001)
    ljm.eWriteName(handle, "EIO6", 1)
    time.sleep(0.001)

def write_dac_value(code):
    set_dir_output()
    enable_buffer()
    set_data(code)
    pulse_latch()
    disable_buffer()

# Example: write 0xAA to DAC
write_dac_value(0xAA)+