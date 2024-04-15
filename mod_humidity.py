from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2

def printHumidity(ipcon):
    h = BrickletHumidityV2("ViW", ipcon) # Create device object

    # Get current humidity
    humidity = h.get_humidity()
    print("Humidity: " + str(humidity/100.0) + " %RH")

def getHumidity(ipcon):
    h = BrickletHumidityV2("ViW", ipcon)
    return h.get_humidity()

#Bind function as Callback
def bind(ipcon, function):
    h = BrickletHumidityV2("ViW", ipcon)
    h.register_callback(h.CALLBACK_HUMIDITY, function)
    h.set_humidity_callback_configuration(60000, False, "o", 70*100, 100*100)
    
def unbind(ipcon):
    h = BrickletHumidityV2("ViW", ipcon)
    h.reset()