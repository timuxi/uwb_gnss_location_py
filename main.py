
import json
import time

import numpy as np

from model.SensorData import SensorData
from mqtt.mqtt import MqttService
from utils.FileUtil import FileUtil
from utils.RepeatingTimer import RepeatingTimer
from utils.TimeUtil import TimeUtil
from utils.mySerial import mySerial

int_short = pow(2, 15)
uwb_btl = 115200
uwb_port = '/dev/ttyUSBuwb'

imu_btl = 9600
imu_port = '/dev/ttyUSBuwb'
accByteSend = [
    0x50,
    0x03,
    0x00,
    0x34,
    0x00,
    0x0C,
    0X09,
    0X80
]

gps_btl = 115200
gps_port = '/dev/ttyUSBgps'

filepath = "./sensorData/"
file_now_time = TimeUtil.getYearHourTimeStr()
cnt = 0
sensorData = SensorData()
fileUtil = FileUtil(filepath + TimeUtil.getYearDayTimeStr(), file_now_time + ".txt")


def short(_data):
    if _data >= int_short:
        _data = _data - 2 * int_short
    return _data


def parseData(chrBuf):
    sData = np.zeros(12,dtype=int)
    acc = np.zeros(3)
    w = np.zeros(3)
    angle = np.zeros(3)
    if len(chrBuf) != 29:
        return
    if (chrBuf[0] != 0x50) or (chrBuf[1] != 0x03):
        return
    for i in range(12):
        sData[i] = short((chrBuf[3 + i * 2] << 8) | chrBuf[4 + i * 2])
    for i in range(3):
        acc[i] = sData[i] / 32768.0 * 16.0
        w[i] = sData[3 + i] / 32768.0 * 2000.0
        angle[i] = sData[9 + i] / 32768.0 * 180.0
    return str(acc[0]).__add__(",").__add__(str(acc[1])).__add__(",").__add__(str(acc[2])).__add__(",")\
        .__add__(str(w[0])).__add__(",").__add__(str(w[1])).__add__(",").__add__(str(w[2])).__add__(",")\
        .__add__(str(angle[0])).__add__(",").__add__(str(angle[1])).__add__(",").__add__(str(angle[2]))


def readData(_gpsSerial: mySerial, _imuSerial: mySerial, mqtt: MqttService):
    global file_now_time, cnt, fileUtil
    if len(sensorData.msTimeList) >= 1 * 10:
        # mqtt发布数据
        sensorJson = json.dumps({
            "time": sensorData.msTimeList,
            "gnssData": sensorData.gnssDataList,
            "imuData": sensorData.imuDataList,
        })
        mqtt.MqttPublish(topic="uwb", payload=sensorJson)
        print("data publish")
        # 写入本地文件
        if TimeUtil.getYearHourTimeStr() != file_now_time:
            file_now_time = TimeUtil.getYearHourTimeStr()
            fileUtil = FileUtil(path=filepath + TimeUtil.getYearDayTimeStr(), filename=file_now_time+".txt")
        for i in range(len(sensorData.msTimeList)):
            fileUtil.write(str(sensorData.msTimeList[i])+","
                           + str(sensorData.gnssDataList[i])+","
                           + str(sensorData.imuDataList[i])+"\n")
        # 数据重置
        sensorData.reset()
    # 读取数据
    if _imuSerial.ser.in_waiting:
        imu_msg = parseData(_imuSerial.ser.readall())
        _imuSerial.ser.write(accByteSend)
        if _gpsSerial.ser.in_waiting:
            ms_time = TimeUtil.getMsTimeStr()
            gps_msg = _gpsSerial.ser.readline().decode('utf-8').strip('\n').strip('\r')
            sensorData.writeData(ms_time=ms_time, gps_msg=gps_msg, imu_msg=str(imu_msg))


def mqttPublish():
    mqtt = MqttService(on_connect_func=MqttService.mqttConnect)
    gpsSerial = mySerial(port=gps_port, btl=gps_btl)
    imuSerial = mySerial(port=imu_port, btl=imu_btl)
    imuSerial.ser.write(accByteSend)
    time.sleep(0.1)
    RepeatingTimer(0.1, readData, (gpsSerial, imuSerial, mqtt)).start()


if __name__ == '__main__':
    mqttPublish()

