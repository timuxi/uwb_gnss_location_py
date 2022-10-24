#! /usr/bin/env python
# -*- coding:utf-8 -*-
import configparser

import paho.mqtt.client as mqtt


class MqttService:
    """
    on_connect_func:连接MQTT回调函数,订阅主题时触发
    """

    def __init__(self, on_connect_func=None):
        self.config = configparser.ConfigParser()
        self.host = None
        self.port = 1883
        self.keepalive = 60
        self.name = None
        self.pwd = None
        self.mqtt_info = None
        self.InitMqtt(on_connect_func)


    """
    初始化MQTT配置信息
    """

    def InitMqtt(self, on_connect_func=None):
        self.config.read("./mqtt/mqttConfig.ini", encoding="gbk")
        self.host = self.config.get("MqttInfo", "Host")
        self.port = self.config.get("MqttInfo", "Port")
        self.keepalive = self.config.get("MqttInfo", "Keepalive")
        self.name = self.config.get("MqttInfo", "Name")
        self.pwd = self.config.get("MqttInfo", "Pwd")
        self.mqtt_info = mqtt.Client(protocol=3)
        self.mqtt_info.on_connect = on_connect_func
        self.mqtt_info.username_pw_set(self.name, self.pwd)
        self.mqtt_info.connect(host=self.host, port=int(self.port), keepalive=int(self.keepalive))
        self.mqtt_info.loop_start()

    """
    发布消息
    topic:主题
    payload:发布的数据
    qos:模式
    """

    def MqttPublish(self, topic=None, payload=None, qos=1):
        if topic is None or payload is None:
            return None
        self.mqtt_info.publish(topic=topic, payload=payload, qos=qos)

    """
    订阅消息
    topic:主题
    qos:模式
    msg_func:接收数据回调
    on_subscribe_func:订阅回调
    """

    @staticmethod
    def MqttSubscribe(self, topic=None, qos=1, msg_func=None, on_subscribe_func=None):
        if topic is None:
            return None
        self.mqtt_info.subscribe(topic, qos)
        self.mqtt_info.on_message = msg_func
        self.mqtt_info.on_subscribe = on_subscribe_func
        self.mqtt_info.loop_forever()

    @staticmethod
    def mqttMessage(client, userdata, msg):
        print("订阅的数据:" + msg.payload.decode('utf-8'))

    @staticmethod
    def mqttConnect(client, userdata, flags, rc):
        print("连接成功：" + str(rc))

    @staticmethod
    def mqttSubscribe(client, userdata, mid, granted_qos):
        print("消息订阅成功")

    @staticmethod
    def dataProcess(msg):
        return int(msg[msg.find(":") + 1: len(msg) - 4])