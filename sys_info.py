#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display basic system information.

Needs psutil (+ dependencies) installed::

  $ sudo apt-get install python-dev
  $ sudo -H pip install psutil
"""
#%%
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
#import threading
#from get_net_info import RaspberryMonitorNetSpeed as rmn
# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
#serial = i2c(port=1, address=0x3C)
serial = spi(device=0, port=0)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = sh1106(serial)

import subprocess
from PIL import ImageFont
import os
import sys
import time


if os.name != 'posix':
    sys.exit('{} platform not supported'.format(os.name))



font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'C&C Red Alert [INET].ttf'))

font2 = ImageFont.truetype(font_path, 12)

def stats(device):
    
 with canvas(device) as draw:
    IP = subprocess.check_output(["hostname", "-I"]).split()[0]
   # print ('Local IP :'+str(IP))
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    draw.text((0, 0), str(CPU), font=font2, fill="white")
    draw.text((0, 14),"IP : " + str(IP), font=font2, fill="white")
    draw.text((0, 26), str(MemUsage), font=font2, fill="white")
    draw.text((0, 38), str(Disk), font=font2, fill="white")
  #draw.text((0, 0), cpu_usage(), font=font2, fill="white")
  #draw.text((0, 14), mem_usage(), font=font2, fill="white")
  #draw.text((0, 26), disk_usage('/'), font=font2, fill="white")
  #draw.text((0, 38), "IP:" + get_ip_address('wlan0'), font=font2, fill="white")
  #draw.text((0, 50), network('wlan0'), font=font2, fill="white")
#    except KeyError:
                # no wifi enabled/available
pass

#%%

def main():
    while True:
        stats(device)
        time.sleep(5)


if __name__ == "__main__":
    try:
        device = sh1106(serial)
        main()
    except KeyboardInterrupt:
        pass
