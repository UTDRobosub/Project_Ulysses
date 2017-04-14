from Adafruit_PWM_Servo_Driver import PWM
import socket
import serial
import time
import sys

pwm = PWM(0x40)
pwm.setPWMFreq(60)

# Output ID map
# Left Joystick X axis = 0
# Left Joystick Y axis = 1
# Left Trigger (positive values 0 to 99) = 2
# Right Trigger (negative values -99 to 0) = 2
# Right Joystick Y axis = 3
# Right Joystick X axis = 4
# A Button = 6
# B Button = 7
# X Button = 8
# Y Button = 9
# Left Bumper = 10
# Right Bumper = 11
# Back = 12
# Start = 13
# Left Joystick click = 14
# Right Joystick click = 15
# Dpad = 17


# pin outs for motors
# back vertical 	pins 0,1	motor 1
# right thruster 	pins 2,3	motor 2 
# front vertical	pins 4,5	motor 3
# front horizon		pins 6,7	motor 4
# back borizon		pins 8,9	motor 5
# left thruster		pins 10,11	motor 6


#network settings
HOST = '' 
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", PORT))
#example packet
packet = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
oldPacket = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]

angle = 0.0

list = []
list = packet


#returns UDP data as string list
def getUDP():
	data, addr = s.recvfrom(1024)
	li = []
	li = data.split()
	return li



#loop
while (1):

	#save previous packet
	oldPacket = packet
	
	#get new packet
	packet = getUDP()
	#print packet
	#left joystick packet, checking x axis, YAW AXIS MOVEMENT

	
	#turning right
	if(int(packet[0]) > 0):
		
		#set motor polarity
		pwm.setPWM(6, 0, 4095) #motor 4 
		pwm.setPWM(8, 0, 4095) #motor 5
		
		motorPower = int(((float(packet[0]))/100)*4095)
		pwm.setPWM(7, 0, motorPower) #motor 4 
		pwm.setPWM(9, 0, motorPower) #motor 4 
		print("right" + str(motorPower))
		
	#turning left
	elif(int(packet[0]) < 0):
	
		pwm.setPWM(6, 0, 0) #motor 4 
		pwm.setPWM(8, 0, 0) #motor 5
		
		motorPower = int(((float(packet[0]))/100)*4095) * -1
		pwm.setPWM(7, 0, motorPower) #motor 4 
		pwm.setPWM(9, 0, motorPower) #motor 4 
		print("left" + str(motorPower))
		
		
		
	elif(int(packet[0]) == 0):
		pwm.setPWM(7, 0, 0) #motor 4 
		pwm.setPWM(9, 0, 0) #motor 4 

	
	#L/R Trigger, checking axis,  variable THRUST forwards/backwards

	
	# right thruster 	pins 2,3	motor 2 
	# left thruster		pins 10,11	motor 6

	#forward
	if(int(packet[2]) < 0):
		#set motor polarity
		pwm.setPWM(2, 0, 4095) #motor 4 
		pwm.setPWM(10, 0, 4095) #motor 5
		
		#set pwm
		motorPower = (int(((float(packet[2]))/99)*4095) * -1)
		pwm.setPWM(3, 0, motorPower) #motor 4 
		pwm.setPWM(11, 0, motorPower) #motor 5
		
	#backwards
	elif(int(packet[2]) > 0):
		#set motor polarity
		pwm.setPWM(2, 0, 0) #motor 4 
		pwm.setPWM(10, 0, 0) #motor 5	
		
		#set pwm
		motorPower = int(((float(packet[2]))/99)*4095)
		pwm.setPWM(3, 0, motorPower) #motor 4 
		pwm.setPWM(11, 0, motorPower) #motor 5
		
	elif(int(packet[2]) == 0):
		pwm.setPWM(3, 0, 0) #motor 4 
		pwm.setPWM(11, 0, 0) #motor 4 		
		


	
	# back vertical 	pins 0,1	motor 1
	# front vertical	pins 4,5	motor 3
	
	
	if(int(packet[3]) > 0):
		#set motor polarity
		pwm.setPWM(0, 0, 4095) #motor 1 
		pwm.setPWM(4, 0, 0) #motor 3
	
		motorPower = int(((float(packet[3]))/100)*4095)
		
		pwm.setPWM(1, 0, motorPower) #motor 4 
		pwm.setPWM(5, 0, motorPower) #motor 5
	
	elif(int(packet[3]) < 0):
		#set motor polarity
		pwm.setPWM(0, 0, 0) #motor 1 
		pwm.setPWM(4, 0, 4095) #motor 3
	
		motorPower = int(((float(packet[3]))/100)*4095) * -1
		pwm.setPWM(1, 0, motorPower) #motor 4 
		pwm.setPWM(5, 0, motorPower) #motor 5	
		
	elif(int(packet[3]) == 0):
		pwm.setPWM(1, 0, 0) #motor 4 
		pwm.setPWM(5, 0, 0) #motor 4 		





	 
def getAngle(x, y):
	rads = atan2(y,x)
	rads %= 2*pi
	degs = degrees(rads)
	#angle =(math.degrees(math.atan2(x2,y2)))
	#angle = angle * 57
	#magnitude = math.hypot(x2,y2)
	#list = [angle, magnitude]
	return degs	
