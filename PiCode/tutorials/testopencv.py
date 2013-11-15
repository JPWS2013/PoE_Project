import cv2
import SimpleCV as cv

#capture from camera at location 0
cap = cv2.VideoCapture(1)
#set the width and height, and UNSUCCESSFULLY set the exposure time
cap.set(3,640)
cap.set(4,320)
cap.set(10, 1)
cap.set(12, 1)

while True:
    ret, img = cap.read()
    # cv2.imshow("input", img)
    #cv2.imshow("thresholded", imgray*thresh2)

    key = cv2.waitKey(10)

    simplecvimg=cv.Image(img, cv2image=True)

    #print type(simplecvimg)
    simplecvimg.show()

    red_pointer=simplecvimg.colorDistance(cv.Color.RED)#(color=(19.34367347, 19.01224490, 107.48408163))

    # only_pointer=simplecvimg-red_pointer

    # pointer_detection=red_pointer.findBlobs()
    
    # if pointer_detection:

    #   for b in pointer_detection:

    #       b.draw()

    #red_pointer.show()
 #    if key == 27:
 #        break


cv2.destroyAllWindows() 
cv2.VideoCapture(0).release()