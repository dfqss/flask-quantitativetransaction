import xlrd
import os
import datetime
from itertools import zip_longest

# *args是可变参数，args接收的是一个tuple；
# **kw是关键字参数，kw接收的是一个dict。


# 读取excel文件的所有行对象到列表中
# filePath：文件的路径
# fileName：文件的名称
# sheetIndex：读取文件的sheet页的索引位置
# startIndex：从当前sheet页的行索引开始读取
# keys：每列数据的字典key列表（按照列的顺序排序）
def readExcel(filePath: str, fileName: str,
              sheetIndex: int = 0, startIndex: int = 0, keys: list = []):
    # 判断文件名是否为空，为空则返回异常信息
    if fileName.isspace():
        raise Exception('文件名fileName为空')
    # 判断文件路径是否存在
    if not os.path.exists(filePath):
        # 如果不存在则创建目录
        os.makedirs(filePath)
    # 拼接文件的全路径
    fileFullPath = os.path.join(filePath, fileName)
    # 判断文件是否存在，不存在则返回异常信息
    if not os.path.isfile(fileFullPath):
        raise Exception('文件:' + fileFullPath + '不存在')
    # 读取文件对象
    data = xlrd.open_workbook(fileFullPath)
    # 获取第一个工作薄
    sheet = data.sheet_by_index(sheetIndex)
    # 组装数据参数
    dataList = []
    for i in range(sheet.nrows):
        if i < startIndex:
            continue
        dataList.append(dict(zip_longest(keys, sheet.row_values(i))))
    return dataList


# 根据key值，将列表中所有符合条件的字典对应的value值转换成对应的类型
def formatCellValue(formatList, key, dataType):
    for formatDict in formatList:
        if key in formatDict:
            # 将数据转换成时间类型
            if dataType == 'datetime':
                # 第二个参数-dateMode:0是以1900-01-01为基准的日期, 1是1904-01-01为基准的日期
                formatDict[key] = xlrd.xldate_as_datetime(formatDict[key], 0)
                continue
            if dataType == 'str':
                # 添加你需要的代码
                continue
            if dataType == 'other':
                # 添加你需要的代码
                continue

