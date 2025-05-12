# Testing Digital Circuit with 7Segment Decoder and Bitshifting Register
# Authors: Chris Hölzle, Luis Huber
# Date: 09.05.2025


import labjack

from labjack import ljm

handle = ljm.openS("ANY","ANY","ANY")

# Set default Output to LOW
ljm.eWriteName(handle, "FIO0", 0)
ljm.eWriteName(handle, "FIO1", 0)
ljm.eWriteName(handle,"DAC0",0)
ljm.eWriteName(handle,"DAC1",0)

# Vcc of both ICs is nom. 5V (datasheet)
ljm.eWriteName(handle, "DAC0",5)

# Clock-Signal out of DAC1 with 3V



inp = ['A', 'B', 'C','D', 'LT', 'BI')

for i in inp:
    


