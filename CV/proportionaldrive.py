import LaserDetectFunct as ldf
import DriveAlgorithmFunct as daf
from numpy import interp

def Steering(x1):
    """Determines the ratio of speeds between the two wheels"""
    # RETURNS WHEELPROP: LEFTWHEEL = RIGHTWHEEL * WHEELPROP
    # 0 <= WHEELPROP

    print "x1=", x1
    
    xdiff = x1 - 320
    
    WheelProp = interp(abs(xdiff), [0, 320], [1, 0])
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


def Speed(y1, steering):
    print "y1=", y1
    
    ydiff = y1 - 180

    # We select a minimum speed such that if you drive one motor at this
    # speed, the other can be driven at any speed (greater than this, of
    # course) without knocking over dominoes.
    MinWheelSpeed = 30

    # CruiseSpeed = ((255-MinWheelSpeed)/2)+MinWheelSpeed

    AvgSpeed = interp(y1, [0, 480], [255, MinWheelSpeed])

    print 'AvgSpeed=', AvgSpeed

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


def Drive(PL):
    SteeringProportion = Steering(PL[0])
    FinalControl = Speed(PL[1], SteeringProportion)
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

        print res

        # daf.Pi2Ard(res[0], res[1], 2, 2)
