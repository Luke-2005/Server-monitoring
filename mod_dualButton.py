from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2

def bind(ipcon, callback):
    db = BrickletDualButtonV2("Vd8", ipcon)

    db.register_callback(db.CALLBACK_STATE_CHANGED, callback)
    
    db.set_state_changed_callback_configuration(True)

    print("Bound Button to Function")

def unbind(ipcon):
    db = BrickletDualButtonV2("Vd8", ipcon)
    db.reset()