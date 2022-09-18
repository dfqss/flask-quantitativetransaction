from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.listingDateCal import MbaListingDateCal
from app.api.investmentV1.model.batchFiles import MbaBatchFiles
import datetime
import time
from app.util import common
from sqlalchemy import or_, and_, not_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.development import DevelopmentConfig
from app.api.investmentV1.scheduler.tasking.batchFiles import update_batch_files_status
from app.util.excel import readExcel, formatCellValue

# 定义全局app变量
app = Flask(__name__)

# 加载配置:必须先加载配置参数，再创建conn才有效
app.config.from_object(DevelopmentConfig())

# 创建全局的数据库连接对象，一个数据库连接对象下执行同一个session
conn = SQLAlchemy(app)


# 批量创建或更新核心指数表
def createOrUpdateListingDateCal():
    # 获取要读取文件的信息
    file = get_file_names()
    # 没有查询到要读取的文件直接返回
    if len(file) <= 0:
        app.logger.info('没有需要计算上市日期数据')
        return success(22)
    # 获取文件路径、文件名称
    filePath = file[0][0]
    fileName = file[0][1]
    # 将数据更新为：毫秒值-[读取中]
    update_batch_files_status(conn, fileName, str(round(time.time() * 1000)), '')
    try:
        app.logger.info('------start 开始计算上市日期: ' + fileName)
        # 1.读取excel中上市日期的数据
        keys = ['code', 'name', 'ipo_date']
        excelData = readExcel(filePath, fileName, 0, 2, keys)
        # 将ipo_date的值转换成datetime类型
        formatCellValue(excelData, 'ipo_date', 'datetime')
        # 2.查询数据库
        queryList = conn.session.query(MbaListingDateCal).all()
        # 3.如果查询数据为空则进行数据初始化
        if len(queryList) <= 0:
            app.logger.info('start------首次初始化上市日期表数据: ' + fileName)
            create_table(excelData)
            app.logger.info('end------首次初始化上市日期表数据完成')
        else:
            # 4.更新上市时间表
            update_listing_deta(excelData)
            # 5.过滤出需要新增的数据
            filterList = common.filterNewDictList(excelData, queryList, 'code')
            # 6.新增上市日期表数据
            if len(filterList) > 0:
                create_table(filterList)
        # 提交数据
        conn.session.commit()
        # 更新数据读取状态为：2-成功
        update_batch_files_status(conn, fileName, '2', '')
    except Exception as e:
        app.logger.info('读取上市日期文件失败 [' + str(e) + ']')
        conn.session.rollback()
        # 更新数据读取状态为：1-失败
        update_batch_files_status(conn, fileName, '1', str(e))
        return failed(10219)
    finally:
        conn.session.close()
    return success(22)


# 查询mba_batch_files表中需要写入的上市时间文件的路径和文件名
def get_file_names():
    # 根据字段排序加 -MbaBatchFiles.file_name是降序
    slq = conn.session \
        .query(MbaBatchFiles.file_path, MbaBatchFiles.file_name) \
        .filter(and_(MbaBatchFiles.file_name.startswith('SSRQ'),
                     MbaBatchFiles.status.__eq__('0'))) \
        .order_by(MbaBatchFiles.file_periods).limit(1)
    return slq.all()


# 初始化上市时间表
def create_table(insertData):
    app.logger.info('开始创建上市日期数据')
    try:
        if len(insertData) > 0:
            # 计算上市天数与(新,次,否)股票
            calculation(insertData)
            sql = "insert into mba_listing_date_cal " \
                  "(is_deleted, code, is_new_shares, listing_day, ipo_date, " \
                  "create_time, update_time) values " \
                  "('0', :code, :is_new_shares, :listing_day, :ipo_date, now(), now()) "
            conn.session.execute(sql, insertData)
    except Exception as e:
        app.logger.error('初始化上市日期表数据失败:' + str(e))
        raise Exception("初始化上市日期表数据失败")


# 计算上市天数与(新,次,否)股票
def calculation(calData):
    for dataDict in calData:
        ipo_date = dataDict['ipo_date']
        now_date = datetime.datetime.now()
        dataDict['listing_day'] = common.get_day_diff(ipo_date, now_date)
        # 计算月份差
        diff_month = common.get_month_diff_i(ipo_date, now_date)
        if diff_month <= 6:
            # 小于等于6个月：新股
            dataDict['is_new_shares'] = 'N'
        elif diff_month > 12:
            # 大于12个月：非新股
            dataDict['is_new_shares'] = 'F'
        else:
            # 大于6个月 并且 小于等于12个月：次新
            dataDict['is_new_shares'] = 'C'


# 更新上市时间表上市天数与(新,次,否)股票
def update_listing_deta(excelData):
    app.logger.info('更新上市时间表上市天数与(新,次,否)股票')
    try:
        if len(excelData) > 0:
            # 计算上市天数与(新,次,否)股票
            calculation(excelData)
            sql = "update mba_listing_date_cal " \
                  "set is_new_shares = :is_new_shares, " \
                  "listing_day = :listing_day, update_time = now() where code = :code "
            conn.session.execute(sql, excelData)
    except Exception as e:
        app.logger.error('更新上市时间表上市天数与(新,次,否)股票失败:' + str(e))
        raise Exception("更新上市时间表上市天数与(新,次,否)股票失败")
