
HOST = "172.20.10.242"
PORT = 4223

WIDTH = 296 # Columns
HEIGHT = 128 # Rows

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_e_paper_296x128 import BrickletEPaper296x128
from PIL import Image

# Convert PIL image to matching color bool list
def bool_list_from_pil_image(image, width=296, height=128, color=(0, 0, 0)):
    WIDTH = 296 # Columns
    HEIGHT = 128 # Rows
    image_data = image.load()
    pixels = []

    for row in range(height):
        for column in range(width):
            pixel = image_data[column, row]
            value = (pixel[0] == color[0]) and (pixel[1] == color[1]) and (pixel[2] == color[2])
            pixels.append(value)
    
    return pixels

def testEDisplay(ipcon):
    epaper = BrickletEPaper296x128("XGL", ipcon) # Create device object

    image = Image.open('~\source\troll.png')

    # Get black/white pixels from image and write them to the Bricklet buffer
    pixels_bw  = bool_list_from_pil_image(image, WIDTH, HEIGHT, (0xFF, 0xFF, 0xFF))
    epaper.write_black_white(0, 0, WIDTH-1, HEIGHT-1, pixels_bw)
