import os
from itertools import groupby
from operator import itemgetter
import copy
import datetime


# 获取当前系统时间的年月日时分秒
def get_now_time_yyyymmdd():
    return datetime.datetime.now().strftime("%Y%m%d")


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


basedir = os.getcwd()
