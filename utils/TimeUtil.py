import datetime


class TimeUtil:
    @staticmethod
    def getMsTimeStr():
        """
        返回 时:分:秒.毫秒
        """
        time_now = datetime.datetime.now()
        time_now_str = time_now.strftime('%Y-%m-%d-%H:%M:%S')
        time_now_str = time_now_str.__add__(".").__add__(str(time_now.microsecond // 100000))
        return time_now_str

    @staticmethod
    def getYearDayTimeStr():
        time_now = datetime.datetime.now()
        time_now_str = time_now.strftime('%Y-%m-%d')
        return time_now_str

    @staticmethod
    def getYearHourTimeStr():
        time_now = datetime.datetime.now()
        time_now_str = time_now.strftime('%Y-%m-%d-%H')
        return time_now_str
