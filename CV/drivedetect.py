import LaserDectFunct as ldf

point1=ldf.get_laser_pos()

while True:
	point1=ldf.get_laser_pos()
	point2=ldf.get_laser_pos()

	xval1, yval1=point1

	xval2, yval2=point2

	if xval1>xval2:
		print "I'm turning Left"

	if xval1<xval2:
		print "I'm turning Right"

	if yval1<yval2:
		print "I'm slowing down"

	if yval1>yval2:
		print "I'm speeding up"