
import time
import datetime
import threading
from get_net_info import RaspberryMonitorNetSpeed as rmn

import subprocess

import Adafruit_SSD1306

import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

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
x = 2
font = ImageFont.load_default()

IP = subprocess.check_output(["hostname", "-I"]).split()[0]
print ('Local IP :'+str(IP))
ns = [-1, -1]

def network_speed():
    global ns
    b = rmn('admin', 'Sakuna0711')
    while True:
        time.sleep(1)
        ns = b.get_human_speed()
#%%
def main():
    tmp = threading.Thread(target=network_speed)
    tmp.setDaemon(True)
    tmp.start()


    while True:
        try:
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell = True )
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell = True )
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )
            # Write some text.
            draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
            draw.text((x, top+8),     'U/S: ' + str(ns[1]), font=font, fill=255)
            draw.text((x, top+16),   'D/S: ' + str(ns[0]),  font=font, fill=255)
            draw.text((x, top+25),   str(CPU),  font=font, fill=255)
            draw.text((x, top+33), str(MemUsage),  font=font, fill=255)
            draw.text((x, top+41), str(Disk),  font=font, fill=255)
            disp.image(image)
            disp.display()

            time.sleep(1)
        except KeyboardInterrupt:
            exit(0)


#%%
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
 
