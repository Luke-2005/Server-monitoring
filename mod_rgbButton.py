from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rgb_led_button import BrickletRGBLEDButton

# Callback function for button state changed callback
def cb_button_state_changed(state):
    if state == BrickletRGBLEDButton.BUTTON_STATE_PRESSED:
        print("State: Pressed")
    elif state == BrickletRGBLEDButton.BUTTON_STATE_RELEASED:
        print("State: Released")

def setBlue(ipcon):
    rlb = BrickletRGBLEDButton("XBe", ipcon)
    # rlb.reset
    # TODO crashed code pls fix

    # rlb.get_color()
    rlb.set_color(0, 170, 234)

    #print(rlb.get_color())
    #rlb.set_color("blue")
    print("Button set: blue")



#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
UID = "XBe" # Change XYZ to the UID of your RGB LED Button Bricklet
 
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rgb_led_button import BrickletRGBLEDButton
 
def setColor(ipcon):
    rlb = BrickletRGBLEDButton(UID, ipcon) # Create device object
    rlb.reset
    # Set light blue color
    rlb.set_color (200, 170, 200)
 
 
    input("Press key to exit\n") # Use raw_input() in Python 2