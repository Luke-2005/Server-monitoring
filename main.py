
HOST = "172.20.10.242"
PORT = 4223

from tinkerforge.ip_connection import IPConnection
import mod_humidity as hum
import mod_temperature as temp
import mod_dualButton as dButton
import mod_rgbButton as rgbButton
import mod_segDisplay as segDisp

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection


    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
    
    #exec all our code in try catch, so con gets closed reliably
    try:

        temp.printTemperature(ipcon)

        
        hum.printHumidity(ipcon)

        segDisp.setHumidity(ipcon)
        segDisp.setTemperature(ipcon)



    except Exception as e:
        print(repr(e))
    except: 
        print("Something went wrong.")
        

    input("Press key to exit\n") # Use raw_input() in Python 2

    ipcon.disconnect()

