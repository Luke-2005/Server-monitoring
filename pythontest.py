
HOST = "172.20.10.242"
PORT = 4223

WIDTH = 296 # Columns
HEIGHT = 128 # Rows

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light_v3 import BrickletAmbientLightV3
from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2
from tinkerforge.bricklet_e_paper_296x128 import BrickletEPaper296x128
from PIL import Image

# Convert PIL image to matching color bool list
def bool_list_from_pil_image(image, width=296, height=128, color=(0, 0, 0)):
    image_data = image.load()
    pixels = []

    for row in range(height):
        for column in range(width):
            pixel = image_data[column, row]
            value = (pixel[0] == color[0]) and (pixel[1] == color[1]) and (pixel[2] == color[2])
            pixels.append(value)
    
    return pixels
# Callback function for illuminance callback
def cb_illuminance(illuminance):
    print("Illuminance: " + str(illuminance/100.0) + " lx")
    print("Too bright, close the curtains!")

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    al = BrickletAmbientLightV3("Pdw", ipcon) # Create device object
    ptc = BrickletPTCV2("Wcg", ipcon) # Create device object
    h = BrickletHumidityV2("ViW", ipcon) # Create device object
    epaper = BrickletEPaper296x128("XGL", ipcon) # Create device object


    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected



    # Download example image here:
    # https://raw.githubusercontent.com/Tinkerforge/e-paper-296x128-bricklet/master/software/examples/tf_red.png
    image = Image.open('~\source\troll.png')

    # Get black/white pixels from image and write them to the Bricklet buffer
    pixels_bw  = bool_list_from_pil_image(image, WIDTH, HEIGHT, (0xFF, 0xFF, 0xFF))
    epaper.write_black_white(0, 0, WIDTH-1, HEIGHT-1, pixels_bw)


    # Get current temperature
    temperature = ptc.get_temperature()
    print("Temperature: " + str(temperature/100.0) + " °C")


    # Get current humidity
    humidity = h.get_humidity()
    print("Humidity: " + str(humidity/100.0) + " %RH")


    # Register illuminance callback to function cb_illuminance
    al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)

    # Configure threshold for illuminance "greater than 500 lx"
    # with a debounce period of 1s (1000ms)
    al.set_illuminance_callback_configuration(1000, False, ">", 20*100, 0)



    input("Press key to exit\n") # Use raw_input() in Python 2

    ipcon.disconnect()

