
HOST = "172.20.10.242"
PORT = 4223

from tinkerforge.ip_connection import IPConnection
import mod_humidity as hum
import mod_temperature as temp

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection


    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    temp.printTemperatur(ipcon)

    hum.printHumidity(ipcon)

    input("Press key to exit\n") # Use raw_input() in Python 2

    ipcon.disconnect()

