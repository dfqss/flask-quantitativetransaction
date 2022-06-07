from app.api.investmentV1.model.listingDateCal import MbaListingDateCal, MbaShares
from app.api.investmentV1.model.batchFiles import MbaBatchFiles
import datetime
from dateutil import rrule
import time
from app.util.common import filterNewDictList, get_now_time_yyyymmdd
from sqlalchemy import or_, and_, not_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.development import DevelopmentConfig
from app.api.investmentV1.scheduler.tasking.batchFiles import update_batch_files_status
import xlrd
import os
from itertools import zip_longest
from xlrd import xldate_as_tuple
from dateutil import rrule

from app.util.excel import readExcel

# 定义全局app变量
app = Flask(__name__)

# 加载配置:必须先加载配置参数，再创建conn才有效
app.config.from_object(DevelopmentConfig())

# 创建全局的数据库连接对象，一个数据库连接对象下执行同一个session
conn = SQLAlchemy(app)


# 批量创建或更新核心指数表
def createOrUpdateListingDateIndex():
    # 获取要读取文件的信息
    file = get_file_names()
    # 没有查询到要读取的文件直接返回
    if len(file) <= 0:
        app.logger.info('没有需要计算上市日期数据')
        return
    # 获取文件路径、文件名称和文件期数
    filePath = file[0][0]
    fileName = file[0][1]
    filePeriods = file[0][2]
    # 将数据更新为：毫秒值-[读取中]
    update_batch_files_status(conn, fileName, str(round(time.time() * 1000)), '')
    try:
        app.logger.info('------start 开始计算上市日期: ' + fileName)
        # 1.读取excel中核心指标数据
        app.logger.info('读取上市日期文件: ' + fileName)
        keys = ['code', 'name', 'ipo_date']
        excelData = readExcel(filePath, fileName, 0, 2, keys)
        # 2.查询数据库
        app.logger.info('查询上市日期上期数据')
        queryList = (conn.session.query(MbaListingDateCal.code, MbaListingDateCal.ipo_date)).all()
        print(type(queryList))
        # 3.查看是否为空表,为空表插入数据
        if len(queryList) <= 0:
            # 3.excelData
            app.logger.info('初始化上市日期表数据')
            create_table(excelData)
            return
        # 4.更新上市时间表
        app.logger.info('更新上市日期表数据')
        update_listing_deta(excelData)
        # 5.查看新增数据
        filterList = filterNewDictList(excelData, queryList, 'code')
        # 6.新增上市时间index表
        if len(filterList) < 0:
            create_table(filterList)
        # 提交数据
        conn.session.commit()
        # 更新数据读取状态为：2-成功
        update_batch_files_status(conn, fileName, '2', '')
    except Exception as e:
        app.logger.info('读取批量指标文件失败 [' + str(e) + ']')
        conn.session.rollback()
        # 更新数据读取状态为：1-失败
        update_batch_files_status(conn, fileName, '1', str(e))
    finally:
        conn.session.close()


# 查询mba_batch_files表中需要写入的上市时间文件的路径和文件名
def get_file_names():
    # 根据字段排序加 -MbaBatchFiles.file_name是降序
    slq = conn.session \
        .query(MbaBatchFiles.file_path, MbaBatchFiles.file_name, MbaBatchFiles.file_periods) \
        .filter(and_(MbaBatchFiles.file_name.startswith('SSRQ'), MbaBatchFiles.status.__eq__('0'))) \
        .order_by(MbaBatchFiles.file_periods).limit(1)
    return slq.all()


# 初始化上市时间表
def create_table(excelData):
    app.logger.info('初始化上市时间表')
    try:
        if len(excelData) > 0:
            sql = "insert into mba_shares(is_deleted, code, name, " \
                  "ipo_date, create_time) values ('0', :code, :name, " \
                  ":ipo_date, now()) "
            conn.session.execute(sql, excelData)
            # 计算上市天数与(新,次,否)股票
            listingDateList =calculation(excelData)
            sql = "insert into mba_listing_date_cal(is_deleted, code, name, ipo_date, " \
                  "create_time, update_time) values ('0', :code, :name, " \
                  ":ipo_date, now(), now()) "
            conn.session.execute(sql, listingDateList)
    except Exception as e:
        app.logger.error('初始化上市时间表失败:' + str(e))
        raise Exception("初始化上市时间表失败")


# 计算上市天数与(新,次,否)股票
def calculation(excelData):
    try:
        listingDateList = []
        for excelLine in excelData:
            # 判断excelLine是否是字段
            if not isinstance(excelLine, dict):
                excelLine = excelLine.to_dict()
            # 间隔月数
            # 上市时间
            nowDate = datetime.datetime.now().strftime("%Y-%m-%d")
            nowYear, nowMonth, nowDay = format_date(nowDate)[:3]
            listingYear, listingMonth, listingDay = format_date(excelLine.get('ipo_date'))
            d1 = datetime.date(nowYear, nowMonth, nowDay)
            d2 = datetime.date(listingYear, listingMonth, listingDay)
            month_count = rrule.rrule(rrule.MONTHLY, dtstart=d1, until=d2).count()
            if month_count < 6:
                excelLine['is_new_shares'] = 'N'
            elif month_count < 12:
                excelLine['is_new_shares'] = 'C'
            else:
                excelLine['is_new_shares'] = 'F'
            # 上市天数
            excelLine['listing_day'] += 1
            listingDateList.append(excelLine)
        return listingDateList
    except Exception as e:
        app.logger.error('计算上市天数与(新,次,否)股票:' + str(e))
        raise Exception("计算上市天数与(新,次,否)股票")


# 转换日期格式 ’2019-02-01‘ =》 2019 02 01
def format_date(date):
    fmt = '%Y-%m-%d'
    time_tuple = time.strptime(date, fmt)
    return time_tuple[:3]

# 更新上市时间表上市天数与(新,次,否)股票
def update_listing_deta(excelData):
    app.logger.info('更新上市时间表上市天数与(新,次,否)股票')
    try:
        if len(excelData) > 0:
            # 计算上市天数与(新,次,否)股票
            listingDateList = calculation(excelData)
            sql = "update mba_listing_date_cal set is_new_shares = :is_new_shares, " \
                  "listing_day = listing_day+1, update_time = now() " \
                  "where code = :code"
            conn.session.execute(sql, listingDateList)
    except Exception as e:
        app.logger.error('更新上市时间表上市天数与(新,次,否)股票:' + str(e))
        raise Exception("更新上市时间表上市天数与(新,次,否)股票")

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
    nrows = sheet.nrows
    ncols = sheet.ncols
    for iRow in range(1, nrows):
        execlLine = {}
        flag = 0
        for iCol in range(ncols):
            sCell = sheet.cell_value(iRow, iCol)
            # Python读Excel，返回的单元格内容的类型有5种：
            # ctype： 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
            ctype = sheet.cell(iRow, iCol).ctype
            # ctype =3,为日期
            if ctype == 3:
                date = datetime(*xldate_as_tuple(sCell, 0))
                cell = date.strftime('%Y-%m-%d')  # ('%Y/%m/%d %H:%M:%S')
                execlLine['ipo_date'] = cell
                flag +=1
            if iCol == 0:
                execlLine['code'] =sCell
                flag += 1
            if iCol == 1:
                execlLine['name'] =sCell
                flag += 1
            if flag == 3:
                dataList.append(execlLine)
    return dataList
