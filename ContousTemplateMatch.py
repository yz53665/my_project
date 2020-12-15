from MouseCatchTemplate import catchtemplate
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import os

imgNum = input('请输入检测图片的数量：')
methodNum = input('请输入检测函数编号（0-5）:')
methodNum = int(methodNum)
imgParDir = 'ExpPic/car/'
#imgParDir = 'ExpPic/plane'
imgDirList = []
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

def SobelNormalize(img):
    dx = cv.Sobel(img, cv.CV_32F, 1, 0, 1)
    dy = cv.Sobel(img, cv.CV_32F, 0, 1, 1)
    dx = cv.convertScaleAbs(dx)
    dy = cv.convertScaleAbs(dy)
    dxy = cv.addWeighted(dx, 0.5, dy, 0.5, 0, dtype=cv.CV_32F)
    return dxy

for info in os.listdir(imgParDir):
    imgDirList.append(os.path.join(imgParDir, info))
imgDirList.sort()

src = cv.imread(imgDirList[0])
# template = catchtemplate(src)
template = cv.imread('template.png')
sobelTemplate = SobelNormalize(template)

# 获取模版的边缘
grayTemplate = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
templateDxy = SobelNormalize(grayTemplate)

for i in imgDirList:
    img = cv.imread(i)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    dxy = SobelNormalize(gray)
    
    print(dxy.dtype)
    print(sobelTemplate.dtype)
    res = cv.matchTemplate(dxy, templateDxy, eval(methods[methodNum]))
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(res)

    if methods[methodNum] in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        topLeft = minLoc
    else:
        topLeft = maxLoc
    w, h = grayTemplate.shape[::-1]
    bottomRight = (topLeft[0] + w, topLeft[1] + h)

    cv.rectangle(img, topLeft, bottomRight, (0, 255, 0), 1)
   
    cv.namedWindow('grey')
    cv.imshow('grey', res)
    cv.namedWindow(i)
    cv.imshow(i, img)
    cv.waitKey(0)

