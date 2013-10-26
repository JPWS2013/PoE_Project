import SimpleCV as cv

display= cv.Display()
c=cv.Camera()
normaldisplay=True

while display.isNotDone():
    if display.mouseRight:
        normaldisplay=not(normaldisplay)
        prin
