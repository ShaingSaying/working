# dataSet样本点，k为簇的个数
# disMeans距离度量，默认为欧几里得距离
# createCent，初始点的选取

from numpy import *
import numpy as np
import matplotlib.pyplot as plt

def loadDataSet(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float, curLine))          # map all elements to float())
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))    # la.norm(vecA - vecB)

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k, n)))             # create centroid mat
    for j in range(n):                # create random cluster centers, within bounds of eac hdimension
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centroids[:, j] = mat(minJ + rangeJ * random.rand(k, 1))
    return centroids


def KMeans(dataSet, k, disMeans=distEclud, createCent=randCent):
    m = np.shape(dataSet)[0]              # 样本数
    clusterAssment = np.mat(zeros((m, 2)))   # m*2的矩阵
    centroids = createCent(dataSet, k)       # 初始化k个中心
    clusterChanged = True
    while clusterChanged:                    # 当聚类不再变化
        clusterChanged = False
        for i in range(m):
            minDist = inf; minIndex = -1
            for j in range(k):                # 找到最近的质心
                distJI = disMeans(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i, 0] != minIndex: clusterChanged = True
            # 第一列为所属质心，第二列为距离
            clusterAssment[i, :] = minIndex, minDist ** 2
        print(centroids)

        # 更改质心位置
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment


def draw(data, center):
    length = len(center)
    fig = plt.figure
    # 绘制原始数据的散点图
    plt.scatter(data[:, 0], data[:, 1], s=25, alpha=0.4)
    # 绘制图的质心点
    for i in range(length):
        plt.annotate('center', xy=(center[i, 1]), xytext=(center[i, 0] + 1, center[i, 1] + 1,
                     center[i, 1] + 1), arrowprops=dict(facecolor='red'))
    plt.show()