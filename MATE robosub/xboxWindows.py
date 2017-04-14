#A class for reading values from an xbox controller by Martin O'Hanlon www.stuffaboutcode.com
#UDP Network mod by Grant Carr grantcharr@gmail.com
#This script requires Python 2.7, Xbox360 controller on any usb port, and Pygame library -> http://pygame.org/ftp/pygame-1.9.1.win32-py2.7.msi <- download link

# Data output format is "Button ID  Button Value"

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

#Run this script on your robot to read UDP data, or test script by saving and running along side main program on pc
'''
import socket

#UDP setup
HOST = '' 
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", PORT))
list = [" "]

#returns UDP data as string list
def getUDP():
    data, addr = s.recvfrom(1024)
    li = []
    li = data.split()
    return li

#main loop, will exit when xbox360 BACK button is pressed
while list[0] != "12":
        list = getUDP()

        #check for D-pad special input
        if(list[0] == "17"):
            print list[0] + " " + list[1] + " " + list[2]

        #check for normal input
        else:
            print list[0] + " " + list[1]

#required to safely close the port
s.close()


'''

#Start of the main program
import pygame
from pygame.locals import *
import os, sys
import threading
import time
import socket

PACKET = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
#UDP setup
IP = '192.168.43.206' # <- the ip address of the robot on the network
PORT = 8888

question = raw_input('Use this IP '+ IP + ' y/n: ')
if (question=='n' or question=='N'):
    IP = raw_input('Enter new IP: ')
sPACKET = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'        
PACKETDATA = ' '
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.connect((IP, PORT))

