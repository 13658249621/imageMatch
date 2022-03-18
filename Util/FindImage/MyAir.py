import cv2
import numpy as np
###寻找一个图片在另一个图片中的位置并返回坐标
def has_image(haystack, needle):
    haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
    needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
    w, h = needle.shape[::-1]
    res = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where(res >= threshold)
    print(loc)
    try:
        assert loc[0][0] > 0
        assert loc[1][0] > 0
        return (loc[1][0], loc[0][0])
    except:
        return (-1, -1)


if __name__ == "__main__":
    fruits = cv2.imread("/Users/timo/Downloads/Wechatbig.png")
    strawberry = cv2.imread("/Users/timo/Downloads/Wechatsmall.png")

    x, y = has_image(fruits, strawberry)
    print(x, y)
    if x >= 0 and y >= 0:
        w, h, _ = strawberry.shape
        cv2.imshow("Found the strawberry at (%d,%d)" % (x, y), fruits)
        cv2.rectangle(fruits, (x, y), (x + h, y + w), (255, 0, 0), 2)
        cv2.waitKey(0xFFFF)
    else:
        print("Not found")
