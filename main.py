
HOST = "172.20.10.242"
PORT = 4223

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2
import mod_humidity as hum
import mod_temperature as temp
import mod_dualButton as dButton
import mod_rgbButton as rgbButton
import mod_segDisplay as segDisp
import mod_lcdDisplay as lcdDisp
import mod_motion as motion
import sys
import bot
import alarm
import threading
import datetime
import time


ipcon = ""
lcdDispTask1 = 0
segDispTask = 0

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
            segDisp.updateDisplay(ipcon, False)
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
            segDisp.updateDisplay(ipcon, False)
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

def callback_motion():
    print("Motion Detected.")
    # if(Watching and time(17,00) < time.time() < time(7,00)): <-- auskommentiert zum testen innerhalb der Schulzeiten
    if(True):
        callback_AlertTriggered()

def callback_AlertTriggered():
    print("Alarm ausgelöst!")
    bot.send_msg('Server Alarm triggered!!!')
    Alert = True
    alarm.playAlarm(ipcon)
    callback_rgbButton(ipcon)

def callback_AlertEngaged():
    print("Alarm scharf")
    Watching = True

def callback_rgbButton(ipcon):
    global Alert
    print(datetime.datetime.now().hour)
    hour = datetime.datetime.now().hour

    # When the Alert is active, waiting for a button press
    if(Alert):
        print('RGB-Button set: red')
        rgbButton.setRed(ipcon)

        while(True):
            if(rgbButton.cb_button_state_changed(ipcon)):
                print('RGB-Button set: orange')
                Alert = False
                alarm.stopAlarm(ipcon)
                rgbButton.setOrange(ipcon)
                time.sleep(2.5)
                callback_rgbButton(ipcon)
                break
    # When between 7 & 17 Uhr Alert System active
    elif(17 <= hour <= 7):
        print('RGB-Button set: blue')
        rgbButton.setBlue(ipcon)
        callback_AlertEngaged
    else:
        print('RGB-Button set: green')
        rgbButton.setGreen(ipcon)


if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection

    try:
        ipcon.connect(HOST, PORT)
    except:
        print("Unable to connect to Server.")
        sys.exit()

    #exec all our code in try catch, so con gets closed reliably
    try:
        print("Main Thread ident is " + str(threading.current_thread().ident))
        temp.printTemperature(ipcon)
        hum.printHumidity(ipcon)

        print("Binding SegDisplay")
        segDispTask = threading.Thread(target = segDisp.updateDisplay, args=(ipcon, True))

        print("Binding Display")
        lcdDisp.ipconG = ipcon
        lcdDisp.bind(ipcon)
        print("Creating Display Update Threads")

        ipconSec = IPConnection() # Create secondary IP connection for threads
        try:
            ipconSec.connect(HOST, PORT)
        except:
            print("Unable to connect secondary connection to Server.")
        lcdDispTask = threading.Thread(target = lcdDisp.repeatUpdate, args=(ipconSec, temp.getTemperature, hum.getHumidity)) 

        try:
            print("Starting continuous Update Threads")
            lcdDispTask.start()
            segDispTask.start()
            print("Done.")
        except:
            print("Unable to start Threads")

        print("Binding DualButton Bricklet")
        dButton.bind(ipcon, callback_DualButton)

        print("Binding Motion Detector Bricklet")
        motion.bind(ipcon, callback_motion)

        print("Binding Humidity Bricklet")
        hum.bind(ipcon, callback_humidity)
        hum.bindTemp(ipcon, callback_humTemp)

        print("Binding Temperature Bricklet")
        temp.bind(ipcon, callback_temperature)

        tempValue = temp.getTemperatureString(ipcon)+"°C"
        humValue = hum.getHumidityString(ipcon)+"%"
        
        bot.send_msg(str(tempValue))
        bot.send_msg(str(humValue))

        callback_rgbButton(ipcon)


        input("Press key to exit\n") # Use raw_input() in Python 2

    except Exception as e:
        print(repr(e))
    except: 
        print("Something went wrong.")
    finally:
        try:
            lcdDispTask1.stop()
            segDispTask.stop()
            print("Repeated Tasks aborted. ")
        except:
            print("Unable to stop Task(s). ")

        try: 
            dButton.unbind(ipcon)
            hum.unbind(ipcon)
            temp.unbind(ipcon)
            lcdDisp.unbind(ipcon)
            print("Unbound.")
        except:
            print("Unable to reset. ")

        try:
            ipcon.disconnect()
            ipconSec.disconnect()
            print("Disconnected.")
        except:
            print("Unable to disconnect. :(")

        


    
