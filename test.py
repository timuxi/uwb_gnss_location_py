#! /usr/bin/env python
# -*- coding:utf-8 -*-
import json
import math
from datetime import datetime
from threading import Timer

import numpy as np
import serial

from mqtt.mqtt import MqttService
from utils.FileUtil import FileUtil
from utils.TimeUtil import TimeUtil


def testMqtt():
    mqtt = MqttService(on_connect_func=MqttService.mqttConnect)
    mqtt.MqttPublish(topic="test", payload=json.dumps("test"))


def fileWriteTest():
    fileUtil = FileUtil("./test", TimeUtil.getYearTimeStr() + ".txt")
    fileUtil.write(["123\n","123\n"])


if __name__ == '__main__':
    data = [[0.0, 0, 1],
            [1.0, 1, 1],
            [2.0, 0, 1],
            ]
    n = 3
    data = np.array(data)
    a = np.array(data[:, 0:2])
    print(a)
    f = np.linalg.inv(a.transpose().dot(a))

    x_v, y_v = 0, 0
    for i in range(n):
        x_v = x_v + data[i][0]
    x_v = x_v / n

    for i in range(n):
        y_v = y_v + data[i][1]
    y_v = y_v / n

    a_new = a
    a_new[:, 0] = a_new[:, 0] - x_v
    a_new[:, 1] = a_new[:, 1] - y_v
    print(a_new)

    f_new = np.linalg.inv(a_new.transpose().dot(a_new))

    res_x = 0.0
    res_y = 0.0
    for i in range(n):
        x_i = a_new[i][0]
        y_i = a_new[i][1]
        r_i = data[i][2]
        k_i = math.pow(x_i, 2) + math.pow(y_i, 2)
        res_x = res_x + (f_new[0][0]*x_i + f_new[0][1]*y_i) * (k_i-math.pow(r_i, 2))
        res_y = res_y + (f_new[1][0] * x_i + f_new[1][1] * y_i) * (k_i - math.pow(r_i, 2))
    res = [res_x/2 + x_v, res_y/2 + y_v]

    print(res)