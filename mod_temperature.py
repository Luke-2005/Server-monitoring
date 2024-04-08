from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2

def printTemperature(ipcon):
    ptc = BrickletPTCV2("Wcg", ipcon) # Create device object

    # Get current temperature
    temperature = ptc.get_temperature()
    print("Temperature: " + str(temperature/100.0) + " °C")

def getTemperature(ipcon):
    ptc = BrickletPTCV2("Wcg", ipcon) # Create device object
    return ptc.get_temperature()