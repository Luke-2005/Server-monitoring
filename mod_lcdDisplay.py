
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_lcd_128x64 import BrickletLCD128x64
import datetime, sched, time
import threading

s = sched.scheduler(time.time, time.sleep)

Temperatures = [0, 0]
Humidities = [0, 0]
Alarms = ["", "", "", "", ""]
CurrentDisp = 0
ipconG = 0

def cb_gui_tab_selected(index):
    print("LCD: Tab change to Index: " + str(index))
    CurrentDisp = index
    if(ipconG != 0):
        updateDisplay(ipconG)
    else:
        print("LCD: Callback has no Connection Variable? Thread is " + str(threading.current_thread().ident))

def cb_touch_gesture(gesture, duration, pressure_max, x_start, x_end, y_start, y_end, age):
    print("LCD: Touch Input received")
    if gesture == BrickletLCD128x64.GESTURE_LEFT_TO_RIGHT | gesture == GESTURE_RIGHT_TO_LEFT:
        if CurrentDisp == 1:
            CurrentDisp = 0
            print("LCD: Swipe: 0")
            #setGraphs(ipcon)
        elif CurrentDisp == 0:
            CurrentDisp = 1
            print("LCD: Swipe: 1")
            #setList(ipcon)
        #updateDisplay(ipcon, False)
    elif gesture == BrickletLCD128x64.GESTURE_TOP_TO_BOTTOM:
        print("LCD: Top To Bottom")
    elif gesture == BrickletLCD128x64.GESTURE_BOTTOM_TO_TOP:
        print("LCD: Bottom To Top")
    

def bind(ipcon):
    lcd = BrickletLCD128x64("24Rh", ipcon) # Create device object

    #reset everything
    lcd.reset()
    lcd.clear_display()
    lcd.remove_all_gui()

    #Set period for GUI tab selected callback to 0.1s (100ms)
    lcd.set_gui_tab_selected_callback_configuration(100, True)
    lcd.set_touch_gesture_callback_configuration(100, True)

    #These should give me callbacks, but apparently doesn't
    #lcd.set_gui_tab_configuration(lcd.CHANGE_TAB_ON_CLICK_AND_SWIPE, True)
    #lcd.register_callback(lcd.CALLBACK_TOUCH_GESTURE, cb_touch_gesture)
    #lcd.register_callback(lcd.CALLBACK_GUI_TAB_SELECTED, cb_gui_tab_selected)

    #Add Tabs. Switching works without callbacks, apparently
    lcd.set_gui_tab_text(0, "Env")
    #lcd.set_gui_tab_text(1, "Alert")
    setGraphs(ipcon, lcd)

    #dirty hacks
    #ipconG = ipcon
    #print("LCD: Set ipcon holding variable in Thread " + str(threading.current_thread().ident))


def setGraphs(ipcon, lcd):

    print("LCD: Setting Graphs")
    #Temp
    lcd.set_gui_graph_configuration(0, BrickletLCD128x64.GRAPH_TYPE_LINE, 0, 0, 128, 16, "", "C°");
    #Hum
    lcd.set_gui_graph_configuration(1, BrickletLCD128x64.GRAPH_TYPE_LINE, 0, 16, 128, 16, "", "H%");

def addAlarm(Alarm):
    if len(Alarms) >= 5:
        Alarms.pop(0)
    Alarms.append(Alarm)

def updateLists(ipcon, Temp, Hum):
    print("LCD: Updating Value Lists")
    try:
        if len(Temperatures) >= 100:
            Temperatures.pop(0)
        if len(Humidities) >= 100:
            Humidities.pop(0)
        Temperatures.append(round(Temp(ipcon)))
        Humidities.append(round(Hum(ipcon)))

        print(Temperatures)
        print(Humidities)
    except:
        print("LCD: Failed updating values.")
        return

def updateDisplay(ipcon):
    lcd = BrickletLCD128x64("24Rh", ipcon) # Create device object
    try:            
        if CurrentDisp == 0:
            print("LCD: Updating Graphs")
            setGraphs(ipcon, lcd)
        elif CurrentDisp == 1:
            print("LCD: Updating Alarm List.")
            index = 0
            for al in Alarms:
                lcd.draw_text(1, index * 8, lcd.FONT_6X8, lcd.COLOR_BLACK, al)
                index += 1

        #Temp
        lcd.set_gui_graph_data(0, Temperatures)
        #Hum
        lcd.set_gui_graph_data(1, Humidities)
    except:
        print("LCD: updateDisplay Failed.")
        return

def repeatUpdate(ipcon, Temp, Hum):
    #print("LCD: Thread ident:" + str(threading.current_thread().ident))
    while True:
        try:
            if (ipcon.get_connection_state() != ipcon.CONNECTION_STATE_CONNECTED):
                print("LCD: Connection dead. Exiting Async Loop")
                return
            updateLists(ipcon, Temp, Hum)
            updateDisplay(ipcon)
            now = time.time()
            seconds = 30 - int(now % 30)
            print ("LCD: Rescheduled in " + str(seconds) + " Seconds")
            time.sleep(seconds)
            #s.enter(seconds + 1, 1, updateDisplay, (ipcon, True, Temp, Hum))
            #s.run()
        except:
            print("LCD: repeat updateDisplay Failed.")
            return

def unbind(ipcon):
    lcd = BrickletLCD128x64("24Rh", ipcon) # Create device object
    lcd.reset()