from SimpleCV import *
import timeit

c=Camera(1) #To avoid the onboard camera
data=[]
num=1000

# for i in range(num):
#     startTime=timeit.default_timer()
#     img=c.getImage()
#     elapsed=timeit.default_timer()-startTime

#     data.append(elapsed)

# total=sum(data)

# print total/num

while True:

    img=c.getImage()
    # img=img.binarize()
    # img.drawText("Hello World!")
    img.show()