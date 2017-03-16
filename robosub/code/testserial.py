import serial
import time

port = serial.Serial("/dev/ttyAMA0", baudrate=9600)
buffer1 = "                    ";
buffer2 = "                    ";
buffer3 = "                    ";
buffer4 = "                    ";
port.write(buffer1)
port.write(buffer2)
port.write(buffer3)
port.write(buffer4)

while True:
    port.write(chr(17))
    time.sleep(1)
    port.write(chr(18))
    time.sleep(1)