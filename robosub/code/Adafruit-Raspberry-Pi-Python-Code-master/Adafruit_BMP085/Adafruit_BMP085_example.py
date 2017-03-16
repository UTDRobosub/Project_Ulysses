#!/usr/bin/python

from Adafruit_BMP085 import BMP085
import time
import os

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the BMP085 and use STANDARD mode (default value)
# bmp = BMP085(0x77, debug=True)
bmp = BMP085(0x77)

# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
# bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode
while(True):

	temp = bmp.readTemperature()

	# Read the current barometric pressure level
	pressure = bmp.readPressure()

	# To calculate altitude based on an estimated mean sea level pressure
	# (1013.25 hPa) call the function as follows, but this won't be very accurate
	altitude = bmp.readAltitude()

	# To specify a more accurate altitude, enter the correct mean sea level
	# pressure level.  For example, if the current pressure level is 1023.50 hPa
	# enter 102350 since we include two decimal places in the integer value
	# altitude = bmp.readAltitude(102350)
	#os.system('cls')
	#print "Temperature: %.2f C" % temp
	#value = (pressure / 100.0) # in hpa
	value = (pressure) * 0.0002953 # in hg
	print value
	#print "Altitude:    %.2f" % altitude
	time.sleep(1)
