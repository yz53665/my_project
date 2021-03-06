'''
实现基于边缘投影的特征提取
'''
import os

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

from MouseCatchTemplate import TemplateCatcher

imgNum = input('请输入检测图片的数量:')
methodNum = input('请输入检测函数编号（0-1）:')
methodNum = int(methodNum)
imgParDir = 'ExpPic/car/'
# imgParDir = 'ExpPic/plane'
imgDirList = []
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
           'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']


def Projection(img):
    projectX = np.sum(img, axis=0)
    projectY = np.sum(img, axis=1)
    return (projectX, projectY)


def MatchFuncs_1D(src, template, methodNum):
    fun = 0
    if methodNum == 0:
        # 最小均方误差函数(SQDIFF)
        fun = np.sum((src - template) ** 2)
    elif methodNum == 1:
        # 标准相关匹配(CCOEFF)
        template = template - np.sum(template) / len(template)
        src = src - np.sum(src) / len(src)
        fun = np.sum(template * src)
    return fun


def MatchTemplate(src, template, methodNum):
    w, h = template.shape[::-1]
    W, H = src.shape[::-1]
    mask = np.zeros([H - h + 1, W - w + 1])
    templateX, templateY = Projection(template)
    for i in range(H - h):
        for j in range(W - w):
            srcX, srcY = Projection(src[i:i+h, j:j+w])
            mask[i, j] = MatchFuncs_1D(srcX, templateX, methodNum) +\
                         MatchFuncs_1D(srcY, templateY, methodNum)
    return mask


for info in os.listdir(imgParDir):
    imgDirList.append(os.path.join(imgParDir, info))
imgDirList.sort()
imgDirList = imgDirList[0:int(imgNum)]

src = cv.imread(imgDirList[0])
catcher = TemplateCatcher()
catcher.catchTemplateFrom(src)
template = catcher.getTemplate()
mask = catcher.getMask()

# 获取模版的边缘
grayTemplate = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
cannyTemplate = cv.Canny(grayTemplate, 50, 150)
w, h = grayTemplate.shape[::-1]

templateX, templateY = Projection(cannyTemplate)
plt.title('模版沿x、y轴投影图')
plt.subplot(121)
plt.plot(list(range(len(templateX))), templateX.ravel())
plt.xlabel('x')
plt.subplot(122)
plt.plot(list(range(len(templateY))), templateY.ravel())
plt.xlabel('y')
plt.show()
for index, i in enumerate(imgDirList):
    img = cv.imread(i)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cannySrc = cv.Canny(gray, 50, 150)

    res = MatchTemplate(cannySrc, cannyTemplate, methodNum)
    cv.normalize(res, res, 0, 1, cv.NORM_MINMAX)
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(res)

    if methodNum == 0:
        topLeft = minLoc
    else:
        topLeft = maxLoc
    bottomRight = (topLeft[0] + w, topLeft[1] + h)

    cv.rectangle(img, topLeft, bottomRight, (0, 255, 0), 1)

    cv.imshow(i, img)
    cv.imwrite('project/img' + str(index) + '.png', img)
    cv.waitKey(500)
