# LaserDectFunct.py

"""

Provides function definitions for laser detection

Module written as part of Principles of Engineering, Fall 2013 at Olin College of Engineering

"""

from SimpleCV import *
import cv2
import time


def FindLaser(image, RedThreshold,GreenThreshold, BlueThreshold):
    """Returns the (x,y) tuple which corresponds to the average of all the red ([255, 0, 0]) points in the image"""
    from numpy import mean

    #Split into RGB channels. red, green, & blue are image classes 
    try:

        (red, green, blue) = image.splitChannels(False)

    except:
        errormessage='No camera image detected; Please check to ensure that you have selected the right camera'
        return (None, errormessage)

    #Get matrices for each color channel. EX:  gmat[50][70] returns a three-member 'vector' in the form [R,G,B], where R, G, & B are 0-255 color values

    gmat = green.getNumpy()
    bmat = blue.getNumpy()
    rmat = red.getNumpy()

    sliced_red = rmat[:, :, 0]

    maxVal = np.max(sliced_red)

    x, y = np.where(sliced_red == maxVal)

    pts = zip(x.tolist(), y.tolist())

    #pts is a list of (x,y) tuples which correspond to points where the red channel is at a maximum. mx gives this maximum value. We do not use it.
    # mx,pts=rmat.simple_maxValue(locations=True)

    #Splits pts tuples into two lists, one of x-red max value points, and one of y-red max value points
    rmvpx, rmvpy = zip(*pts)

    #Declares/clears two lists
    redx = []
    redy = []

    #The for-loop evaluates the blue and green value at each max red point. This is because white (255,255,255), (255,255,0), and red(255,0,0) all will appear to be a maximum on the red channel. By checking the B & G values at each point, we can avoid identifying yellow or white areas as lasers.
    for n in range(len(pts)):
        bv = bmat[rmvpx[n]][rmvpy[n]][2]
        gv = gmat[rmvpx[n]][rmvpy[n]][1]
        rv = rmat[rmvpx[n]][rmvpy[n]][0]

        # If the blue AND the green value at a point are under their appropriate threshold parameter, then they are confirmed to be sufficiently red, and their coordinates are apppended to lists
        if gv < GreenThreshold and bv < BlueThreshold and rv > RedThreshold:
        # if not much blue and green, then it is red
            redx.append(rmvpx[n])
            redy.append(rmvpy[n])

    #Combine the redx and redy coordinates into a list of (x,y) tuples
    redPTS = zip(redx, redy)

    #Calculate the average X and Y value from all the points we confirmed to be red. The try-except statement takes care of scenarios where the function detects no red points. In this case, it passes out it's own AvgX and AvgY values. These can be configured to make it easy for the robot to detect and react to this error (e.g. if AvgMax==(-2,-2): STOP!)
    try:
        (AvgX, AvgY) = tuple(map(mean, zip(*redPTS)))
    except ValueError:
        AvgX = 0
        AvgY = 0

    #Converts the calculated average coordinates to integers (because decimal pixels don't make sense) and saves them as an (x,y) tuple
    AvgMax = (int(AvgX), int(AvgY))

    #Draws all the confirmed red pixels with blue dots. Draws the average of all these points with a larger black point. Displays the original image with the points overlayed. (can be eliminated for RPi running)
    
    # image.drawPoints(redPTS, color=Color.BLUE, sz=1, width=-1)
    # image.drawPoints([AvgMax], color=Color.BLACK,sz=3,width=-1)
    # image.show(type='window')

    #Return the (x,y) tuple containing the average of all the confirmed red points
    return AvgMax


def get_laser_pos(cap):
    start = time.time()

    res = []
    xvalues = []
    yvalues = []
    LaserErrors = 0

    while len(res) != 2:

        simplecvimg = cap.getImage()

        Max = FindLaser(simplecvimg, 220, 200, 200)

        if Max[0] == None:
            return Max

        x_value, y_value = Max

        if x_value != 0 and y_value != 0:
            res.append(Max)
        else:
            LaserErrors += 1  # Count the number of images w/ no found laser

        if LaserErrors == 3:  # Number of unfound laser images before bot stop
            res = [(-1, -1), (-1, -1)]  # Pass out error condition
            LaserErrors == 0  # Reset error counter

    for xval, yval in res:
        xvalues.append(xval)
        yvalues.append(yval)

    aver_x = sum(xvalues) / len(xvalues)
    aver_y = sum(yvalues) / len(yvalues)

    aver_point = (aver_x, aver_y)

    return aver_point


def cont_get_laser_pos(cap):

    res = []
    xvalues = []
    yvalues = []

    while True:

        ret, img = cap.read()

        key = cv2.waitKey(5)

        simplecvimg = Image(img, cv2image=True)

        Max = FindLaser(simplecvimg, 220, 200, 200)

        print Max

if __name__ == '__main__':
    print "Waiting for user to be ready"
    time.sleep(3)
    print "Starting now"
    test = get_laser_pos()
    print test

    #print cont_get_laser_pos()