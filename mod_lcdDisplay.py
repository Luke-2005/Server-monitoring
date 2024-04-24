
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_lcd_128x64 import BrickletLCD128x64

Temperatures = [0];
Humidities = [0];

def setGraphs(ipcon):
    lcd = BrickletLCD128x64("25Rh", ipcon) # Create device object
    #Temp
    lcd.set_gui_graph_configuration(0, BrickletLCD128x64.GRAPH_TYPE_LINE, 0, 0, 128, 16, "Time", "Case Temp");
    #Hum
    lcd.set_gui_graph_configuration(1, BrickletLCD128x64.GRAPH_TYPE_LINE, 0, 16, 128, 16, "Time", "Hum");

def updateDisplay(ipcon):
    lcd = BrickletLCD128x64("25Rh", ipcon) # Create device object
    #Temp
    lcd.set_gui_graph_data(0, Temperatures)
    #Hum
    lcd.set_gui_graph_data(1, Humidities)
