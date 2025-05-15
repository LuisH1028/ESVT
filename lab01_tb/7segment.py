from labjack import ljm
import time

# =========================
# CONFIGURATION SECTION
# =========================

# LabJack digital output and input channel mappings
#  TODO not correct ports
outputs = {
    'LT': "FIO0",
    'RBI': "FIO1",
    'D': "FIO2",
    'C': "FIO3",
    'B': "FIO4",
    'A': "FIO5",
    'BI_RBO': "FIO6"
}

inputs = {
    'a': "FIO7",
    'b': "FIO8",
    'c': "FIO9",
    'd': "FIO10",
    'e': "FIO11",
    'f': "FIO12",
    'g': "FIO13"
}

# Truth table for 7-segment display
test_vectors = [
    # LT RBI D C B A BI/RBO -> a b c d e f g   # Notes
    {'inputs': [1, 1, 0, 0, 0, 0, 1],
        'expected_outputs': [1, 1, 1, 1, 1, 1, 0]},  # 0
    {'inputs': [1, 1, 0, 0, 0, 1, 1],
        'expected_outputs': [0, 1, 1, 0, 0, 0, 0]},  # 1
    {'inputs': [1, 1, 0, 0, 1, 0, 1],
        'expected_outputs': [1, 1, 0, 1, 1, 0, 1]},  # 2
    {'inputs': [1, 1, 0, 0, 1, 1, 1],
        'expected_outputs': [1, 1, 1, 1, 0, 0, 1]},  # 3
    {'inputs': [1, 1, 0, 1, 0, 0, 1],
        'expected_outputs': [0, 1, 1, 0, 0, 1, 1]},  # 4
    {'inputs': [1, 1, 0, 1, 0, 1, 1],
        'expected_outputs': [1, 0, 1, 1, 0, 1, 1]},  # 5
    {'inputs': [1, 1, 0, 1, 1, 0, 1],
        'expected_outputs': [1, 0, 1, 1, 1, 1, 1]},  # 6
    {'inputs': [1, 1, 0, 1, 1, 1, 1],
        'expected_outputs': [1, 1, 1, 0, 0, 0, 0]},  # 7
    {'inputs': [1, 1, 1, 0, 0, 0, 1],
        'expected_outputs': [1, 1, 1, 1, 1, 1, 1]},  # 8
    {'inputs': [1, 1, 1, 0, 0, 1, 1],
        'expected_outputs': [1, 1, 1, 1, 0, 1, 1]},  # 9
    {'inputs': [1, 1, 1, 0, 1, 0, 1],
        'expected_outputs': [1, 1, 1, 0, 1, 1, 1]},  # 10
    {'inputs': [1, 1, 1, 0, 1, 1, 1],
        'expected_outputs': [0, 0, 1, 1, 1, 1, 1]},  # 11
    {'inputs': [1, 1, 1, 1, 0, 0, 1],
        'expected_outputs': [0, 0, 0, 1, 1, 1, 0]},  # 12
    {'inputs': [1, 1, 1, 1, 0, 1, 1],
        'expected_outputs': [0, 1, 1, 1, 1, 0, 1]},  # 13
    {'inputs': [1, 1, 1, 1, 1, 0, 1],
        'expected_outputs': [1, 0, 0, 1, 1, 1, 1]},  # 14
    {'inputs': [1, 1, 1, 1, 1, 1, 1],
        'expected_outputs': [1, 0, 0, 0, 0, 0, 0]},  # 15
    # Special function tests
    {'inputs': [0, 1, 0, 0, 0, 0, 1], 'expected_outputs': [
        0, 0, 0, 0, 0, 0, 0]},  # LT = 0, lamp test, note 4
    {'inputs': [1, 0, 0, 0, 0, 0, 1], 'expected_outputs': [
        1, 1, 1, 1, 1, 1, 1]},  # RBI = 0, note 3
    {'inputs': [1, 1, 0, 0, 0, 0, 0], 'expected_outputs': [
        0, 0, 0, 0, 0, 0, 0]},  # BI/RBO = 0, note 2
]

# =========================
# FUNCTION DEFINITIONS
# =========================


def write_outputs(handle, values):
    for i, key in enumerate(outputs.keys()):
        ljm.eWriteName(handle, outputs[key], values[i])


def read_inputs(handle):
    return [int(ljm.eReadName(handle, ch)) for ch in inputs.values()]


def run_test():
    handle = ljm.openS("T7", "ANY", "ANY")
    print("Connected to LabJack")

    try:
        for idx, vector in enumerate(test_vectors):
            print(f"\nTest case {idx+1}")

            # Write inputs
            write_outputs(handle, vector['inputs'])
            time.sleep(0.05)  # Allow signals to settle

            # Read outputs
            result = read_inputs(handle)
            print(f"Expected: {vector['expected_outputs']}, Read: {result}")

            if result == vector['expected_outputs']:
                print("PASS")
            else:
                print("FAIL")

        print("\nTest completed.")

    finally:
        ljm.close(handle)

# =========================
# MAIN SCRIPT
# =========================


if __name__ == "__main__":
    run_test()
