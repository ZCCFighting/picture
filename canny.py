import cv2
import numpy as np 
import random
img=cv2.imread('DJI_0059.JPG',1)
imgInfo=img.shape
height=imgInfo[0]
width=imgInfo[1]
#cv2.imshow('src',img)
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgG=cv2.GaussianBlur(gray,(3,3),0)
dst=cv2.Canny(img,3,3)
kernel = np.ones((3,3),np.uint8)

cv2.imshow('dst',dst)
erosion = cv2.erode(dst,kernel,iterations = 1)
dilation = cv2.dilate(dst,kernel,iterations = 1)
cv2.imwrite('erosion.tif',erosion)
cv2.imwrite('dilation.tif',dilation)
opening = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)

#cv2.imwrite('result2.tif',opening)
cv2.imwrite('result3.tif',closing)
cv2.waitKey(1000)