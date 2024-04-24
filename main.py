
HOST = "172.20.10.242"
PORT = 4223

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2
import mod_humidity as hum
import mod_temperature as temp
import mod_dualButton as dButton
import mod_rgbButton as rgbButton
import mod_segDisplay as segDisp
import sys
import bot


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

# Callback functino for temperature at humidity sensor (as in, internal)
def callback_humTemp(temperature):
    if Watching:
        callback_AlertTriggered()
    print("Internal Temperature above Threshold: " + str(temperature/100.0) + " °C")

# Callback function for temperature callback of external sensor (die Sonde)
def callback_temperature(temperature):
    if Watching:
        callback_AlertTriggered()
    print("External Temperature above Threshold: " + str(temperature/100.0) + " °C")

def callback_AlertTriggered():
    print("Alarm ausgelöst!")
    Watching = True


def callback_AlertEngaged():
    print("Alarm scharf")
    Alert = True
    

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection

    try:
        ipcon.connect(HOST, PORT)
    except:
        print("Unable to connect to Server.")
        sys.exit()

    #exec all our code in try catch, so con gets closed reliably
    try: # Connect to brickd
        # Don't use device before ipcon is connected

        temp.printTemperature(ipcon)
        hum.printHumidity(ipcon)

        print("Binding DualButton Bricklet")
        dButton.bind(ipcon, callback_DualButton)

        print("Binding Humidity Bricklet")
        hum.bind(ipcon, callback_humidity)
        hum.bindTemp(ipcon, callback_humTemp)

        print("Binding Temperature Bricklet")
        temp.bind(ipcon, callback_temperature)

        tempValue = temp.getTemperatureString(ipcon)+"°C"
        humValue = hum.getHumidityString(ipcon)+"%"

        bot.send_msg(str(tempValue))
        bot.send_msg(str(humValue))

    except Exception as e:
        print(repr(e))
    except: 
        print("Something went wrong.")
        

    input("Press key to exit\n") # Use raw_input() in Python 2

    try: 
        dButton.unbind(ipcon)
        hum.unbind(ipcon)
        temp.unbind(ipcon)
        
    except:
        print("Unable to reset. ")

    try:
        ipcon.disconnect()
        print("Disconnected.")
    except:
        print("Unable to disconnect. :(")
    


