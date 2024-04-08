from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2
import datetime

def setTime(ipcon):
    sd = BrickletSegmentDisplay4x7V2("Tre", ipcon) 
    now = datetime.datetime.now()
    strnow = str(now.time())

    print("set SegmentDisplay to " + strnow)

    sd.set_brightness(7)
    sd.set_numeric_value([int(strnow[0]), int(strnow[1]), int(strnow[3]), int(strnow[4])])
    sd.set_selected_segment(32, True)
    sd.set_selected_segment(33, True)
    

    input("Continue?")


    sd.reset()