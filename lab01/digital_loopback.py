import labjack

from labjack import ljm

handle = ljm.openS("ANY","ANY","ANY")

ljm.eWriteName(handle, "FIO0", 0) # Digital output of a “0” to FIO0
ljm.eWriteName(handle, "FIO1", 0) # Digital output of a “0” to FIO1

# FIO0 connected to FIO3 / FIO1 connected to FIO2

result = ljm.eReadName(handle, "FIO3")  # Read digital input of FIO3
print(result)


result = ljm.eReadName(handle, "FIO2")  # Read digital input of FIO2
print(result)

ljm.eWriteName(handle, "FIO0", 1) # Digital output of a “1” to FIO0
ljm.eWriteName(handle, "FIO1", 1) # Digital output of a “1” to FIO1

result = ljm.eReadName(handle, "FIO3")  # Read digital input of FIO3
print(result)


result = ljm.eReadName(handle, "FIO2")  # Read digital input of FIO2
print(result)

