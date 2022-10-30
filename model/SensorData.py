import json
import string

import numpy as np


class SensorData(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(SensorData, self).default(obj)

    def __init__(self):
        self.msTimeList = []
        self.gnssDataList = []
        self.imuDataList = []

    def writeData(self, ms_time: string, gps_msg:string, imu_msg:string):
        self.msTimeList.append(ms_time)
        self.gnssDataList.append(gps_msg)
        self.imuDataList.append(imu_msg)

    def reset(self):
        self.msTimeList = []
        self.gnssDataList = []
        self.imuDataList = []


