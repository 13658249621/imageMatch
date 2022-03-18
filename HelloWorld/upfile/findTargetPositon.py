import cv2


# 成功过获取了元素中心点坐标
def get_target_rectangle(left_top_pos, w, h):
    """根据左上角点和宽高求出目标区域."""
    x_min, y_min = left_top_pos
    # 中心位置的坐标:
    x_middle, y_middle = int(x_min + w / 2), int(y_min + h / 2)
    # 左下(min,max)->右下(max,max)->右上(max,min)
    left_bottom_pos, right_bottom_pos = (x_min, y_min + h), (x_min + w, y_min + h)
    right_top_pos = (x_min + w, y_min)
    # 点击位置:
    middle_point = (x_middle, y_middle)
    # 识别目标区域: 点序:左上->左下->右下->右上, 左上(min,min)右下(max,max)
    rectangle = (left_top_pos, left_bottom_pos, right_bottom_pos, right_top_pos)
    return middle_point, rectangle


def getTargetPositon(templatePicPath, targetPicPath):
    template = cv2.imread(templatePicPath)
    gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    targetPic = cv2.imread(targetPicPath, 0)

    result = cv2.matchTemplate(gray, targetPic, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    height, width = targetPic.shape[:2]
    top_left = max_loc
    middle_point, rectangle = get_target_rectangle(top_left, height, width)
    print(middle_point)
    # bottom_right = (top_left[0] + width, top_left[1] + height)
    # cv2.rectangle(template, top_left, bottom_right, (0, 0, 255), 5)
    #
    # cv2.imshow('Rainforest', template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


templatePicPath = '/Users/timo/PycharmProjects/AirTest/HelloWorld/media/template.png'
targetPicPath = '/Users/timo/PycharmProjects/AirTest/HelloWorld/media/target.png'
getTargetPositon(templatePicPath, targetPicPath)

# image = cv2.imread('/Users/timo/Downloads/1.jpeg')
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# template = cv2.imread('/Users/timo/Downloads/2.jpeg', 0)
#
# result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
# height, width = template.shape[:2]
# top_left = max_loc
# middle_point, rectangle=get_target_rectangle(top_left,height,width)
# print(middle_point)
# bottom_right = (top_left[0] + width, top_left[1] + height)
# cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 5)
#
# cv2.imshow('Rainforest', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()