# filename: 7segment_labjack.py
# author: Torben Burandt, Jannis Rohleder
# version: 1.1
# date: 16.05.2025

from labjack import ljm
import time

# Open LabJack T7
handle = ljm.openS("ANY", "ANY", "ANY")

# Define FIO/AIN mappings
pins = {
    "LT": "FIO5",
    "RBI": "FIO4",
    "D": "FIO2",
    "C": "FIO7",
    "B": "FIO6",
    "A": "FIO3",
    "CLK": "FIO1",
    "PARALLEL_LOAD": "FIO0",
    "SER_IN": "AIN0",
    "SER_N_IN": "AIN1"
}

# Configure digital outputs
outputs = ["LT", "RBI", "D", "C", "B", "A", "CLK", "PARALLEL_LOAD"]
for pin in outputs:
    ljm.eWriteName(handle, pins[pin], 1)

# Truth table for 7448
test_vectors = [
    {"label": "0",  "LT": 1, "RBI": 1, "D": 0, "C": 0, "B": 0, "A": 0, "expected": [0,1,1,1,1,1,1]},
    {"label": "1",  "LT": 1, "RBI": 1, "D": 0, "C": 0, "B": 0, "A": 1, "expected": [0,0,0,0,1,1,0]},
    {"label": "2",  "LT": 1, "RBI": 1, "D": 0, "C": 0, "B": 1, "A": 0, "expected": [1,0,1,1,0,1,1]},
    {"label": "3",  "LT": 1, "RBI": 1, "D": 0, "C": 0, "B": 1, "A": 1, "expected": [1,0,0,1,1,1,1]},
    {"label": "4",  "LT": 1, "RBI": 1, "D": 0, "C": 1, "B": 0, "A": 0, "expected": [1,1,0,0,1,1,0]},
    {"label": "5",  "LT": 1, "RBI": 1, "D": 0, "C": 1, "B": 0, "A": 1, "expected": [1,1,0,1,1,0,1]},
    {"label": "6",  "LT": 1, "RBI": 1, "D": 0, "C": 1, "B": 1, "A": 0, "expected": [1,1,1,1,1,0,0]},
    {"label": "7",  "LT": 1, "RBI": 1, "D": 0, "C": 1, "B": 1, "A": 1, "expected": [0,0,0,0,1,1,1]},
    {"label": "8",  "LT": 1, "RBI": 1, "D": 1, "C": 0, "B": 0, "A": 0, "expected": [1,1,1,1,1,1,1]},
    {"label": "9",  "LT": 1, "RBI": 1, "D": 1, "C": 0, "B": 0, "A": 1, "expected": [1,1,0,0,1,1,1]},
    {"label": "10", "LT": 1, "RBI": 1, "D": 1, "C": 0, "B": 1, "A": 0, "expected": [1,0,1,1,0,0,0]},
    {"label": "11", "LT": 1, "RBI": 1, "D": 1, "C": 0, "B": 1, "A": 1, "expected": [1,0,0,1,1,0,0]},
    {"label": "12", "LT": 1, "RBI": 1, "D": 1, "C": 1, "B": 0, "A": 0, "expected": [1,1,0,0,0,1,0]},
    {"label": "13", "LT": 1, "RBI": 1, "D": 1, "C": 1, "B": 0, "A": 1, "expected": [1,1,0,1,0,0,1]},
    {"label": "14", "LT": 1, "RBI": 1, "D": 1, "C": 1, "B": 1, "A": 0, "expected": [1,1,1,1,0,0,0]},
    {"label": "15", "LT": 1, "RBI": 1, "D": 1, "C": 1, "B": 1, "A": 1, "expected": [0,0,0,0,0,0,0]},
    #special test cases
    {"label": "LT Test", "LT": 0, "RBI": 1, "D": 0, "C": 0, "B": 0, "A": 0, "expected": [1,1,1,1,1,1,1]},
    {"label": "RBI Test", "LT": 1, "RBI": 0, "D": 0, "C": 0, "B": 0, "A": 0, "expected": [0,0,0,0,0,0,0]}
]

# Function to write a digital output
def set_output(pin, value):
    ljm.eWriteName(handle, pins[pin], value)

def pulse_clk():
    set_output("CLK", 1)
    time.sleep(0.001)
    set_output("CLK", 0)
    time.sleep(0.001)

def load_parallel():
    set_output("PARALLEL_LOAD", 0)
    time.sleep(0.001)
    set_output("PARALLEL_LOAD", 1)
    time.sleep(0.001)

def shift_and_read():
    bits = []
    for _ in range(7):
        pulse_clk()
        val = ljm.eReadName(handle, pins["SER_IN"])
        valN = ljm.eReadName(handle, pins["SER_N_IN"]) # negativ output verify
        if round(val) > 4 and valN < 4:
            bits.append(1)
        else:
            bits.append(0)
    return bits

### Init, write empty output to shift register, otherwise first testcase will fail
for val in ["LT", "RBI", "D", "C", "B", "A"]: # set value outputs from truth_vector to outputs
        set_output(val, 0)
for _ in range(8):
    pulse_clk()
###

for vector in test_vectors:
    print(f"\nTesting: {vector['label']}")

    # Set control inputs
    for val in ["LT", "RBI", "D", "C", "B", "A"]: # set value outputs from truth_vector to outputs
        set_output(val, vector[val])

    load_parallel()
    result = shift_and_read()

    status = "PASS" if result == vector["expected"] else "FAIL"
    print(f"Expected: {vector['expected']}\nActual:   {result} → {status}")

# Close LabJack
ljm.close(handle)
