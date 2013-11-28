"""

Binary Drive Control Module

"""

import DriveAlgorithmFunct as daf
import LaserDetectFunct as ldf

def Steering(x1):
    """Checks to see whether the bot should execute a left/right turn"""
    #RETURNS A LIST WITH THE RIGHTSPEED and LEFTSPEED for the appropriate turn
    
    LeftSp=127
    RightSp=127

    if x1 < 320:
        print "I'm turning Left"
        LeftSp = 50
        RightSp = 240

    if x1 > 320:
        print "I'm turning Right"
        LeftSp = 240
        RightSp = 50

    return [RightSp, LeftSp]


def Speed(yval1):
    """Checks to see whether the bot should go fast/slow"""
    #RETURNS A LIST WITH THE RIGHTSPEED and LEFTSPEED for the appropriate vel.
    if yval1 < 160:
        print "I'm slowing down"
        LeftSp = 100
        RightSp = 100

    if yval1 > 160:
        print "I'm speeding up"
        LeftSp = 255
        RightSp = 255

    return [RightSp, LeftSp]


def Combine(spRight, spLeft, drRight, drLeft):
    """Combines binary driving instructions. Faster+Right=FastRight"""
    # RETURNS TUPLE (RIGHTWHEELSPEED,LEFTWHEELSPEED).
    RightWheel = (spRight + drRight) / 2
    LeftWheel = (spLeft + drLeft) / 2
    return (RightWheel, LeftWheel)


def Drive(PL):
    """Function which calls binary control functions"""
    #RETURNS TUPLE (RIGHTWHEELSPEED,LEFTWHEELSPEED)
    SteerPoints = Steering(PL[0])
    SpeedPoints = Speed(PL[1])
    FinalControl = Combine(SpeedPoints[0], SpeedPoints[1], SteerPoints[0], SteerPoints[1])
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

def drive_decision(cap):
    point1 = ldf.get_laser_pos(cap)
    #point2 = ldf.get_laser_pos(cap)

    xval1, yval1 = point1

    # xval2, yval2 = point2

    # elapsed = time.time() - start
    # print elapsed

    # PointList = [xval1, xval2, yval1, yval2]

    PointList = [xval1, yval1]

    DriveSpeeds = Drive(PointList)

    RightSp, LeftSp = SpeedChecker(DriveSpeeds)

    return (RightSp, LeftSp)


if __name__ == '__main__':

    cap=daf.Initialize_Camera()

    while True:
        # start = time.time()

        res=drive_decision(cap)

        # daf.Pi2Ard(res[0], res[1], 2, 2)