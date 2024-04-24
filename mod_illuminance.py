
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light_v3 import BrickletAmbientLightV3

# Callback function for illuminance callback
def cb_illuminance(illuminance):
    print("Illuminance: " + str(illuminance/100.0) + " lx")
    print("Too bright, close the curtains!")


def monitorIlluminance(ipcon, threshold):
    al = BrickletAmbientLightV3("Pdw", ipcon) # Create device object

    # Register illuminance callback to function cb_illuminance
    al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)

    # Configure threshold for illuminance "greater than 500 lx"
    # with a debounce period of 1s (1000ms)
    al.set_illuminance_callback_configuration(1000, False, ">", threshold, 0)

def getIlluminance(ipcon):
    al = BrickletAmbientLightV3("Pdw", ipcon)
    return al.get_illuminance()