import SimpleCV as cv

disp1=cv.Display()
disp2=cv.Display()
cam=cv.Camera(1)

# calib_image=cam.getImage()

# while disp1.isNotDone():
	
# 	if disp1.mouseLeft:
# 		break
# 	calib_image.show()

while disp2.isNotDone():

	if disp2.mouseLeft:
		break
	
	true_b=[]

	img=cam.getImage()

	red_pointer=img.colorDistance(color=(19.34367347, 19.01224490, 107.48408163))

	only_pointer=img-red_pointer

	pointer_detection=only_pointer.findBlobs()
	
	if pointer_detection:

		for b in pointer_detection:

			b.draw()
				# true_b.append((b.area(), b, b.coordinates))

		# true_b.sort()

		# actualpointer=true_b[-1]

		# actualpointer[2]

		#img.dl().centeredRectangle(actualpointer[2], )


	
	only_pointer.show()