#Main class for reading the xbox controller values
class XboxController(threading.Thread):

    #internal ids for the xbox controls
    class XboxControls():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 2
        RTHUMBY = 3
        RTRIGGER = 4
        LTRIGGER = 5
        A = 6
        B = 7
        X = 8
        Y = 9
        LB = 10
        RB = 11
        BACK = 12
        START = 13
        XBOX = 14
        LEFTTHUMB = 15
        RIGHTTHUMB = 16
        DPAD = 17

    #pygame axis constants for the analogue controls of the xbox controller
    class PyGameAxis():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 2
        RTHUMBY = 3
        RTRIGGER = 4
        LTRIGGER = 5

    #pygame constants for the buttons of the xbox controller
    class PyGameButtons():
        A = 0
        B = 1
        X = 2
        Y = 3
        LB = 4
        RB = 5
        BACK = 6
        START = 7
        XBOX = 8
        LEFTTHUMB = 9
        RIGHTTHUMB = 10

    #map between pygame axis (analogue stick) ids and xbox control ids
    AXISCONTROLMAP = {PyGameAxis.LTHUMBX: XboxControls.LTHUMBX,
                      PyGameAxis.LTHUMBY: XboxControls.LTHUMBY,
                      PyGameAxis.RTHUMBX: XboxControls.RTHUMBX,
                      PyGameAxis.RTHUMBY: XboxControls.RTHUMBY}
    
    #map between pygame axis (trigger) ids and xbox control ids
    TRIGGERCONTROLMAP = {PyGameAxis.RTRIGGER: XboxControls.RTRIGGER,
                         PyGameAxis.LTRIGGER: XboxControls.LTRIGGER}

    #map between pygame buttons ids and xbox contorl ids
    BUTTONCONTROLMAP = {PyGameButtons.A: XboxControls.A,
                        PyGameButtons.B: XboxControls.B,
                        PyGameButtons.X: XboxControls.X,
                        PyGameButtons.Y: XboxControls.Y,
                        PyGameButtons.LB: XboxControls.LB,
                        PyGameButtons.RB: XboxControls.RB,
                        PyGameButtons.BACK: XboxControls.BACK,
                        PyGameButtons.START: XboxControls.START,
                        PyGameButtons.XBOX: XboxControls.XBOX,
                        PyGameButtons.LEFTTHUMB: XboxControls.LEFTTHUMB,
                        PyGameButtons.RIGHTTHUMB: XboxControls.RIGHTTHUMB}
                        
    #setup xbox controller class
    def __init__(self,
                 controllerCallBack = None,
                 joystickNo = 0,
                 deadzone = 0.1,
                 scale = 1,
                 invertYAxis = False):

        #setup threading
        threading.Thread.__init__(self)
        
        #persist values
        self.running = False
        self.controllerCallBack = controllerCallBack
        self.joystickNo = joystickNo
        self.lowerDeadzone = deadzone * -1
        self.upperDeadzone = deadzone
        self.scale = scale
        self.invertYAxis = invertYAxis
        self.controlCallbacks = {}

        #setup controller properties
        self.controlValues = {self.XboxControls.LTHUMBX:0,
                              self.XboxControls.LTHUMBY:0,
                              self.XboxControls.RTHUMBX:0,
                              self.XboxControls.RTHUMBY:0,
                              self.XboxControls.RTRIGGER:0,
                              self.XboxControls.LTRIGGER:0,
                              self.XboxControls.A:0,
                              self.XboxControls.B:0,
                              self.XboxControls.X:0,
                              self.XboxControls.Y:0,
                              self.XboxControls.LB:0,
                              self.XboxControls.RB:0,
                              self.XboxControls.BACK:0,
                              self.XboxControls.START:0,
                              self.XboxControls.XBOX:0,
                              self.XboxControls.LEFTTHUMB:0,
                              self.XboxControls.RIGHTTHUMB:0,
                              self.XboxControls.DPAD:(0,0)}

        #setup pygame
        self._setupPygame(joystickNo)

    #Create controller properties
    @property
    def LTHUMBX(self):
        return self.controlValues[self.XboxControls.LTHUMBX]

    @property
    def LTHUMBY(self):
        return self.controlValues[self.XboxControls.LTHUMBY]

    @property
    def RTHUMBX(self):
        return self.controlValues[self.XboxControls.RTHUMBX]

    @property
    def RTHUMBY(self):
        return self.controlValues[self.XboxControls.RTHUMBY]

    @property
    def RTRIGGER(self):
        return self.controlValues[self.XboxControls.RTRIGGER]

    @property
    def LTRIGGER(self):
        return self.controlValues[self.XboxControls.LTRIGGER]

    @property
    def A(self):
        return self.controlValues[self.XboxControls.A]

    @property
    def B(self):
        return self.controlValues[self.XboxControls.B]

    @property
    def X(self):
        return self.controlValues[self.XboxControls.X]

    @property
    def Y(self):
        return self.controlValues[self.XboxControls.Y]

    @property
    def LB(self):
        return self.controlValues[self.XboxControls.LB]

    @property
    def RB(self):
        return self.controlValues[self.XboxControls.RB]

    @property
    def BACK(self):
        return self.controlValues[self.XboxControls.BACK]

    @property
    def START(self):
        return self.controlValues[self.XboxControls.START]

    @property
    def XBOX(self):
        return self.controlValues[self.XboxControls.XBOX]

    @property
    def LEFTTHUMB(self):
        return self.controlValues[self.XboxControls.LEFTTHUMB]

    @property
    def RIGHTTHUMB(self):
        return self.controlValues[self.XboxControls.RIGHTTHUMB]

    @property
    def DPAD(self):
        return self.controlValues[self.XboxControls.DPAD]

    #setup pygame
    def _setupPygame(self, joystickNo):
        # set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        # init pygame
        pygame.init()
        # create a 1x1 pixel screen, its not used so it doesnt matter
        screen = pygame.display.set_mode((1, 1))
        # init the joystick control
        pygame.joystick.init()
        # how many joysticks are there
        #print pygame.joystick.get_count()
        # get the first joystick
        joy = pygame.joystick.Joystick(joystickNo)
        # init that joystick
        joy.init()

    #called by the thread
    def run(self):
        self._start()

    #start the controller
    def _start(self):
        
        self.running = True
        
        #run until the controller is stopped
        while(self.running):
            #react to the pygame events that come from the xbox controller
            for event in pygame.event.get():

                #thumb sticks, trigger buttons                    
                if event.type == JOYAXISMOTION:
                    #is this axis on our xbox controller
                    if event.axis in self.AXISCONTROLMAP:
                        #is this a y axis
                        yAxis = True if (event.axis == self.PyGameAxis.LTHUMBY or event.axis == self.PyGameAxis.RTHUMBY) else False
                        #update the control value
                        self.updateControlValue(self.AXISCONTROLMAP[event.axis],
                                                self._sortOutAxisValue(event.value, yAxis))
                    #is this axis a trigger
                    if event.axis in self.TRIGGERCONTROLMAP:
                        #update the control value
                        self.updateControlValue(self.TRIGGERCONTROLMAP[event.axis],
                                                self._sortOutTriggerValue(event.value))
                        
                #d pad
                elif event.type == JOYHATMOTION:
                    #update control value
                    self.updateControlValue(self.XboxControls.DPAD, event.value)

                #button pressed and unpressed
                elif event.type == JOYBUTTONUP or event.type == JOYBUTTONDOWN:
                    #is this button on our xbox controller
                    if event.button in self.BUTTONCONTROLMAP:
                        #update control value
                        self.updateControlValue(self.BUTTONCONTROLMAP[event.button],
                                                self._sortOutButtonValue(event.type))
        
    #stops the controller
    def stop(self):
        self.running = False

    #updates a specific value in the control dictionary
    def updateControlValue(self, control, value):
        #if the value has changed update it and call the callbacks
        if self.controlValues[control] != value:
            self.controlValues[control] = value
            self.doCallBacks(control, value)
    
    #calls the call backs if necessary
    def doCallBacks(self, control, value):
        #call the general callback
        if self.controllerCallBack != None: self.controllerCallBack(control, value)

        #has a specific callback been setup?
        if control in self.controlCallbacks:
            self.controlCallbacks[control](value)
            
    #used to add a specific callback to a control
    def setupControlCallback(self, control, callbackFunction):
        # add callback to the dictionary
        self.controlCallbacks[control] = callbackFunction
                
    #scales the axis values, applies the deadzone
    def _sortOutAxisValue(self, value, yAxis = False):
        #invert yAxis
        if yAxis and self.invertYAxis: value = value * -1
        #scale the value
        value = value * self.scale
        #apply the deadzone
        if value < self.upperDeadzone and value > self.lowerDeadzone: value = 0
        return value

    #turns the trigger value into something sensible and scales it
    def _sortOutTriggerValue(self, value):
        #trigger goes -1 to 1 (-1 is off, 1 is full on, half is 0) - I want this to be 0 - 1
        value = max(0,(value + 1) / 2)
        #scale the value
        value = value * self.scale
        return value

    #turns the event type (up/down) into a value
    def _sortOutButtonValue(self, eventType):
        #if the button is down its 1, if the button is up its 0
        value = 1 if eventType == JOYBUTTONDOWN else 0
        return value
    
