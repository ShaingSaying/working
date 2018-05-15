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


def KMeans(dataSet, k, disMeans=distEclud):
    m = np.shape(dataSet)[0]              # 这里第一列为类别，第二列为SSE
    clusterAssment = np.mat(zeros((m, 2)))   # m*2的矩阵
    # 看成一个簇是的质心
    centroids0 = mean(dataSet, axis=0).tolist()[0]       # 初始化k个中心
    centList = [centroids0]                              # create a list with one centroid
    for j in range(m):                       # 计算只有一个簇的误差
        clusterAssment[j, 1] = disMeans(mat(centroids0), dataSet[j, :])**2

    # 核心代码
    while (len(centList) < k):
        lowestSSE = inf
        # 对于每一个质心，尝试的进行划分
        for i in range(len(centList)):
            # 得到属于该质心的数据
            ptsInCurrClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0], :]
            # 对该质心划分为两类
            centroidMat, splitClustAss = KMeans(ptsInCurrClust, 2, disMeans)
            # 计算该簇划分后的SSE
            sseSplit = sum(splitClustAss[:, 1])
            # 没有参与划分的簇SSE
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != i)[0], 1])
            print("sseSplit, and notSplit: ", sseSplit, sseNotSplit)
            # 寻找最小的SSE进行划分
            # 即对哪一个簇进行划分后SSE最小
            bestCentToSplit = i
            bestNewCents = centroidMat
            bestClustAss = splitClustAss.copy()
            lowestSSE = sseSplit + sseNotSplit

            # 较难理解的部分
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)  # change 1 to 3,4, or whatever
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        print('the bestCentToSplit is: ', bestCentToSplit)
        print('the len of bestClustAss is: ', len(bestClustAss))
        centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]  # replace a centroid with two best centroids
        centList.append(bestNewCents[1, :].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0],
        :] = bestClustAss  # reassign new clusters, and SSE
    return mat(centList), clusterAssment


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