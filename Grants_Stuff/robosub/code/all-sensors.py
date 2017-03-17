
#Reads both the accel/magnetometer (LSM303) and temp/pressure sensor (BMP085) at the same time.

import time
from time import sleep

import sys
sys.path.append("/home/pi/robosub/code/Adafruit-Raspberry-Pi-Python-Code-master/Adafruit_BMP085")
sys.path.append("/home/pi/robosub/code/Adafruit-Raspberry-Pi-Python-Code-master/Adafruit_LSM303")

from Adafruit_BMP085 import BMP085
from Adafruit_LSM303 import Adafruit_LSM303

bmp=BMP085(0x77)
lsm=Adafruit_LSM303()

while True:
	print lsm.read()
	print bmp.readTemperature()
	print bmp.readPressure()
	sleep(1)

