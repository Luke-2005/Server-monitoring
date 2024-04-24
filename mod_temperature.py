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

def bind(ipcon, function):
    ptc = BrickletPTCV2("Wcg", ipcon)
    ptc.register_callback(ptc.CALLBACK_TEMPERATURE, function)
    ptc.set_temperature_callback_configuration(10000, False, ">", 35 * 100, 500)

def unbind(ipcon):
    ptc = BrickletPTCV2("Wcg", ipcon)
    ptc.reset()
def getTemperatureString(ipcon):
    ptc = BrickletPTCV2("Wcg", ipcon) # Create device object
    tempValue = ptc.get_temperature()/100.0
    tempValue = str(tempValue)
    return tempValue