import time
import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

while (1):
	ser.write('m1255!')
	print 'm1255!'
	time.sleep(2)
	ser.write('m1127!')
	print 'm1127!'
	time.sleep(2)