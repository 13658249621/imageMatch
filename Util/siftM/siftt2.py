import cv2 as cv

# 初步成功，缺少坐标提取
tem = cv.imread("/Users/timo/Downloads/hotelMain.jpeg");
tar = cv.imread("/Users/timo/Downloads/chosemudidi.png");
cv.imshow("tem", tem)
cv.imshow("tar", tar)

sift = cv.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(tem, None)
kp2, des2 = sift.detectAndCompute(tar, None)

index_params = dict(algorithm=0, trees=5)

search_params = dict(checks=20)

flann = cv.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k=2)

# 记录好的点
goodMatches = [[0, 0] for i in range(len(matches))]

for i, (m, n) in enumerate(matches):
    if m.distance < 0.2 * n.distance:
        goodMatches[i] = [1, 0]

draw_params = dict(matchColor=(0, 255, 0), singlePointColor=(255, 0, 0), matchesMask=goodMatches, flags=0)
result = cv.drawMatchesKnn(tem, kp1, tar, kp2, matches, None, **draw_params)


cv.imshow("orb-match", result)
cv.waitKey(0)
cv.destroyAllWindows()
