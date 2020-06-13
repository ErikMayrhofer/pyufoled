import os
from time import sleep

import pyufoled as mhl


#results = mhl.LD686.scan(1)
#for ip, message in results.items():
#    print(f"{ip}: ({message})")

led = mhl.LD686("192.168.170.102")
#print(led.on)
#led.on = False
#print(led.on)
#led.on = True
#led.rgb = (186, 186, 186)

#sleep(1)

#led.send_raw(mhl.BYTE_MSGTYPE_POWER)

# for i in range(255):
#     hsv = (i/255, 1, 1)
#     led.hsv = hsv
#     print(f"{hsv} -> {led.hsv}")


#Send: MSGTYPE_POWER 0fcs
#Receive: 80 MSGTYPE_POWER POWER_ON cs?