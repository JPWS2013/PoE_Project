from SimpleCV import *
import timeit

c=Camera()
data=[]
num=1000

for i in range(num):
    startTime=timeit.default_timer()
    img=c.getImage()
    elapsed=timeit.default_timer()-startTime

    data.append(elapsed)

total=sum(data)

print total/num
