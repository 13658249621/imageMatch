import sys
import cv2
"""图像识别服务本地调用文件"""

def feature_matching(templatePicPath, targetPicPath):
    tem = cv2.imread(templatePicPath)
    tar = cv2.imread(targetPicPath)

    # 创建特征检测器——用于检测模板和图像上的获取图像特征的关键点和描述符
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(tem, None)
    kp2, des2 = sift.detectAndCompute(tar, None)
    """
    获取图片的长，宽
    img.shape[:2]
    取彩色图片的长、宽
    img.shape[:3]
    取彩色图片的长、宽、通道
    img.shape[0]
    图像的垂直尺寸（高度）
    img.shape[1]
    图像的水平尺寸（宽度）
    img.shape[2]
    图像的通道数
    """
    height1, width2 = tem.shape[:2]

    """
    定义FLANN匹配器
    indexParams:配置我们要使用的算法Randomized k-d tree,增加树的数量能加快搜索速度，但由于内存负载的问题，树的数量只能控制在一定范围内，比如20，如果超过一定范围，那么搜索速度不会增加甚至会减慢
    SearchParams：指定递归遍历的次数,值越高结果越准确，但是消耗的时间也越多
    """
    indexParams = dict(algorithm=0, trees=10)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)
    # 使用KNN算法实现图像匹配，返回最佳的k个匹配,KnnMatch与match的返回值类型一样，只不过一组返回的俩个DMatch类型：
    matches = flann.knnMatch(des1, des2, k=2)
    # matches是DMatch对象，具有以下属性：
    # DMatch.distance - 描述符之间的距离。 越低越好。
    # DMatch.trainIdx - 训练描述符中描述符的索引
    # DMatch.queryIdx - 查询描述符中描述符的索引
    # DMatch.imgIdx - 训练图像的索引。

    """
    去除错误匹配，0.5是系数，系数大小不同，匹配的结果页不同
    distance:代表匹配的特征点描述符的欧式距离，数值越小也就说明俩个特征点越相近
    """
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


if __name__ == "__main__":
    # 数组第一个是py文件路径，所以下表从1开始，取传入的参数
    res = feature_matching(sys.argv[1], sys.argv[2])
    print(res)
