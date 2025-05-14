# Extended Test: SN74LS47 + SN74LS165A Bitshift Readout
# Authors: Chris Hölzle, Luis Huber
# Date: 12.05.2025

from labjack import ljm
import time

# Open Labjack device
handle = ljm.openS("ANY", "ANY", "ANY")

# -----------------------------
# Configure digital outputs for SN74LS47 (7-Segment Decoder)
# FIO0-FIO5 are connected to pins A, B, C, D, LT, and BI of SN74LS47
# These are used to simulate all valid input combinations
# -----------------------------
for i in range(6):
    ljm.eWriteName(handle, f"FIO{i}", 0)  # Set Default Output to LOW

# FIO6 is connected to /LOAD (active-low) of SN74LS165A
# LOW: loads the parallel inputs into the register
# HIGH: shifts out serial data on QH
ljm.eWriteName(handle, "FIO6", 1)  # Set HIGH initially (active LOW)

# FIO7 is connected to CLK input of SN74LS165A
# Toggling this pin shifts the bits in the register
ljm.eWriteName(handle, "FIO7", 0)  # Set LOW initially

# FIO8 is connected to QH (serial output) of SN74LS165A
# It will be read to capture the state of the parallel inputs
ljm.eWriteName(handle, "FIO8", 0)  # Set LOW as default

# Provide 5V power via DAC0 for ICs' Vcc
ljm.eWriteName(handle, "DAC0", 5)

# DAC1 is reserved but unused in this example
ljm.eWriteName(handle, "DAC1", 0)

# -----------------------------
# Function: Set inputs to SN74LS47
# A, B, C, D are the BCD input pins
# LT = Lamp Test (active low), BI = Blanking Input (active low)
# Set LT and BI to 1 by default (inactive)
# -----------------------------
def set_sn74ls47_inputs(a, b, c, d, lt=1, bi=1):
    values = [a, b, c, d, lt, bi]
    for i, val in enumerate(values):
        ljm.eWriteName(handle, f"FIO{i}", val)

# -----------------------------
# Function: Generate a single clock pulse
# Clocking the SN74LS165A shifts the next bit to QH
# -----------------------------
def clock_pulse():
    ljm.eWriteName(handle, "FIO7", 1)
    time.sleep(0.001)  # 1 ms HIGH pulse duration
    ljm.eWriteName(handle, "FIO7", 0)
    time.sleep(0.001)  # 1 ms LOW pause

# -----------------------------
# Function: Trigger parallel load on SN74LS165A
# Puts current state of parallel inputs into the internal shift register
# -----------------------------
def load_shift_register():
    ljm.eWriteName(handle, "FIO6", 0)  # Pull /LOAD LOW to latch data
    time.sleep(0.001)
    ljm.eWriteName(handle, "FIO6", 1)  # Return to HIGH for normal shift mode
    time.sleep(0.001)

# -----------------------------
# Function: Read all 8 bits serially from SN74LS165A
# After parallel load, we shift out one bit at a time using CLK
# -----------------------------
def read_shift_register():
    bits = []
    for _ in range(8):
        val = ljm.eReadName(handle, "FIO8")  # Read serial output bit (QH)
        bits.append(int(val))               # Append bit to list
        clock_pulse()                       # Shift to next bit
    return bits

# -----------------------------
# Main test loop
# Iterate through all 4-bit BCD input combinations (0000 to 1111)
# Feed each to SN74LS47 and read the resulting 7-segment output
# via SN74LS165A bitshift register
# -----------------------------
print("Testing SN74LS47 input combinations with SN74LS165A output capture")

# Iterate through all 4-bit binary combinations from 0 to 15 (0000 to 1111)
# e.g. i = 6 (0110) => a = 0110 & 1 = 0, b = 0011 & 1 = 1, c = 0001 & 1 = 1, d = 0000 & 1 = 0
for i in range(16):
    a = (i >> 0) & 1        # a represents the lsb
    b = (i >> 1) & 1
    c = (i >> 2) & 1
    d = (i >> 3) & 1        # d represents the msb

    set_sn74ls47_inputs(a, b, c, d)
    print(f"Set SN74LS47 inputs: A:{a} B:{b} C:{c} D:{d}")

    load_shift_register()  # Capture current 7-segment output state
    data = read_shift_register()
    print(f" -> SN74LS165A Output (QH→QH7): {data}")

    time.sleep(10)  # delay between test cases in seconds

# -----------------------------
# Close connection to LabJack
# -----------------------------
ljm.close(handle)
