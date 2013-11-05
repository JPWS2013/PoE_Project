import SimpleCV as cv

disp=cv.Display()
cam=cv.Camera()

while disp.isNotDone():

	if disp.mouseLeft:
		break
		
	img=cam.getImage()
	blobs=img.findBlobs()

	if blobs:
		blobs.draw()

	img.save(disp)