#tests
if __name__ == '__main__':


    #SEND UDP PACKETS FROM HERE
    #generic call back
    def controlCallBack(xboxControlId, value):
		
        #str1 = ''.join(list1)       #convert list to string
        #print "{} {}".format(xboxControlId, value)        
        idx = "{}".format(xboxControlId)
        idv = "{}".format(value)
        idv = idv.replace("(","")
        idv = idv.replace(",","")
        idv = idv.replace(")","")
        #s.send(PACKETDATA)
        
        #print idx + " " + idv
        if(idx == "0"):
	
            PACKET[0] = "{}".format(int(value))
			
        elif(idx == "1"):
		
            PACKET[1] = "{}".format(int(value))
			
        elif(idx == "2"):
		
            PACKET[2] = "{}".format(int(value))
			
        elif(idx == "3"):
		
            PACKET[3] = "{}".format(int(value))
			
        elif(idx == "4"):
		
            PACKET[4] = "{}".format(int(value))
			
        elif(idx == "6"):
		
            PACKET[5] = idv
		
        elif(idx == "7"):
		
            PACKET[6] = idv
		
        elif(idx == "8"):
		
            PACKET[7] = idv
		
        elif(idx == "9"):
		
            PACKET[8] = idv
		
        elif(idx == "10"):
		
            PACKET[9] = idv
		
        elif(idx == "11"):
		
            PACKET[10] = idv
		
        elif(idx == "12"):
		
            PACKET[11] = idv
		
        elif(idx == "13"):
		
            PACKET[12] = idv
		
        elif(idx == "14"):
		
            PACKET[13] = idv
		
        elif(idx == "15"):
		
            PACKET[14] = idv
			
        elif(idx == "17"):
			
            li = []
            li = idv.split()
			
            if(li[0] == "1"):
                PACKET[15] = idv
			
            if(li[1] == "1"):
                PACKET[16] = idv
		
	
		
        sPACKET = ' '.join(PACKET)
        print sPACKET
        s.send(sPACKET)
        #time.sleep(.05)
        
    #specific callbacks for the left thumb (X & Y)
    def leftThumbX(xValue):
        #print "X,{}".format(xValue)
        n=0
    def leftThumbY(yValue):
        n=0
        #print "{}".format(yValue)

    #setup xbox controller, set out the deadzone and scale, also invert the Y Axis (for some reason in Pygame negative is up - wierd! 
    xboxCont = XboxController(controlCallBack, deadzone = 30, scale = 100, invertYAxis = True)

    #setup the left thumb (X & Y) callbacks
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBX, leftThumbX)
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBY, leftThumbY)

    try:
        #start the controller
        xboxCont.start()
        print "xbox controller running"
        while True:
            #change this to smaller number for faster update
            time.sleep(.05)

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"
        s.close()
    
    #error        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
        
    finally:
        #stop the controller
        xboxCont.stop()
