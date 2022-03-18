from django.http import HttpResponse
from django.shortcuts import render
import os
import cv2


def index_view(request):
    BASE_PIC_DIR = '/Users/timo/PycharmProjects/AirTest/HelloWorld/media/'
    picNameArray = ['template.png', 'target.png']
    if request.method == 'GET':
        return render(request, 'up.html')
    elif request.method == "POST":
        m_dict = request.FILES
        k = 0
        """
        遍历文件列表，读取文件存放本地
        """
        for i in m_dict.values():
            i.name = picNameArray[k]
            with open(os.path.join(os.getcwd(), 'media', i.name), 'wb') as fw:
                # 一次性读取文件
                fw.write(i.read())
                # 分块读取文件
                # for w in i.chunks():
                #     fw.write(w)
            k = k + 1
        """
        调用特征点匹配和模板匹配方法，寻找目标元素中心坐标
        """
        try:
            fea_pos = feature_matching(BASE_PIC_DIR + picNameArray[0], BASE_PIC_DIR + picNameArray[1])
            if fea_pos is not None:
                response = response_format(0, "成功", fea_pos)
                return HttpResponse(response)
            else:
                fea_pos = template_matching(BASE_PIC_DIR + picNameArray[0], BASE_PIC_DIR + picNameArray[1])
        except BaseException as err:
            response = response_format(3001, "图像匹配异常", fea_pos)
            return response

    else:
        return HttpResponse('访问失败')


"""
计算模板匹配结果中心坐标,根据左上角点和宽高求出目标区域.
"""


def get_target_rectangle(left_top_pos, w, h):
    x_min, y_min = left_top_pos
    # 中心位置的坐标:
    x_middle, y_middle = int(x_min + w / 2), int(y_min + h / 2)
    # 左下(min,max)->右下(max,max)->右上(max,min)
    left_bottom_pos, right_bottom_pos = (x_min, y_min + h), (x_min + w, y_min + h)
    right_top_pos = (x_min + w, y_min)
    # 点击位置:
    middle_point = [x_middle, y_middle]
    # 识别目标区域: 点序:左上->左下->右下->右上, 左上(min,min)右下(max,max)
    rectangle = (left_top_pos, left_bottom_pos, right_bottom_pos, right_top_pos)
    return middle_point, rectangle


"""
模板匹配
"""


def template_matching(templatePicPath, targetPicPath):
    template = cv2.imread(templatePicPath)
    gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    targetPic = cv2.imread(targetPicPath, 0)

    result = cv2.matchTemplate(gray, targetPic, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    height, width = targetPic.shape[:2]
    top_left = max_loc
    middle_point, rectangle = get_target_rectangle(top_left, height, width)
    print(middle_point)
    return middle_point


"""
特征点匹配并返回匹配结果坐标
"""


def feature_matching(templatePicPath, targetPicPath):
    tem = cv2.imread(templatePicPath)
    tar = cv2.imread(targetPicPath)

    # 使用SIFT算法获取图像特征的关键点和描述符
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(tem, None)
    kp2, des2 = sift.detectAndCompute(tar, None)

    height1, width2 = tem.shape[:2]
    print(height1, width2)

    # 定义FLANN匹配器
    indexParams = dict(algorithm=0, trees=10)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)
    # 使用KNN算法实现图像匹配，并对匹配结果排序
    matches = flann.knnMatch(des1, des2, k=2)
    matches = sorted(matches, key=lambda x: x[0].distance)

    # 去除错误匹配，0.5是系数，系数大小不同，匹配的结果页不同
    goodMatches = []
    for m, n in matches:
        if m.distance < 0.25 * n.distance:
            goodMatches.append(m)

    # 获取某个点的坐标位置
    # index是获取匹配结果的中位数
    index = int(len(goodMatches) / 2)
    # queryIdx是目标图像的描述符索引
    x, y = kp1[goodMatches[index].queryIdx].pt
    return [int(x), int(y)]


def response_format(errorCode, errorMessage, pos):
    res = {"errorCode": errorCode, "errorMessage": errorMessage, "pos": pos}
    return str(res)
