import os
from time import sleep
print(os.getcwd())

import pyufoled as mhl


results = mhl.LD686.scan(1)
for ip, message in results.items():
    print(f"{ip}: ({message})")


led = mhl.LD686("192.168.170.101")

led.rgb = (255, 10, 123)