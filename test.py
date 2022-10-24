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
    mqtt = MqttService(on_connect_func=MqttService.mqttConnect)
    mqtt.MqttPublish(topic="uwb", payload="123")