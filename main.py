import datetime
import json

from mqtt.mqtt import MqttService
from utils.FileUtil import FileUtil
from utils.RepeatingTimer import RepeatingTimer
from utils.TimeUtil import TimeUtil
from utils.mySerial import mySerial

uwb_btl = 115200
uwb_port = '/dev/ttyUSBuwb'

gps_btl = 115200
gps_port = '/dev/ttyUSBgps'
dataList = []


def readData(_gpsSerial: mySerial, _uwbSerial: mySerial, mqtt: MqttService, file: FileUtil):
    global dataList
    # 存储一分钟数据后发布到服务器
    if len(dataList) >= 5 * 10:
        mqtt.MqttPublish(topic="uwb", payload=json.dumps(dataList))
        file.write(dataList)
        print("data publish")
        dataList = []

    if _gpsSerial.ser.in_waiting:
        gps_msg = _gpsSerial.ser.readline()
        if _uwbSerial.ser.in_waiting:
            TimeUtil.getMsTimeStr()
            uwb_msg = _uwbSerial.ser.readline()
            data = TimeUtil.getMsTimeStr() \
                .__add__(",").__add__(gps_msg.decode('utf-8').strip('\n').strip('\r')) \
                .__add__(",").__add__(uwb_msg.decode('utf-8'))
            if len(data) > 120:
                print("error")
            else:
                print(data)
                dataList.append(data)


def damon1():
    mqtt = MqttService(on_connect_func=MqttService.mqttConnect)
    gpsSerial = mySerial(port=gps_port, btl=gps_btl)
    uwbSerial = mySerial(port=uwb_port, btl=gps_btl)
    fileUtil = FileUtil("./uwbData", TimeUtil.getYearTimeStr()+".txt")
    RepeatingTimer(0.1, readData, (gpsSerial, uwbSerial, mqtt, fileUtil)).start()


def damon2():
    uwbSerial = mySerial(port=uwb_port, btl=gps_btl)
    while True:
        if uwbSerial.ser.in_waiting:
            uwb_msg = uwbSerial.ser.read_all()
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%01f')
            print(dt_ms, uwb_msg)


if __name__ == '__main__':
    damon1()
