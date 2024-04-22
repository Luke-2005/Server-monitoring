from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2
import datetime, sched, time
import mod_humidity as hum
import mod_temperature as temp

s = sched.scheduler(time.time, time.sleep)
mode = "T"; # T for Time, H for humidity, C for Temp
brightness = 7

def setTime(ipcon):
    sd = BrickletSegmentDisplay4x7V2("Tre", ipcon) 
    now = datetime.datetime.now()

    try:
        strnow = str(now.time())

        print("set SegmentDisplay to " + strnow)

        sd.set_brightness(brightness)
        sd.set_numeric_value([int(strnow[0]), int(strnow[1]), int(strnow[3]), int(strnow[4])])
        sd.set_selected_segment(32, True)
        sd.set_selected_segment(33, True)
        
    except Exception as e:
        print(repr(e))
    except: 
        print("Something went wrong.")

def setHumidity(ipcon):
    sd = BrickletSegmentDisplay4x7V2("Tre", ipcon) 

    try:
        strnow = str(hum.getHumidity(ipcon))

        #print("Hum Vals")
        #print(strnow[0])
        #print(strnow[1])
        #print(strnow[2])
        #print(strnow[3])
        sd.set_brightness(brightness)
        sd.set_numeric_value([int(strnow[0]), int(strnow[1]), int(strnow[2]), int(strnow[3])])
        sd.set_selected_segment(32, False)
        sd.set_selected_segment(33, True)
        
    except Exception as e:
        print(repr(e))
    except: 
        print("Something went wrong.")
    sd.reset()

def setTemperature(ipcon):
    sd = BrickletSegmentDisplay4x7V2("Tre", ipcon) 

    try:
        strnow = str(temp.getTemperature(ipcon))

        #print("Temp Vals")
        #print(strnow[0])
        #print(strnow[1])
        #print(strnow[2])
        #print(strnow[3])
        sd.set_brightness(brightness)
        sd.set_numeric_value([int(strnow[0]), int(strnow[1]), int(strnow[2]), int(strnow[3])])
        sd.set_selected_segment(32, False)
        sd.set_selected_segment(33, True)
        
    except Exception as e:
        print(repr(e))
    except: 
        print("Something went wrong.")
    sd.reset()

def UpdateDisplay(ipcon, repeat):
    if mode == "T":
        setTime(ipcon)
    elif mode == "H":
        setHumidity(ipcon)
    elif mode == "C":
        setTemperature(ipcon)
    
    if repeat:
        #Do some black magic to adjust for drift - we want to update once a minute, about 
        #a second after the minute changed...
        now = time.time()
        seconds = 60 - int(now % 60)
        print ("Rescheduled in " + now + " Seconds")
        s.enter(seconds + 1, 1, UpdateDisplay(ipcon, True), (s, ))

def scheduleUpdates(ipcon):
    s.enter(60, 1, UpdateDisplay(ipcon, True), (s, ))
    s.run()
    
