import SimpleCV as cv
import sys

cam=cv.Camera(1)

ver1='n'
ver2='n'

while ver1.lower() != 'y':
	raw_input("About to take a picture of blank view.\nPlease ensure laser is not in view and hit enter when ready")

	nopointer=cam.getImage()

	nopointer.show()

	ver1=raw_input("Please verify this is a correct blank view. Enter 'y' to confirm or 'n' to end and restart: ")

while ver2.lower() != 'y':
	raw_input("About to take a picture of a view with the laser.\nPlease aim the laser in the center of the image as best as possible and hit enter")

	pointer=cam.getImage()

	pointer.show()

	ver2=raw_input("Please verify this is a correct blank view. Enter 'y' to confirm or 'n' to end and restart: ")


