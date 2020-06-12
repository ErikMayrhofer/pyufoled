import os
from time import sleep

import pyufoled as mhl

#results = mhl.LD686.scan(1)
#for ip, message in results.items():
#    print(f"{ip}: ({message})")

led = mhl.LD686("192.168.170.102")
led.on = True

for i in range(255):
    hsv = (i/255, 1, 1)
    led.hsv = hsv
    print(f"{hsv} -> {led.hsv}")