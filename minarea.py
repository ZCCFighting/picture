import cv2 as cv
import numpy as np
import math 
img=cv.imread('fff.JPG')
sp=img.shape
h=sp[0]
w=sp[1]
print(h)
print(w)
ws=5
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    #直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
image_median=cv.medianBlur(binary,7)
kernel = np.ones((7,7),np.uint8)
dilation = cv.dilate(image_median,kernel,iterations = 1)
#cv.imshow('img1',dilation)
image, contours, hierarchy = cv.findContours(dilation,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
#cv.imshow('img',image)
for i in range(len(contours)):
	area = cv.contourArea(contours[i])     # 处理掉小的轮廓区域，这个区域的大小自己定义。    
	if(area <5000): continue
	triangle=cv.minEnclosingTriangle(contours[i])
	points=triangle[1].reshape(3,2) #trinagle[1] 三个顶点的坐标 3,1,2的数组
	print(points)
	for j in range(3):
		img=cv.line(img,(points[j][0],points[j][1]),(points[(j+1)%3][0],points[(j+1)%3][1]),(255,0,0),2)
	longth=[]
	angles=0
	for k in range(3):
		longth.append(math.sqrt((points[k][0]-points[(k+1)%3][0])*(points[k][0]-points[(k+1)%3][0])+(points[k][1]-points[(k+1)%3][1])*(points[k][1]-points[(k+1)%3][1])))
	index=0
	if (longth[0]>longth[1]):
		if(longth[0]>longth[2]):
			index=0
		else:
			index=2
	else:
		if(longth[1]>longth[2]):
			index=1
		else:
			index=2
	results=((points[(index+2)%3][0]-points[(index+1)%3][0])*(points[index][1]-points[(index+1)%3][1]))/(points[index][0]-points[(index+1)%3][0])+points[(index+1)%3][1]
	angles=(points[index %3 ][1]-points[(index+1)%3][1])/(points[index %3 ][0]-points[(index+1)%3][0])
	angle=math.atan(angles)
	angle=angle*180/math.pi
	if(results<0):
		angle=180-angle
	print(angle)
	agl=str(angle)
	a=(w//2-ws,h//2)
	cv.putText(img,agl,a,cv.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),2)
#cv.namedWindow("result", cv.WINDOW_NORMAL)
cv.imshow("res", img)
cv.imwrite('result.jpg',img)
cv.waitKey(0)
#cv.imwrite(filena+'binary0.tif',binary)