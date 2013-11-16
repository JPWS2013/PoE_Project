import LaserDectFunct as ldf
from SimpleCV import *
import cv2
import time
import serial


def InitializeSerial(sp):
    # Opening the serial port resets the Arduino. This waits for the Arduino
    # to print 'Ready' to indicate that it has started and is prepared to
    # send/recieve data
    global slink  # Saves us from passing serial link into each function
    # Initialize variable used for confirming Arduino readiness
    ArduinoReady = 2000

    slink = serial.Serial(sp, 9600)
    # Print confirmation that Pyserial has opened the serial port
    print 'Port Opened'

    while ArduinoReady == 2000:
        print ArduinoReady
        # Waits to see that the Arduino has outputted a value to the serial
        # port. This indicates that the Arduino has reset and is ready to
        # recieve data
        AR = slink.readline()

        # Checks to see that the Arduino has outputted digits. Not just
        # whitespace
        try:
            float(AR)
            ArduinoReady = AR
        except ValueError:
            ArduinoReady = 2000

        print ArduinoReady

    # Print confirmation that the Arduino is ready to recieve data
    print 'Ready'


def Pi2Ard(rs, ls, ld, rd):  # Pi to Arduino serial communications
    rightspeed = str(rs)
    leftspeed = str(ls)
    LeftDirection = str(ld)
    RightDirection = str(rd)

    # Fills in leading zeros so speed is always 3 digits
    RightSpeed = rightspeed.zfill(3)
    LeftSpeed = leftspeed.zfill(3)

    Transmission = RightSpeed + LeftSpeed + RightDirection + LeftDirection + chr(003)

    slink.write(Transmission)  # Write the new message to the serial port
    # Print confirmation of sent message
    print "Transmission : " + Transmission


def CloseSerial():  # Stop drive motors & close Pi<-->Arduino serial link
    slink.write(str(00000000) + chr(003))  # release the motors when finished
    slink.close()  # After data collection, the serial port is closed.
    #'Serial Link Closed' is printed to verify a successful closing of the
    # serial connection
    print 'Serial Link Closed'


InitializeSerial('COM5')


cap = cv2.VideoCapture(1)
# set the width and height, and UNSUCCESSFULLY set the exposure time
cap.set(3, 640)
cap.set(4, 320)
cap.set(10, 0.4)
cap.set(12, 3)


# point1=ldf.get_laser_pos(cap)
while True:
    start = time.time()

    point1 = ldf.get_laser_pos(cap)
    point2 = ldf.get_laser_pos(cap)

    xval1, yval1 = point1

    xval2, yval2 = point2

    elapsed = time.time() - start
    print elapsed

    if xval1 > xval2:
        print "I'm turning Left"
        LeftSp = 240
        RightSp = 50

    if xval1 < xval2:
        print "I'm turning Right"
        LeftSp = 50
        RightSp = 240

    if yval1 < yval2:
        print "I'm slowing down"
        LeftSp = 100
        RightSp = 100

    if yval1 > yval2:
        print "I'm speeding up"
        LeftSp = 255
        RightSp = 255

    Pi2Ard(LeftSp, RightSP, 2, 2)
