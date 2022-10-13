import math


class GnssUtil:
    R = 637100
    L = 2 * math.pi * R

    @staticmethod
    def ddmm2dd(x):
        degrees = int(x) // 100
        minutes = x - 100 * degrees
        return degrees + minutes / 60

    @staticmethod
    def latTrans(Latitude):
        """
        参考地址：https://blog.csdn.net/Dust_Evc/article/details/1
        02847870?utm_medium=distribute.pc_relevant.none-task-blog-2%7
        Edefault%7EBlogCommendFromBaidu%7Edefault-7.control&depth_
        1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault
        %7EBlogCommendFromBaidu%7Edefault-7.control
        度数与弧度转化公式：1°=π/180°，1rad=180°/π。
        地球半径：6371000M
        地球周长：2 * 6371000M  * π = 40030173
        纬度38°地球周长：40030173 * cos38 = 31544206M
        任意地球经度周长：40030173M
        经度（东西方向）1M实际度：360°/31544206M=1.141255544679108e-5=0.00001141
        纬度（南北方向）1M实际度：360°/40030173M=8.993216192195822e-6=0.00000899
        """
        Latitude = GnssUtil.ddmm2dd(Latitude)
        Lat_l = GnssUtil.L * math.cos(Latitude * math.pi / 180)  # 当前纬度地球周长，弧度转化为度数
        Lat_C = Lat_l / 360
        Latitude_m = Latitude * Lat_C
        return Latitude_m

    @staticmethod
    def lonTrans(Longitude):
        Longitude = GnssUtil.ddmm2dd(Longitude)
        Lng_l = 2 * GnssUtil.R * math.pi  # 当前经度地球周长
        Lng_C = Lng_l / 360
        Longitude_m = Longitude * Lng_C
        return Longitude_m

    @staticmethod
    def getGnssData(lon, lat):
        """
        :param lon: 经度
        :param lat: 纬度
        :return: uncompressed[0]表示经度，uncompressed[1]表示纬度
        """
        uncompressed = [[], []]
        for i in range(len(lon)):
            uncompressed[0].append(GnssUtil.ddmm2dd(lon[i]-lon[0]) * 1000000 * 0.111)
            uncompressed[1].append(GnssUtil.ddmm2dd(lat[i]-lat[0]) * 1000000 * 0.111)
        return uncompressed
