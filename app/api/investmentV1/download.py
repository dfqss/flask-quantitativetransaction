import datetime
import os
import shutil
import time
from io import BytesIO

import xlwt
from flask import Flask, Blueprint, make_response, send_file, request
from lin import db
from app.api.investmentV1.model.stockPool import MbaStockPool
from app.config.development import DevelopmentConfig
from app.api.investmentV1.model.coreIndex import MbaCoreIndex
from sqlalchemy import func

from app.util import common

app = Flask(__name__)
download_file_api = Blueprint("download", __name__)


def stockPool_data():
    dateList = db.session.query(MbaStockPool.code, MbaStockPool.code_name).all()
    print(dateList)
    return dateList


def coreIndex_date():
    dateList = db.session.query(MbaCoreIndex.code, MbaCoreIndex.code_name,
                                MbaCoreIndex.current_core, MbaCoreIndex.periods,
                                MbaCoreIndex.final_cal_core, MbaCoreIndex.periods,
                                MbaCoreIndex.status, MbaCoreIndex.show_times,
                                func.date_format(MbaCoreIndex.cal_date, "%Y-%m-%d").label("m_time"),
                                func.date_format(MbaCoreIndex.create_time, "%Y-%m-%d").label(
                                    "m_time"),
                                func.date_format(MbaCoreIndex.update_time, "%Y-%m-%d").label(
                                    "m_time")).filter(
        MbaCoreIndex.status == '0').all()
    return dateList


# 文件下载目录
downloadFilePath = DevelopmentConfig.downloadFilePath


@download_file_api.route('/downloadFile', methods=["get"])  # 设置路由
def downloadStockPoolFile():  # 执行视图函数
    fileTpye = request.args.get("fileTpye")
    print(fileTpye)
    if fileTpye == 'StockPool':
        data = stockPool_data()  # 获取数据
        # 生成excel文件列表头字段
        keys = ["code", "code_name"]
        # 文件名
        file_name = str(round(time.time() * 1000)) + "_StockPool.xls"
        # execl sheet名
        sheet = "StockPool"
    elif fileTpye == 'CoreIndex':
        # 数据
        data = coreIndex_date()  # 获取数据
        # 生成excel文件列表头字段
        keys = MbaCoreIndex().key_to_list()
        # 文件名
        file_name = str(round(time.time() * 1000)) + "_CoreIndex.xls"
        # execl sheet名
        sheet = "CoreIndex"
    app.logger.info('start service downloadFile------excel文件下载：' + file_name)
    # 文件下载地址
    file_path = os.path.join(downloadFilePath, common.get_now_time_yyyymmdd())
    # 判断文件夹是否存在,不存在创建新的
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # 生成要下载的临时文件
    listInDist_Excle(data, file_path, file_name, sheet, keys)
    # 调用下载文件方法
    return download_Excel(file_path, file_name)


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
        for j in range(len(keys)):  # 在每列添加数据
            ws.write(k, j, i[j])
        k += 1
    wb.save(excel_name)
    shutil.move(excel_name, os.path.join(file_path, excel_name))
    return 'ok'  # 必须return，并且不能return 空
