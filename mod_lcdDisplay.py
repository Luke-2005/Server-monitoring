
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_lcd_128x64 import BrickletLCD128x64
import datetime, sched, time

s = sched.scheduler(time.time, time.sleep)

Temperatures = [0];
Humidities = [0];

def setGraphs(ipcon):
    lcd = BrickletLCD128x64("25Rh", ipcon) # Create device object
    
    print("Clearing Display")
    lcd.clear_display()

    print("Setting Graphs")
    #Temp
    lcd.set_gui_graph_configuration(0, BrickletLCD128x64.GRAPH_TYPE_LINE, 0, 0, 128, 16, "Time", "Case Temp");
    #Hum
    lcd.set_gui_graph_configuration(1, BrickletLCD128x64.GRAPH_TYPE_LINE, 0, 16, 128, 16, "Time", "Hum");

def updateDisplay(ipcon, repeat, Temp, Hum):
    lcd = BrickletLCD128x64("25Rh", ipcon) # Create device object
    
    print("Updating Graphs")

    if Temperatures.count() >= 100:
        Temperatures.pop(0);
    if Humidities.count() >= 100:
        Humidities.pop(0)
    Temperatures.append(Temp(ipcon))
    Humidities.append(Hum(ipcon))

    #Temp
    lcd.set_gui_graph_data(0, Temperatures)
    #Hum
    lcd.set_gui_graph_data(1, Humidities)
    if repeat:
        now = time.time()
        seconds = 5 - int(now % 5)
        print ("Rescheduled in " + now + " Seconds")
        s.enter(seconds + 1, 1, UpdateDisplay(ipcon, True, Temp, Hum), (s, ))

def unbind(ipcon):
    lcd = BrickletLCD128x64("25Rh", ipcon) # Create device object
    lcd.reset()