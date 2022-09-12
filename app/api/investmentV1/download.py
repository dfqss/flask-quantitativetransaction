import datetime
import os
import shutil
import time
from itertools import zip_longest
from operator import and_

import xlwt
from flask import Flask, Blueprint, make_response, send_file, request
from lin import db

from app.api.investmentV1.model.industryClass import MbaIndustryClass
from app.api.investmentV1.model.listingDateCal import MbaListingDateCal
from app.api.investmentV1.model.stockPool import MbaStockPool
from app.config.development import DevelopmentConfig
from app.api.investmentV1.model.coreIndex import MbaCoreIndex, MbaCoreIndexHist
from app.api.investmentV1.model.backtest import MbaCoreIndexBack, MbaFinAnalysisIndexBack, \
    MbaRangeRiseCommon
from sqlalchemy import func

from app.util import common
from app.util.common import addFieldByConditions

app = Flask(__name__)
download_file_api = Blueprint("download", __name__)

# 文件下载目录
downloadFilePath = DevelopmentConfig.downloadFilePath


@download_file_api.route('/downloadFile', methods=["get"])  # 设置路由
def downloadStockPoolFile():  # 执行视图函数
    fileType = request.args.get("fileType")
    if fileType == 'StockPool':
        data = stockPool_data()  # 获取数据
        # 生成excel文件列表头字段
        keys = ['股票代码', '股票名称', '行业名称(申万)', '备注', '创建日期', '资本市场指标']
        # 文件名
        file_name = str(round(time.time() * 1000)) + "_StockPool.xls"
        # execl sheet名
        sheet = "StockPool"
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'periods', 'remark', 'create_time', 'industry_sw']
        dataList = model_to_dict(data, mapList)
    elif fileType == 'CoreIndex':
        # 数据
        data = coreIndex_date()  # 获取数据
        # 生成excel文件列表头字段
        keys = ['股票代码', '股票名称', '行业名称(申万)', '上期核心指数', '本期核心指数', '是否新股', '期数', '是否本期新增', '获取日期',
                '报告日期', "资本市场指标"]
        # 文件名
        file_name = str(round(time.time() * 1000)) + "_CoreIndex.xls"
        # execl sheet名
        sheet = "CoreIndex"
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'industrySw', 'preFinalCalCore', 'finalCalCore',
                   'isNewShares', 'periods', 'showTimes', 'calDate', 'reportDate']
        dataList = model_to_dict(data, mapList)
        dataList = capsulationDate(dataList)
    elif fileType == 'CodeIndexBack':
        # 获取文件期数
        periods = request.args.get("periods")
        # 数据
        data = coreIndexBack_date(periods)  # 获取数据
        # 生成excel文件列表头字段
        keys = ['股票代码', '股票名称', '期数', '核心指数', '净资产收益率ROE(平均)', '季涨幅', '半年涨幅', '报告日期']
        # 文件名
        file_name = str(round(time.time() * 1000)) + "_CoreIndexBack.xls"
        # execl sheet名
        sheet = "CoreIndexBack"
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'periods', 'finalCalCore', 'roeAvg',
                   'quarterRise', 'halfYearRise', 'calDate']
        dataList = model_to_dict(data, mapList)
    # 添加资本市场指标
    dataList = addFieldByConditions(dataList)
    app.logger.info('start service downloadFile------excel文件下载：' + file_name)
    # 文件下载地址
    file_path = os.path.join(downloadFilePath, common.get_now_time_yyyymmdd())
    # 判断文件夹是否存在,不存在创建新的
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # 生成要下载的临时文件
    listInDist_Excle(dataList, file_path, file_name, sheet, keys)
    # 调用下载文件方法
    return download_Excel(file_path, file_name)


# 查询出来的数据转为字典
def model_to_dict(data, mapList):
    dataList = []
    for returnData in data:
        dataList.append(dict(zip_longest(mapList, returnData)))
    return dataList


# 下载操作
def download_Excel(file_path='', file_name="execl1.xls"):
    # 下载的文件内容
    response = make_response(send_file(os.path.join(file_path, file_name)))
    # 下载的文件名字
    response.headers["Content-Disposition"] = "attachment; filename=" + file_name + ";"
    return response


