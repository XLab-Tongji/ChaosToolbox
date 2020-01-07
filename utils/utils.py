import time
import datetime


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def datetime_timestamp(dt):
        time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return int(s)

    @staticmethod
    def timestamp_datetime(ts):
        dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return dt
