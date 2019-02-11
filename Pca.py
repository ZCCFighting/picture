import cv2 as cv
import numpy as np
img=cv.imread('DJI_0024binary0.tif')
h, w, _ = img.shape
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, binary =  cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
image, contours, hierarchy = cv.findContours(binary,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
#cv.drawContour(image,contours,-1,(0,255,0),3)
def eigValPct(eigVals,percentage):
	sortArray=np.sort(eigVals) #使用numpy中的sort()对特征值按照从小到大排序
	sortArray=sortArray[-1::-1] #特征值从大到小排序
	arraySum=sum(sortArray) #数据全部的方差arraySum
	tempSum=0
	num=0
	for i in sortArray:
		tempSum+=i
		num+=1
		if tempSum>=arraySum*percentage:
			return num

'''pca函数有两个参数，其中dataMat是已经转换成矩阵matrix形式的数据集，列表示特征；
其中的percentage表示取前多少个特征需要达到的方差占比，默认为0.9'''
def pca(dataMat,percentage=0.9):
	#print(dataMat.shape)
	dataMat_re=np.reshape(dataMat,(-1,2))
	meanVals=np.mean(dataMat_re,axis=0)  #对每一列求平均值，因为协方差的计算中需要减去均值
	#print(meanVals)
	meanRemoved=dataMat_re-meanVals
	covMat=np.cov(meanRemoved)  #cov()计算方差
	eigVals,eigVects=np.linalg.eig(np.mat(covMat))  #利用numpy中寻找特征值和特征向量的模块linalg中的eig()方法
	k=eigValPct(eigVals,percentage) #要达到方差的百分比percentage，需要前k个向量
	eigValInd=np.argsort(eigVals)  #对特征值eigVals从小到大排序
	eigValInd=eigValInd[:-(k+1):-1] #从排好序的特征值，从后往前取k个，这样就实现了特征值的从大到小排列
	redEigVects=eigVects[:,eigValInd]
#返回排序后特征值对应的特征向量redEigVects（主成分）
	lowDDataMat=meanRemoved.T*redEigVects #将原始数据投影到主成分上得到新的低维数据lowDDataMat
	reconMat=(lowDDataMat*redEigVects.T).T+meanVals   #得到重构数据reconMat
	return lowDDataMat,reconMat
k=0
rec=[]
for i in range(len(contours)):
	cnt = contours[i]    
	area = cv.contourArea(cnt)     # 处理掉小的轮廓区域，这个区域的大小自己定义。    
	if(area <1e2 or 1e5 <area): continue        # thickness不为-1时，表示画轮廓线，thickness的值表示线的宽度。       
	cv.drawContours(img,contours,i,(255,0,0),2,8,hierarchy,0)
	lowDDataMat,reconMat=pca(contours[i],percentage=0.9)
	recon_mean=np.mean(reconMat,axis=0)
	print(recon_mean)
	rec.append(recon_mean)
	k+=1
#print(rec)
pos=np.mean(recon_mean)
#cv.circle(img,(a,b),3,(255,0,0),2,lineType=8,shift=0)
img=cv.line(img,(3210,1649),(1243,325),(0,0,255),2)
cv.imshow('img',img)
cv.imwrite('res.jpg',img)
cv.waitKey(1000)