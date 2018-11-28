import time
import datetime
import threading
from get_net_info import RaspberryMonitorNetSpeed as rmn

import subprocess


#import Adafruit_Nokia_LCD as LCD
import Adafruit_SSD1306

import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi hardware SPI config:
#DC = 23
#RST = 24
#SPI_PORT = 0
#SPI_DEVICE = 0


# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


#disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=1000000))
#disp.begin(contrast=60)


# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()


#image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
#draw = ImageDraw.Draw(image)
#draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT),outline=255,fill=128)
#disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0







# # Clear display.
disp.clear()
disp.display()
IP = subprocess.check_output(["hostname", "-I"]).split()[0]
print ('Local IP :'+str(IP))
ns = [-1, -1]
#%%
def main():
    tmp = threading.Thread(target=network_speed)
    tmp.setDaemon(True)
    tmp.start()

    while True:
        try:
            disp.clear()
            disp.display()
            # Get drawing object to draw on image.
            draw = ImageDraw.Draw(image)
            #draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
            # Load default font.
		    draw.rectangle((0,0,width,height), outline=0, fill=0)
            font = ImageFont.truetype("DejaVuSansMono.ttf", 9)

            # Write some text.
			draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
            draw.text((x, top+8),     'U/S: ' + str(ns[1]), font=font, fill=255)
            draw.text((x, top+16),   'D/S: ' + str(ns[0]),  font=font, fill=255)
			draw.text((x, top+25),   str(CPU),,  font=font, fill=255)
            #draw.text((0,0), str(IP) , font=font)
            #draw.text((0,10), 'U/S: ' + str(ns[1]), font=font)
            #draw.text((0,20), 'D/S: ' + str(ns[0]), font=font)
            #draw.text((0,30), datetime.datetime.now().__str__()[5:].lstrip('0').split('.')[0], font=font)
            disp.image(image)
            disp.display()
            time.sleep(0.1)
        except KeyboardInterrupt:
            exit(0)

def network_speed():
    global ns
    b = rmn('admin', 'Sakuna0711')
    while True:
        time.sleep(1)
        ns = b.get_human_speed()


#%%
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
 
