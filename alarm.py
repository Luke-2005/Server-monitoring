from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2



def playAlarm(ipcon):
        ps = BrickletPiezoSpeakerV2("R7M", ipcon)

        ps.set_alarm(800, 2000, 10, 1, 3, 600000)

        input("Press key to exit\n")

def stopAlarm(ipcon):
        ps = BrickletPiezoSpeakerV2("R7M", ipcon)

        ps.set_alarm(800, 2000, 10, 1, 3, 0)

        input("Press key to exit\n")
