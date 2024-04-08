from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2
import datetime, sched, time

s = sched.scheduler(time.time, time.sleep)

def setTime(ipcon, repeat):
    sd = BrickletSegmentDisplay4x7V2("Tre", ipcon) 
    now = datetime.datetime.now()

    try:
        strnow = str(now.time())

        print("set SegmentDisplay to " + strnow)

        sd.set_brightness(7)
        sd.set_numeric_value([int(strnow[0]), int(strnow[1]), int(strnow[3]), int(strnow[4])])
        sd.set_selected_segment(32, True)
        sd.set_selected_segment(33, True)
        
        if repeat:
            #Do some black magic to adjust for drift - we want to update once a minute, about 
            #a second after the minute changed...
            now = time.time()
            seconds = 60 - int(now % 60)
            print ("Rescheduled in " + now + " Seconds")
            s.enter(seconds + 1, 1, setTime(ipcon, True), (s, ))
        else:
            input("Continue?")

    except Exception as e:
        print(repr(e))
    except: 
        print("Something went wrong.")
    sd.reset()

def setTimeScheduled(ipcon):
    s.enter(60, 1, setTime(ipcon, True), (s, ))
    s.run()
    
