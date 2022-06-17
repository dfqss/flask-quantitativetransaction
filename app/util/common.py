import decimal
import os
from itertools import groupby
from operator import itemgetter
import copy
import datetime
from dateutil import rrule


# 获取当前系统时间的年月日时分秒(返回字符串对象) 返回格式-yyyymmdd
def get_now_time_yyyymmdd():
    return datetime.datetime.now().strftime("%Y%m%d")


# 获取月份差(返回Decimal类型) 传入格式-yy-mm-dd 返回：月份差
def get_month_diff_d(startDate, endDate):
    # 格式化起始日期:将字符串转换成datetime类型
    if isinstance(startDate, str):
        start_date = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    else:
        start_date = startDate
    # 格式化结束日期:将字符串转换成datetime类型
    if isinstance(endDate, str):
        end_date = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    else:
        end_date = endDate
    # 获取起始日期年、月、日
    s_y = start_date.year
    s_m = start_date.month
    s_d = start_date.day
    # 获取结束日期年、月、日
    e_y = end_date.year
    e_m = end_date.month
    e_d = end_date.day
    # 计算年、月、日各时间差
    diff_y = e_y - s_y
    diff_m = e_m - s_m
    diff_d = e_d - s_d
    # 最终计算出起始日期和结束日期的时间差
    diff_info = diff_y * 12 + diff_m + (decimal.Decimal(str(diff_d)) / decimal.Decimal('31'))
    return round(diff_info, 1)


# 获取月份差(返回int类型) 传入格式-yy-mm-dd 返回：月份差
def get_month_diff_i(startDate, endDate):
    # 格式化起始日期:将字符串转换成datetime类型
    if isinstance(startDate, str):
        start_date = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    else:
        start_date = startDate
    # 格式化结束日期:将字符串转换成datetime类型
    if isinstance(endDate, str):
        end_date = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    else:
        end_date = endDate
    return rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date).count()


# 获取两个日期差(返回int类型) 传入格式-yy-mm-dd 返回：日期差
def get_day_diff(startDate, endDate):
    # 格式化起始日期:将字符串转换成datetime类型
    if isinstance(startDate, str):
        start_date = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    else:
        start_date = startDate
    # 格式化结束日期:将字符串转换成datetime类型
    if isinstance(endDate, str):
        end_date = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    else:
        end_date = endDate
    return (end_date - start_date).days


# 将一个字典列表的某一个key提炼出来，作为该数据的标识，并将其所在的数据列表作为value
def split_group(dict_list, key):
    dict_list.sort(key=itemgetter(key))
    tmps = groupby(dict_list, itemgetter(key))
    result = []
    for key, group in tmps:
        result.append({key: list(group)})
    return result


# 根据某一列表中字典的key值，过滤出另一个列表中不一样的字典的数据
def filterNewDictList(orgList, filter, key):
    returnList = []
    if len(orgList) <= 0 or len(key.strip()) <= 0:
        return returnList
    for dict1 in orgList:
        addFlag = True
        if not isinstance(dict1, dict):
            dict1 = dict1.to_dict()
        if key not in dict1 or len(dict1[key].strip()) <= 0:
            continue
        value1 = dict1[key]
        # 开始过滤
        for dict2 in filter:
            if not isinstance(dict2, dict):
                dict2 = dict2.to_dict()
            if key not in dict2 or len(dict2[key].strip()) <= 0:
                continue
            value2 = dict2[key]
            if value1 == value2:
                addFlag = False
                break
        if addFlag:
            returnList.append(copy.deepcopy(dict1))
    return returnList


# # 给返回数据新增一个字段
# def addFieldByCondition(dataList, condition, field):
#     returnList = []
#     if len(dataList) <= 0 and field != "" and condition != "":
#         return returnList
#     for date in dataList:
#         addFlag = True
#         if not isinstance(date, dict):
#             date = date.to_dict()
#         if(condition):
#             date[field] = field
#     pass


# 给返回数据新增一个字段
def addFieldByConditions(dataList):
    returnList = []
    if len(dataList) <= 0:
        return returnList
    for date in dataList:
        if not isinstance(date, dict):
            date = date.to_dict()
        strCode = date['code'][0:3]
        if strCode == '600':
            date['capitalMarket'] = '上主板'
        elif strCode == '000':
            date['capitalMarket'] = '深主板'
        elif strCode == '002':
            date['capitalMarket'] = '中主板'
        elif strCode == '300':
            date['capitalMarket'] = '创业板'
        elif strCode == '688':
            date['capitalMarket'] = '科技板'
        elif strCode.startswith('8', 0, 1):
            date['capitalMarket'] = '京市A股'
        else:
            date['capitalMarket'] = ''
        returnList.append(date)
    return returnList


basedir = os.getcwd()
