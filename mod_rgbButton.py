from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rgb_led_button import BrickletRGBLEDButton

# Callback function for button state changed callback
def cb_button_state_changed(ipcon):

    rlb = BrickletRGBLEDButton("23Qx", ipcon)
    state = rlb.get_button_state()

    if state == BrickletRGBLEDButton.BUTTON_STATE_PRESSED:
        return True
    elif state == BrickletRGBLEDButton.BUTTON_STATE_RELEASED:
        return False

def setGreen(ipcon):
    rlb = BrickletRGBLEDButton("23Qx", ipcon)
    rlb.set_color(0, 255, 0)

def setRed(ipcon):
    rlb = BrickletRGBLEDButton("23Qx", ipcon)
    rlb.set_color(255, 0, 0)

def setBlue(ipcon):
    rlb = BrickletRGBLEDButton("23Qx", ipcon)
    rlb.set_color(0, 0, 255)

def setOrange(ipcon):
    rlb = BrickletRGBLEDButton("23Qx", ipcon)
    rlb.set_color(255, 40, 0)