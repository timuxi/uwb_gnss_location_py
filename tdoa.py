import numpy as np
import math
import matplotlib.pyplot as plt
from numpy import linalg, double


class TDOA:
    def __init__(self):
        self.r3 = None
        self.y3 = None
        self.x3 = None
        self.r2 = None
        self.y2 = None
        self.x2 = None
        self.y1 = None
        self.r1 = None
        self.x1 = None

    def compute(self, data1, data2, data3):
        self.x1 = data1[0]
        self.y1 = data1[1]
        self.r1 = data1[2]

        self.x2 = data2[0]
        self.y2 = data2[1]
        self.r2 = data2[2]

        self.x3 = data3[0]
        self.y3 = data3[1]
        self.r3 = data3[2]
        r21 = self.r2 - self.r1
        r31 = self.r3 - self.r1
        x21 = self.x2 - self.x1
        x31 = self.x3 - self.x1
        y21 = self.y2 - self.y1
        y31 = self.y3 - self.y1
        P1_tmp = np.array([[x21, y21], [x31, y31]])
        print(P1_tmp+np.array([1e-6]))
        P1 = (-1) * np.linalg.inv(P1_tmp)
        P2 = np.array([[r21], [r31]])
        K1 = self.x1 * self.x1 + self.y1 * self.y1
        K2 = self.x2 * self.x2 + self.y2 * self.y2
        K3 = self.x3 * self.x3 + self.y3 * self.y3
        P3 = np.array([[(-K2 + K1 + r21 * r21) / 2], [(-K3 + K1 + r31 * r31) / 2]])
        res = (np.dot(P1, P2)) * self.r1 + np.dot(P1, P3)
        return res

    @staticmethod
    def oneStep(data, n: int):
        data = np.array(data)
        a = np.array(data[:, 0:2])

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

        f_new = np.linalg.inv(a_new.transpose().dot(a_new))

        res_x = 0.0
        res_y = 0.0
        for i in range(n):
            x_i = a_new[i][0]
            y_i = a_new[i][1]
            r_i = data[i][2]
            k_i = math.pow(x_i, 2) + math.pow(y_i, 2)
            res_x = res_x + (f_new[0][0] * x_i + f_new[0][1] * y_i) * (k_i - math.pow(r_i, 2))
            res_y = res_y + (f_new[1][0] * x_i + f_new[1][1] * y_i) * (k_i - math.pow(r_i, 2))
        res = [res_x / 2 + x_v, res_y / 2 + y_v]
        return res




