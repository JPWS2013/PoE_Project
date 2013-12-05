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
    #start=time.time()
    
    #Split into RGB channels. red, green, & blue are image classes 
    try:

        (red, green, blue)=image.splitChannels(False)

    except:
        errormessage='No camera image detected; Please check to ensure that you have selected the right camera'
        return (None, errormessage)
    
    #Get matrices for each color channel. EX:  gmat[50][70] returns a three-member 'vector' in the form [R,G,B], where R, G, & B are 0-255 color values
    #time1=time.time()
    
    gmat=green.getNumpy()
    bmat=blue.getNumpy()
    rmat=red.getNumpy() #Not used

    sliced_red=rmat[:,:,0]

    maxVal=np.max(sliced_red)

    x,y=np.where(sliced_red==maxVal)

    pts=zip(x.tolist(), y.tolist())

    #time2=time.time()
    #elapsed2=time2-time1
    #print "pt2 = ", elapsed2
    #pts is a list of (x,y) tuples which correspond to points where the red channel is at a maximum. mx gives this maximum value. We do not use it.
    # mx,pts=rmat.simple_maxValue(locations=True)

    #Splits pts tuples into two lists, one of x-red max value points, and one of y-red max value points
    rmvpx,rmvpy=zip(*pts)

    #Declares/clears two lists
    redx=[]
    redy=[]

    #The for-loop evaluates the blue and green value at each max red point. This is because white (255,255,255), (255,255,0), and red(255,0,0) all will appear to be a maximum on the red channel. By checking the B & G values at each point, we can avoid identifying yellow or white areas as lasers.
    for n in range(len(pts)):
        bv=bmat[rmvpx[n]][rmvpy[n]][2]  #Could theoretically use image matrix 
        gv=gmat[rmvpx[n]][rmvpy[n]][1]  #Then could be done in one line,                                        grabbing two values
        rv=rmat[rmvpx[n]][rmvpy[n]][0]

        #If the blue AND the green value at a point are under their appropriate threshold parameter, then they are confirmed to be sufficiently red, and their coordinates are apppended to lists
        if gv<GreenThreshold and bv<BlueThreshold and rv>RedThreshold:  #if not much blue and green, then it is red
            redx.append(rmvpx[n])
            redy.append(rmvpy[n])

    #Combine the redx and redy coordinates into a list of (x,y) tuples
    redPTS=zip(redx,redy)

    #Calculate the average X and Y value from all the points we confirmed to be red. The try-except statement takes care of scenarios where the function detects no red points. In this case, it passes out it's own AvgX and AvgY values. These can be configured to make it easy for the robot to detect and react to this error (e.g. if AvgMax==(-2,-2): STOP!)
    try:
        (AvgX,AvgY)=tuple(map(mean, zip(*redPTS)))
    except ValueError:
        AvgX=0
        AvgY=0
    

    #Converts the calculated average coordinates to integers (because decimal pixels don't make sense) and saves them as an (x,y) tuple
    AvgMax=(int(AvgX), int(AvgY))

    #Draws all the confirmed red pixels with blue dots. Draws the average of all these points with a larger black point. Displays the original image with the points overlayed. (can be eliminated for RPi running)
    # image.drawPoints(redPTS, color=Color.BLUE, sz=1, width=-1)
    # image.drawPoints([AvgMax], color=Color.BLACK,sz=3,width=-1)
    # image.show(type='window')

    #Return the (x,y) tuple containing the average of all the confirmed red points
    return AvgMax

def get_laser_pos(cap):
    start=time.time()

    res=[]
    xvalues=[]
    yvalues=[]
    LaserErrors = 0

    # cap = cv2.VideoCapture(1)
    # #set the width and height, and UNSUCCESSFULLY set the exposure time
    # cap.set(3,640)
    # cap.set(4,320)
    # cap.set(10, 0.4)
    # cap.set(12, 3)

    #cam=Camera(1)
    #print "init time= ", time.time()-start
    #Timer=time.clock()
    while len(res)!=2:
        #time1=time.time()

        simplecvimg=cap.getImage()

        #print type(simplecvimg)
        
        # cv2.imshow("input", img)
        #cv2.imshow("thresholded", imgray*thresh2)

        # time2=time.time()
        # elapsed1=time2-time1
        # print "elapsed1= ", elapsed1

        #key = cv2.waitKey(5)

        # ret, img = cap.read()
        # simplecvimg=Image(img, cv2image=True)

        # time3=time.time()
        # elapsed2=time3-time2
        # print "elapsed2= ", elapsed2
        # simplecvimg.show()
        #image=simplecvimg.crop(320-150, 160-75, 300, 150)

        # time2=time.time()
        # elapsed1=time2-time1
        # print "elapsed1= ", elapsed1

        
        Max=FindLaser(simplecvimg,220, 200, 200)

        if Max[0]==None:
            return Max 
        #print Max

        # time3=time.time()
        # elapsed2=time3-time2
        # print "elapsed2= ",elapsed2

        x_value, y_value=Max

        if x_value != 0 and y_value != 0:
            res.append(Max)
        else:
            LaserErrors += 1 #Count the number of images w/ no found laser

        if LaserErrors == 3  # Number of unfound laser images before bot stop
            res = [(-1,-1), (-1,-1)] #Pass out error condition
            LaserErrors == 0 #Reset error counter


    #print res

    for xval, yval in res:
        xvalues.append(xval)
        yvalues.append(yval)

    aver_x=sum(xvalues)/len(xvalues)
    aver_y=sum(yvalues)/len(yvalues)

    aver_point=(aver_x, aver_y)

    # elapsed3=time.time()-time2
    # print elapsed3

    return aver_point

def cont_get_laser_pos(cap):

    res=[]
    xvalues=[]
    yvalues=[]

    while True:
        # img=cam.getImage()
        ret, img = cap.read()
        # cv2.imshow("input", img)
        #cv2.imshow("thresholded", imgray*thresh2)

        key = cv2.waitKey(5)

        simplecvimg=Image(img, cv2image=True)

        #image=simplecvimg.crop(320-150, 160-75, 300, 150)

        Max=FindLaser(simplecvimg,220, 200, 200)
        #print Max
        print Max

if __name__ == '__main__':
    print "Waiting for user to be ready"
    time.sleep(3)
    print "Starting now"
    test=get_laser_pos()
    print test

    #print cont_get_laser_pos()
