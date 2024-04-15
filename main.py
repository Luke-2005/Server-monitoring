
HOST = "172.20.10.242"
PORT = 4223

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2
import mod_humidity as hum
import mod_temperature as temp
import mod_dualButton as dButton
import mod_rgbButton as rgbButton
import mod_segDisplay as segDisp

ipcon = ""

#Booleans
Watching = False #Alarm Scharf
Alert = False #Alarm Ausgelöst

def callback_DualButton(button_l, button_r, led_l, led_r):
    if button_l == BrickletDualButtonV2.BUTTON_STATE_PRESSED:
        print("Left Button: Pressed")

        #cycle T > H > C
        if segDisp.mode == "T":
            segDisp.mode = "H"
        elif segDisp.mode == "H":
            segDisp.mode = "C"
        else:
            segDisp.mode = "T"

        print("Cycled to '" + segDisp.mode + "'. Updating")
        if ipcon != "":
            segDisp.UpdateDisplay(ipcon, False)
    elif button_l == BrickletDualButtonV2.BUTTON_STATE_RELEASED:
        print("Left Button: Released")

    if button_r == BrickletDualButtonV2.BUTTON_STATE_PRESSED:
        print("Right Button: Pressed")

        #cycle C > H > T
        if segDisp.mode == "C":
            segDisp.mode = "H"
        elif segDisp.mode == "H":
            segDisp.mode = "T"
        else:
            segDisp.mode = "C"

        print("Cycled to '" + segDisp.mode + "'. Updating")
        if ipcon != "":
            segDisp.UpdateDisplay(ipcon, False)
    elif button_r == BrickletDualButtonV2.BUTTON_STATE_RELEASED:
        print("Right Button: Released")

# Callback function for humidity callback
def callback_humidity(humidity):
    if Watching:
        callback_AlertTriggered()
    print("Humidity above Threshold: " + str(humidity/100.0) + " %RH")

# Callback function for temperature callback
def callback_temperature(temperature):
    if Watching:
        callback_AlertTriggered()
    print("Temperature above Threshold: " + str(temperature/100.0) + " °C")

def callback_AlertTriggered():
    print("Alarm ausgelöst!")
    Watching = True


def callback_AlertEngaged():
    print("Alarm scharf")
    Alert = True
    

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection


    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
    
    #exec all our code in try catch, so con gets closed reliably
    try:

        temp.printTemperature(ipcon)
        hum.printHumidity(ipcon)
        dButton.bind(ipcon, callback_DualButton)
        hum.bind(ipcon, callback_humidity)
        temp.bind(ipcon, callback_temperature)

    except Exception as e:
        print(repr(e))
    except: 
        print("Something went wrong.")
        

    input("Press key to exit\n") # Use raw_input() in Python 2

    dButton.unbind(ipcon)
    hum.unbind(ipcon)
    temp.unbind(ipcon)
    
    ipcon.disconnect()
    


