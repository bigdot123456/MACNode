# # encoding:utf-8
# 用python3生成纯色图像

import cv2
import numpy
#全黑的灰度图
gray0=numpy.zeros((500,500),dtype=numpy.uint8)
cv2.imshow('0',gray0)
#全白的灰度图
gray0[:,:]=255
gray255=gray0[:,:]
cv2.imshow('255',gray255)
#将灰度图转换成彩色图
Img_rgb=cv2.cvtColor(gray255,cv2.COLOR_GRAY2RGB)
#将RGB通道全部置成0
Img_rgb[:,:,0:3]=0
cv2.imshow('(0,0,0)',Img_rgb)
#将RGB通道全部置成255
Img_rgb[:,:,0:3]=255
cv2.imshow('(255,255,255)',Img_rgb)
cv2.waitKey(0)
