# -*- coding: utf-8 -*-

"""
#时间管理器
Created on 2014-07-21
@author: Linwencai
"""

import datetime
import time

DEF_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def GetNowDatetime():
    """获取当前的时间
    """
    return datetime.datetime.today()


def GetNowInttime():
    """获取当前的时间戳
    """
    return int(time.time())


def DateToStrtime(curDatetime, timeFormat=DEF_TIME_FORMAT):
    """datetime转格式化字符串
    """
    return curDatetime.strftime(timeFormat)


def StrToDatetime(strDatetime, timeFormat=DEF_TIME_FORMAT):
    """格式化字符串转datetime
    """
    return datetime.datetime.strptime(strDatetime, timeFormat)


def DateToInttime(curDatetime):
    """datetime转时间戳
    """
    return time.mktime(curDatetime.timetuple())


def IntToDatetime(intTime):
    """时间戳转datetime
    """
    return datetime.datetime.fromtimestamp(intTime)


def GetFutureDatetime(secound, curDatetime=None):
    """获取secound秒后的datetime
    """
    if not curDatetime:
        curDatetime = GetNowDatetime()
    delayTime = datetime.timedelta(seconds=secound)
    return delayTime + curDatetime


def GetPassSecound(strDatetime, endDatetime=None):
    """获取时间间隔秒
    @return float（ >0 if endDatetime>strDatetime else <=0)
    """
    if not endDatetime:
        endDatetime = GetNowDatetime()
    intervalDatetime = endDatetime - strDatetime
    return intervalDatetime.total_seconds()


def GetPassDay(strDatetime, endDatetime):
    """获取日期间隔天数（忽略小时，不是时间的间隔天数）
    @return int ( >0 if endDatetime>strDatetime else <=0)
    """
    strDate = strDatetime.date()
    endDate = endDatetime.date()
    return (endDate - strDate).days


def IsInTime(strDatetime, endDatetime, inDatetime):
    """判断某个时间是否在一个时间段里面
    @param strDatetime:
    @param endDatetime:
    @param inDatetime:
    @return:
    """
    timedelta = strDatetime - endDatetime
    if timedelta.total_seconds() > 0:
        strDatetime, endDatetime = endDatetime, strDatetime
    strTimedelta = strDatetime - inDatetime
    endTimedelta = inDatetime - endDatetime
    return strTimedelta.total_seconds() <= 0 and endTimedelta.total_seconds() <= 0

# def IsInTime2(strDatetime, endDatetime, inDatetime):
#     """判断某个时间是否在一个时间段里面
#     @param strDatetime:
#     @param endDatetime:
#     @param inDatetime:
#     @return:
#     """
#     strDatetime = time.mktime(strDatetime.timetuple())
#     endDatetime = time.mktime(endDatetime.timetuple())
#     inDatetime = time.mktime(inDatetime.timetuple())
#     if strDatetime > endDatetime:
#         strDatetime, endDatetime = endDatetime, strDatetime
#     return strDatetime <= inDatetime <= endDatetime

# def compare_time(l_time, start_t, end_t):
#     s_time = time.mktime(time.strptime(start_t, '%Y%m%d%H%M'))
#     e_time = time.mktime(time.strptime(end_t, '%Y%m%d%H%M'))
#     log_time = time.mktime(time.strptime(l_time, '%Y-%m-%d %H:%M:%S'))
#     return (float(log_time) >= float(s_time)) and (float(log_time) <= float(e_time))


if __name__ == "__main__":
    pass
##    i = DateToInttime(GetNowDatetime())
##    print i
##    d = IntToDatetime(i)
##    print d
##    print GetNowDateTime()
##    print GetNowIntTime()
##    print DateToIntTime(time.time())

##    now = GetNowDatetime()
##    future = GetFutureDatetime(10)
##    print now
##    print future
##    print GetPassSecound(now, future)

##    d1 = datetime.datetime(2017, 04, 05, 17, 40, 0)
##    d2 = datetime.datetime(2017, 04, 06, 17, 40, 0)
##    d3 = datetime.datetime(2017, 04, 07, 17, 40, 0)
##    print IsSeriesDate(d1, d2)
##    print IsSeriesDate(d1, d3)
