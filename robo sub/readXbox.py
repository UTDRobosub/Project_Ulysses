import socket
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
HOST = '' 
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", PORT))

packet = ""
li = []
angle = 0.0

thrust = 0

forwardThrust = 0 #2
backwardsThrust = 0
list = []

#loop
while (1):

	#get packet
	list = getUDP()
	
	#forward or backwards thrust, get from left and right analog trigger
	thrust = int(list[2])
	#convert to positive value
	thrust = thrust + 99
	#convert to 0 - 255   0 + 99 == 127 neutral 
	thrust = int(thrust * 1.29)

	
	
	
#returns UDP data as string list
def getUDP():
    data, addr = s.recvfrom(1024)
    li = []
    li = data.split()
    return li





	 

	 
def getAngle(x, y):
	rads = atan2(y,x)
	rads %= 2*pi
	degs = degrees(rads)
	#angle =(math.degrees(math.atan2(x2,y2)))
	#angle = angle * 57
	#magnitude = math.hypot(x2,y2)
	#list = [angle, magnitude]
	return degs	