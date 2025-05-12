# Testing NAND-Gate

import labjack

from labjack import ljm

handle = ljm.openS("ANY","ANY","ANY")

# Set default Output to LOW
ljm.eWriteName(handle, "FIO0", 0)
ljm.eWriteName(handle, "FIO1", 0)
ljm.eWriteName(handle,"DAC0",0)

ljm.eWriteName(handle,"DAC0",3.3)           # setting DAC0 as Vcc for NAND-Gate

# Testcase 1: LOW, LOW
ljm.eWriteName(handle, "FIO0", 0)
ljm.eWriteName(handle, "FIO1", 0)

result1 = ljm.eReadName(handle, "AIN0")     # Read analog input for AIN0 as NAND output
print("Testcase 1: LOW, LOW\n OUTPUT: ",result1)

# Testcase 1: HIGH, LOW
ljm.eWriteName(handle, "FIO0", 1)
ljm.eWriteName(handle, "FIO1", 0)

result1 = ljm.eReadName(handle, "AIN0")     # Read analog input for AIN0 as NAND output
print("Testcase 1: HIGH, LOW\n OUTPUT: ",result1)

# Testcase 1: LOW, HIGH
ljm.eWriteName(handle, "FIO0", 0)
ljm.eWriteName(handle, "FIO1", 1)

result1 = ljm.eReadName(handle, "AIN0")     # Read analog input for AIN0 as NAND output
print("Testcase 1: LOW, HIGH\n OUTPUT: ",result1)

# Testcase 4: HIGH, HIGH
ljm.eWriteName(handle, "FIO0", 1)
ljm.eWriteName(handle, "FIO1", 1)

result1 = ljm.eReadName(handle, "AIN0")     # Read analog input for AIN0 as NAND output
print("Testcase 4: HIGH, HIGH\n OUTPUT: ",result1)



# Set default Output to LOW
ljm.eWriteName(handle, "FIO0", 0)
ljm.eWriteName(handle, "FIO1", 0)
ljm.eWriteName(handle,"DAC0",0)



ljm.close(handle)

