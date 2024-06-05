
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2

def bind(ipcon, callback):
    md = BrickletMotionDetectorV2("ML4", ipcon) # Create device object

    # Register motion detected callback to function callback
    md.register_callback(md.CALLBACK_MOTION_DETECTED, callback)