# 将list字典导出成excel
# data = [{'a': 'a', 'id': 1}, {'a': 'b', 'id': 2}, {'a': 'c', 'id': 3}, {'a': 'e', 'id': 4}]
def listInDist_Excle(data=[], file_path="", excel_name="execl1.xls", sheet_name="sheet1", keys=[]):
    wb = xlwt.Workbook(encoding='utf-8')  # 实例化，有encoding和style_compression参数
    ws = wb.add_sheet(sheet_name, cell_overwrite_ok=True)  # Workbook的方法，生成名为111.xls文件
    for i in range(0, len(keys)):  # 将这些字段写入111.xls文件
        ws.write(0, i, keys[i])
    k = 1
    for i in data:  # 循环每一列
        i_keys = list(i.keys())
        for j in range(len(keys)):  # 在每列添加数据
            ws.write(k, j, i[i_keys[j]])
        k += 1
    wb.save(excel_name)
    shutil.move(excel_name, os.path.join(file_path, excel_name))
    return 'ok'  # 必须return，并且不能return 空


# 封装投资标初选数据
def capsulationDate(dataList):
    resultList = []
    for date in dataList:
        isNewShares = date.get("isNewShares")
        if isNewShares == "N":
            date["isNewShares"] = "新股"
        elif isNewShares == "F":
            date["isNewShares"] = "非新股"
        elif isNewShares == 'C':
            date["isNewShares"] = "次新股"
        showTimes = date.get("showTimes")
        if showTimes == 1:
            date["showTimes"] = "本期数据"
        elif showTimes != 1:
            date["showTimes"] = "往期数据"
        resultList.append(date)
    return resultList


def stockPool_data():
    dateList = db.session.query(MbaStockPool.code,
                                MbaStockPool.code_name,
                                MbaIndustryClass.industry_sw,
                                MbaStockPool.remark,
                                func.date_format(MbaStockPool.create_time, "%Y-%m-%d").label(
                                    "m_time")
                                ) \
        .outerjoin(MbaIndustryClass, MbaStockPool.code == MbaIndustryClass.code).all()
    return dateList


def coreIndex_date():
    # 拼接查询条件-查询展示状态为 0-展示 的数据
    filterList = [MbaCoreIndex.status == '0', MbaCoreIndexHist.periods == MbaCoreIndex.periods - 1]
    # 查询数据
    dateList = db.session.query(MbaCoreIndex.code,
                                MbaCoreIndex.code_name,
                                MbaIndustryClass.industry_sw,
                                MbaCoreIndexHist.final_cal_core.label("pre_final_cal_core"),
                                MbaCoreIndex.final_cal_core,
                                MbaListingDateCal.is_new_shares,
                                MbaCoreIndex.periods,
                                MbaCoreIndex.show_times,
                                func.date_format(MbaCoreIndex.cal_date, "%Y-%m-%d").label("m_time"),
                                func.date_format(MbaCoreIndex.report_date, "%Y-%m-%d").label(
                                    "m_time")) \
        .outerjoin(MbaListingDateCal, MbaCoreIndex.code == MbaListingDateCal.code) \
        .outerjoin(MbaIndustryClass, MbaCoreIndex.code == MbaIndustryClass.code) \
        .outerjoin(MbaCoreIndexHist, MbaCoreIndex.code == MbaCoreIndexHist.code) \
        .filter(*filterList).all()
    return dateList


def coreIndexBack_date(periods):
    # 拼接查询条件-查询展示状态为 0-展示 的数据-根据期数查询
    filterList = [MbaCoreIndexBack.status == '0', MbaCoreIndexBack.periods == periods]
    dateList = db.session.query(MbaCoreIndexBack.code,
                                MbaCoreIndexBack.code_name,
                                MbaCoreIndexBack.periods,
                                MbaCoreIndexBack.final_cal_core,
                                MbaFinAnalysisIndexBack.roe_avg,
                                MbaRangeRiseCommon.quarter_rise,
                                MbaRangeRiseCommon.half_year_rise,
                                MbaCoreIndexBack.cal_date) \
        .outerjoin(MbaFinAnalysisIndexBack,
                   and_(MbaCoreIndexBack.code == MbaFinAnalysisIndexBack.code,
                        MbaCoreIndexBack.periods == MbaFinAnalysisIndexBack.periods)
                   ) \
        .outerjoin(MbaRangeRiseCommon, and_(MbaCoreIndexBack.code == MbaRangeRiseCommon.code,
                                            MbaCoreIndexBack.periods == MbaRangeRiseCommon.periods)
                   ) \
        .filter(*filterList).order_by(MbaCoreIndexBack.code).all()
    return dateList
