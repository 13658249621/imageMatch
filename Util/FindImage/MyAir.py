import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('/Users/timo/Downloads/hotelMain.jpeg', 0)
img2 = img.copy()
template = cv.imread('/Users/timo/Downloads/签到领红包.png', 0)
w, h = template.shape[::-1]
# 列表中所有的6种比较方法
methods = ['cv.TM_CCOEFF']
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # 应用模板匹配
    res = cv.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # 如果方法是TM_SQDIFF或TM_SQDIFF_NORMED，则取最小值
    if method in [cv.TM_CCOEFF]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img, top_left, bottom_right, 255, 2)
    cv.imshow('Rainforest', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
