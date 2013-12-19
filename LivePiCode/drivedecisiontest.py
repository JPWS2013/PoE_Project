"""
This is the main module that will run on dominobot. This module uses computer vision functions in simpleCV and OpenCV in order to detect a laser pointer within a camera image, compute its location within that image and decide how to pilot the robot.

This module was written by Justin Poh and Ryan Eggert for Principles of Engineering, Fall 2013 at Olin College of Engineering
"""

import LaserDetectFunct as ldf
import DriveAlgorithmFunct as daf
from SimpleCV import *
import cv2
import time
import serial
import proportionaldrive as drive

cap = daf.Initialize_simpleCamera()

comport = '/dev/ttyACM0'

daf.InitializeSerial(comport)

while True:

    res = drive.drive_decision(cap)

    daf.Pi2Ard(res[0], res[1], 2, 2)

daf.CloseSerial()