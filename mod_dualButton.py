from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2

def dbutton_bind(ipcon, nr, callback):
    db = BrickletDualButtonV2("23Qx", ipcon)

    db.register_callback(db.CALLBACK_STATE_CHANGED, callback)
    
    db.set_state_changed_callback_configuration(True)

    print("Bound Button to Function")