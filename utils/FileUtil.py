import os.path
import string

import pandas


class FileUtil:
    @staticmethod
    def read_data(fileName, sep=" ", path='/Users/timuxi/PycharmProjects/mqtt/'):
        """
        _filename:   文件名
        """
        pathProject = path + fileName
        print('path: ' + pathProject)
        pd_read = pandas.read_table(pathProject, sep=sep, header=None)
        return pd_read

    @staticmethod
    def strSplit(datas, sep):
        """
        :param datas: 一维数据
        :param sep: 分隔符
        :return: 二维数组
        """
        res = []
        for data in datas:
            res.append(str(data).split(sep))
        return res

    def __init__(self, path: str, filename: str):
        if not path.endswith("/"):
            path = path.__add__("/")
        print("写入文件目录" + path + filename)
        # 目录不存在则创建目录
        if not os.path.exists(path):
            os.makedirs(path)
        self.filename = path + filename
        # 文件不存在则创建，存在则追加
        if not os.path.exists(self.filename):
            self.file = open(path + filename, "w")
        else:
            self.file = open(path + filename, "a")

    def write(self, content):
        self.file.writelines(content)

    def close(self):
        self.file.close()
