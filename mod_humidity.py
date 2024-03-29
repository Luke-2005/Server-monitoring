from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2

def printHumidity(ipcon):
    h = BrickletHumidityV2("ViW", ipcon) # Create device object

    # Get current humidity
    humidity = h.get_humidity()
    print("Humidity: " + str(humidity/100.0) + " %RH")



