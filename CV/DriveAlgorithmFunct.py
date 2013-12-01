#DriveAlgorithmFunct.py

"""

Provides function definitions for making driving decisions on the autonomous domino-laying robot

Module written for Principles of Engineering, Fall 2013 at Olin College of Engineering

"""

import LaserDetectFunct as ldf
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


def Initialize_CVCamera(c=0):
    #InitializeSerial('COM5')


    cap = cv2.VideoCapture(c)
    # set the width and height, and set the exposure time
    cap.set(3, 640) #Width
    cap.set(4, 320) #Height
    cap.set(10, 0.4) #Brightness
    cap.set(12, 3) #Saturation
    #cap.set(15, 0.2) #Exposure

    return cap

def Initialize_simpleCamera(c=0):
    cap=Camera(c)
    return cap

# def drive_decision(cap):
#     point1 = ldf.get_laser_pos(cap)

#     if point1[0]==None:
#         print point1[1]
#         break

#     xval1, yval1 = point1

#     # elapsed = time.time() - start
#     # print elapsed
#     LeftSp=127
#     LeftSp=127
    
#     if xval1 <320:
#         print "I'm turning Left"
#         LeftSp = 240
#         RightSp = 50

#     elif xval1 >320:
#         print "I'm turning Right"
#         LeftSp = 50
#         RightSp = 240

#     elif xval1==320:
#         print"I'm going straight"

#     if xval == 320:
#         print "I'm not turning"

#     if yval1 < 160:
#         print "I'm slowing down"
#         LeftSp = 100
#         RightSp = 100

#     if yval1 > 160:
#         print "I'm speeding up"
#         LeftSp = 255
#         RightSp = 255

#     return (LeftSp, RightSp)