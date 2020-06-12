import os
from time import sleep

import pyufoled as mhl

results = mhl.LD686.scan(1)
for ip, message in results.items():
    print(f"{ip}: ({message})")

led = mhl.LD686("192.168.170.101")

led.rgb = (255, 10, 123)

sleep(1)

led.program = 1

led.program_speed = 5