import LaserDectFunct as ldf
from SimpleCV import *
import cv2
import time
import serial
from numpy import interp

# Variable Declarations

global ImageWidth
global ImageHeight

ImageWidth = 640
ImageHeight = 320


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
cap.set(3, ImageWidth)
cap.set(4, ImageHeight)
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

    PointList = [xval1, xval2, yval1, yval2]

    DriveSpeeds = BinaryDrive(PointList)

    RightSp, LeftSp = SpeedChecker(DriveSpeeds)

    Pi2Ard(RightSp, LeftSP, 2, 2)


def BinarySteering(x1, x2):
    """Checks to see whether the bot should execute a left/right turn"""
    #RETURNS A LIST WITH THE RIGHTSPEED and LEFTSPEED for the appropriate turn
    if x1 > x2:
        print "I'm turning Left"
        LeftSp = 240
        RightSp = 50

    if x1 < x2:
        print "I'm turning Right"
        LeftSp = 50
        RightSp = 240

    return [RightSp, LeftSp]


def BinarySpeed(y1, y2):
    """Checks to see whether the bot should go fast/slow"""
    #RETURNS A LIST WITH THE RIGHTSPEED and LEFTSPEED for the appropriate vel.
    if y1 < y2:
        print "I'm slowing down"
        LeftSp = 100
        RightSp = 100

    if y1 > y2:
        print "I'm speeding up"
        LeftSp = 255
        RightSp = 255

    return [RightSp, LeftSp]


def BinaryCombine(spRight, spLeft, drRight, drLeft):
    """Combines binary driving instructions. Faster+Right=FastRight"""
    # RETURNS TUPLE (RIGHTWHEELSPEED,LEFTWHEELSPEED).
    RightWheel = (spRight + drRight) / 2
    LeftWheel = (spLeft + drLeft) / 2
    return (RightWheel, LeftWheel)


def BinaryDrive(PL):
    """Function which calls binary control functions"""
    #RETURNS TUPLE (RIGHTWHEELSPEED,LEFTWHEELSPEED)
    SpeedPoints = BinarySteering(PL[0], PL[1])
    DrivePoints = BinarySpeed(PL[2], PL[3])
    FinalControl = BinaryCombine(SpeedPoints, DrivePoints)
    return FinalControl


def ProportionalSteering(x1, x2):
    """Determines the ratio of speeds between the two wheels"""
    # RETURNS WHEELPROP: LEFTWHEEL = RIGHTWHEEL * WHEELPROP
    # 0 <= WHEELPROP
    xdiff = x2 - x1
    WheelProp = interp(abs(xdiff), [0, ImageWidth], [0, 1])
    # WheelProp tells you that the speed of one wheel will be
    # WheelProp*OtherWheelSpeed. To figue out which wheel, go on.
    if xdiff > 0:
        WheelProp = WheelProp ** -1
   # If xdiff is positive, x2>x1, and the bot should turn right. This means
   # the left wheel should turn faster than the right wheel. Hence the
   # WheelProp value is inverted.

   # If xdiff is negative, x1>x2, and the bot should turn left. This means
   # the left wheel should turn slower than the right wheel. Hence it uses
   # the original WheelProp value (which ranges from 0 to 1)

    return WheelProp


def ProportionalSpeed(y1, y2, steering):
    ydiff = y1 - y2

    # We select a minimum speed such that if you drive one motor at this
    # speed, the other can be driven at any speed (greater than this, of
    # course) without knocking over dominoes.
    MinWheelSpeed = 30

    # CruiseSpeed = ((255-MinWheelSpeed)/2)+MinWheelSpeed

    AvgSpeed = interp(ydiff, [-ImageHeight, ImageHeight], [MinWheelSpeed, 255])

    RightWheel = (2 * AvgSpeed) / (1 + steering)
    LeftWheel = steering * RightWheel

    if RightWheel < MinWheelSpeed:
        # Maintain Speed
        # print "Turn too sharp. Attempting to modify turning angle"
        # RightWheel = MinWheelSpeed
        # LeftWheel = (2 * AvgSpeed) - MinWheelSpeed

        # OR###

        # Attempt to maintain turning angle
        print "Turn too sharp. Attempting to modify speed"
        RightWheel = MinWheelSpeed
        LeftWheel = (steering ** -1) * RightWheel

    if LeftWheel < MinWheelSpeed:
        # Maintain Speed
        # print "Turn too sharp. Attempting to modify turning angle"
        # LeftWheel = MinWheelSpeed
        # RightWheel = (2 * AvgSpeed) - MinWheelSpeed

         # OR###

        # Attempt to maintain turning angle
        print "Turn too sharp. Attempting to modify speed"
        LeftWheel = MinWheelSpeed
        RightWheel = (steering ** -1) * LeftWheel

    return (RightWheel, LeftWheel)


def ProportionalDrive(PL):
    SteeringProportion = ProportionalSteering(PL[0], PL[1])
    FinalControl = ProportionalSpeed(PL[2], PL[3], SteeringProportion)
    return FinalControl


def SpeedChecker(UncheckedSpeeds):
    if UncheckedSpeeds[0] > 255:
        CheckedRight = 255
        print "Right Wheel Speed too great. Decreasing"
    else:
        CheckedRight = UncheckedSpeeds[0]

    if UncheckedSpeeds[1] > 255:
        CheckedLeft = 255
        print "Left Wheel Speed too great. Decreasing"
    else:
        CheckedLeft = UncheckedSpeeds[1]

    return (CheckedRight, CheckedLeft)
