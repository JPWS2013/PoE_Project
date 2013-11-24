import LaserDetectFunct as ldf
import DriveAlgorithmFunct as daf
from SimpleCV import *
import cv2
import time
import serial


cap=daf.Initialize_Camera()
# point1=ldf.get_laser_pos(cap)
while True:
    # start = time.time()

    point1 = ldf.get_laser_pos(cap)

    if point1[0]==None:
        print point1[1]
        break

    xval1, yval1 = point1

    # elapsed = time.time() - start
    # print elapsed

    if xval1 <320:
        print "I'm turning Left"
        LeftSp = 240
        RightSp = 50

    if xval1 >320:
        print "I'm turning Right"
        LeftSp = 50
        RightSp = 240

    if xval == 320:
        print "I'm not turning"

    if yval1 < 160:
        print "I'm slowing down"
        LeftSp = 100
        RightSp = 100

    if yval1 > 160:
        print "I'm speeding up"
        LeftSp = 255
        RightSp = 255

    daf.Pi2Ard(LeftSp, RightSP, 2, 2)