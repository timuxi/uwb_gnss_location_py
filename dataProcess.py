
import turtle
import matplotlib.pyplot as plt
import numpy as np

from tdoa import TDOA
from utils.PltUtil import PltUtil
from utils.FileUtil import FileUtil
from utils.GnssUtil import GnssUtil


def damon1(split=10):
    gt = FileUtil.read_data(fileName="data/gps_2022-10-10 14:16:8.txt", sep=",")
    gt = GnssUtil.getGnssData(lon=gt[2], lat=gt[4])
    dis = FileUtil.read_data(fileName="data/uwb_2022-10-10 14:16:8.txt", sep=",")
    dis = FileUtil.strSplit(dis[0], " ")
    cnt = 0
    for i in range(len(dis)):
        if cnt % split == 0:
            PltUtil.pltCircle(gt[0][i], gt[1][i], float(dis[i][1]) * 0.01)
        cnt = cnt + 1
    plt.plot(gt[0], gt[1], color='b')

    temp = FileUtil.read_data(fileName="data/gps_2022-10-10 14:15:0.txt", sep=",")
    temp = GnssUtil.getGnssData(lon=temp[2], lat=temp[4])
    plt.plot(temp[0], temp[1], color='r')
    plt.xlabel("lon(m)")
    plt.ylabel("lan(m)")
    plt.show()

def demon2():
    gps = FileUtil.read_data(fileName="data/gps_2022-10-10 14:16:8.txt", sep=",")
    gps = GnssUtil.getGnssData(lon=gps[2], lat=gps[4])
    dis = FileUtil.read_data(fileName="data/uwb_2022-10-10 14:16:8.txt", sep=",")
    dis = FileUtil.strSplit(dis[0], " ")
    num = 25
    data = []
    for i in range(num):
        data.append([])
    for j in range(0, 500, num):
        index = 0
        for i in range(j, j+num):
            if i%5 ==0:
                PltUtil.pltCircle(gps[0][i], gps[1][i], float(dis[i][1]) * 0.01)
            data[index].append(gps[0][i])
            data[index].append(gps[1][i])
            data[index].append(float(dis[i][1]) * 0.01)
            index = index + 1
        # res = TDOA().compute(data[0], data[1], data[2])
        res = TDOA.oneStep(data, num)
        PltUtil.pltCircle(res[0], res[1], 0.01, color='r')
        data = []
        for i in range(num):
            data.append([])
    plt.show()

def demon3():
    gps = FileUtil.read_data(fileName="data/gps_2022-10-10 14:16:8.txt", sep=",")
    gps = GnssUtil.getGnssData(lon=gps[2], lat=gps[4])
    dis = FileUtil.read_data(fileName="data/uwb_2022-10-10 14:16:8.txt", sep=",")
    dis = FileUtil.strSplit(dis[0], " ")
    num = 3
    data = []
    for i in range(num):
        data.append([])
    for j in range(0, 500, 30):
        index = 0
        for i in range(j, j+30,10):
            if i%5 ==0:
                PltUtil.pltCircle(gps[0][i], gps[1][i], float(dis[i][1]) * 0.01)
            data[index].append(gps[0][i])
            data[index].append(gps[1][i])
            data[index].append(float(dis[i][1]) * 0.01)
            index = index + 1
        res = TDOA().compute(data[0], data[1], data[2])
        PltUtil.pltCircle(res[0], res[1], 0.01, color='r')
        data = []
        for i in range(num):
            data.append([])
    plt.show()


if __name__ == '__main__':
    damon1()