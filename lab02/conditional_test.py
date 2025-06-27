# -*- coding: utf-8 -*-
"""
Created on Fri May 30 12:17:40 2025

@author: Torben Burandt, Jannis Rohleder
"""

import numpy as np
import matplotlib.pyplot as plt
from labjack import ljm
from scipy import stats
import time

# Open LabJack T7 connection
handle = ljm.openS("ANY", "ANY", "ANY")

# Configuration
stim_channels = ["DAC0", "DAC1"]
response_channels = ["AIN2", "AIN3"]
v_min = 0.8 # begin at diode forward voltage, otherwise errors in linear regressoion near zero
v_max = 4.7 # prevent supply voltage clipping, 4.7 last value that can be inerpreted as "correct", beyond that op clipped
v_step = 0.1






# Build stimulus array
stimuli = np.arange(v_min, v_max + v_step, v_step)

# Prepare data storage
data = {}

for stim_ch, resp_ch in zip(stim_channels, response_channels):
    print(f"Testing: Stim {stim_ch} -> Resp {resp_ch}")

    response = []
    
    for v in stimuli:
        # Set DAC output
        ljm.eWriteName(handle, stim_ch, v)
        print(f"applying {v}")
        # Small delay if necessary (LabJack settles quickly, but for safety)
        time.sleep(0.1)  # ms

        # Read ADC input
        val = ljm.eReadName(handle, resp_ch)
        response.append(val)
        print(f"reading {val}")
    response = np.array(response)
    data[stim_ch] = {
        "stimuli": stimuli,
        "response": response
    }

    # Linear fit
    gain, intercept, r_value, p_value, std_err = stats.linregress(stimuli, response)
    fit_line = gain * stimuli + intercept
    deviation = response - fit_line
    inl = np.max(np.abs(deviation))

    print(f"\n{stim_ch} to {resp_ch} Results:")
    print(f"  Gain: {gain:.4f}")
    print(f"  Offset: {intercept:.4f} V")
    print(f"  Max Integral Nonlinearity (INL): {inl:.4f} V\n")

    # Plotting
    plt.figure()
    plt.plot(stimuli, response, 'o', label='Measured')
    plt.plot(stimuli, fit_line, '-', label=f'Linear Fit (Gain={gain:.3f}, Offset={intercept:.3f})')
    plt.title(f'Characteristic: {stim_ch} to {resp_ch}')
    plt.xlabel('Stimulus Voltage (V)')
    plt.ylabel('Response Voltage (V)')
    plt.grid(True)
    plt.legend()
    plt.show()

# Close connection
ljm.close(handle)
