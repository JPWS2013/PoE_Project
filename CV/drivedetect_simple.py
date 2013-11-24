"""
A simplified version of original drivedetect script that does not implement serial port functions 
"""
import LaserDectFunct as ldf
from SimpleCV import *
import cv2
import time

cap = cv2.VideoCapture(1)
# set the width and height, and set the exposure time
cap.set(3, 640)
cap.set(4, 320)
cap.set(10, 0.4)
cap.set(12, 3)


# point1=ldf.get_laser_pos(cap)
while True:
    #start = time.time()

    point1 = ldf.get_laser_pos(cap)
    point2 = ldf.get_laser_pos(cap)

    xval1, yval1 = point1

    xval2, yval2 = point2

    #elapsed = time.time() - start
    #print elapsed

    if xval1 > xval2:
        print "I'm turning Left"

    if xval1 < xval2:
        print "I'm turning Right"

    if yval1 < yval2:
        print "I'm slowing down"

    if yval1 > yval2:
        print "I'm speeding up"

    print ' '

