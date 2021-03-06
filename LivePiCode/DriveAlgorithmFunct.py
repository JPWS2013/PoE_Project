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
    LeftDirec = str(ld)
    RightDirec = str(rd)

    # Fills in leading zeros so speed is always 3 digits
    RightSp = rightspeed.zfill(3)
    LeftSp = leftspeed.zfill(3)

    Transmission = RightSp + LeftSp + RightDirec + LeftDirec + chr(003)

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

    cap = cv2.VideoCapture(c)
    # set the width and height, and set the exposure time
    cap.set(3, 640)  # Width
    cap.set(4, 320)  # Height
    cap.set(10, 0.4)  # Brightness
    cap.set(12, 3)  # Saturation
    #cap.set(15, 0.2) #Exposure

    return cap


def Initialize_simpleCamera(c=0):
    cap = Camera()
    return cap