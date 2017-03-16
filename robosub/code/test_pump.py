#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
# Initialise the PWM device using the default address
pwm = PWM(0x40)
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

#pump variables  pwm.setPWM(channel, 0, pulse) channel = 0-11, pulse = 0 or 4095
#only able to run 5 pumps max
#empty glass 68.175g

# @ 40 sec : 53.65 FULL SHOT 1.5oz

p1 = 4  # @ 40 sec : 53.65		=  1.34125  g/sec
p2 = 11 # @ 40 sec : 42.845		=  1.071125 g/sec
p3 = 9  # @ 40 sec : 41.63 		=  1.04075  g/sec
p4 = 2  # @ 40 sec : 43.82		=  1.0955	g/sec
p5 = 0  # @ 40 sec : 42.553		=  1.063825	g/sec
p6 = 7  # @ 40 sec : 42.2575	=  1.056438 g/sec
p1r = 5 
p2r = 10 
p3r = 8 
p4r = 3 
p5r = 1 
p6r = 6 


def primePumps():
  pwm.setPWM(p1,0,4095)
  pwm.setPWM(p2,0,4095)
  pwm.setPWM(p3,0,4095)
  time.sleep(15)
  pwm.setPWM(p1,0,0)
  pwm.setPWM(p2,0,0)
  pwm.setPWM(p3,0,0)
  pwm.setPWM(p4,0,4095)
  pwm.setPWM(p5,0,4095)
  pwm.setPWM(p6,0,4095)
  time.sleep(15)
  pwm.setPWM(p4,0,0)
  pwm.setPWM(p5,0,0)
  pwm.setPWM(p6,0,0)
  
def clearPumps():
  #clear group 1,2,3
  pwm.setPWM(p1r,0,4095)
  pwm.setPWM(p2r,0,4095)
  pwm.setPWM(p3r,0,4095)
  time.sleep(60)
  pwm.setPWM(p1r,0,0)
  pwm.setPWM(p2r,0,0)
  pwm.setPWM(p3r,0,0)
  #clear group 4,5,6
  pwm.setPWM(p4r,0,4095)
  pwm.setPWM(p5r,0,4095)
  pwm.setPWM(p6r,0,4095)
  time.sleep(60)
  pwm.setPWM(p4r,0,0)
  pwm.setPWM(p5r,0,0)
  pwm.setPWM(p6r,0,0)
 
#pour a single shot
def pourShot(pump):
  #1 shot is 44.36 grams	
	
  if pump == p1:
    seconds = 33.07
  elif pump == p2:
    seconds = 41.41
  elif pump == p3:
    seconds = 42.62
  elif pump == p4:
    seconds = 40.49
  elif pump == p5:
    seconds = 41.7
  elif pump == p6:
    seconds = 41.99
  pwm.setPWM(pump, 0, 4095)
  time.sleep(seconds)
  pwm.setPWM(pump, 0, 0)

pourShot(p1)
time.sleep(5)
pourShot(p2)
time.sleep(5)
clearPumps()