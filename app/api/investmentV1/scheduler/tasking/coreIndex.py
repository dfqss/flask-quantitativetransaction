from app.api.investmentV1.model.coreIndex import MbaCoreIndex
from app.api.investmentV1.model.batchFiles import MbaBatchFiles
from app.util.excel import readExcel
import datetime
import time
from app.util.common import filterNewDictList
from sqlalchemy import or_, and_, not_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.development import DevelopmentConfig
from app.api.investmentV1.scheduler.tasking.batchFiles import update_batch_files_status

# 定义全局app变量
app = Flask(__name__)

# 加载配置:必须先加载配置参数，再创建conn才有效
app.config.from_object(DevelopmentConfig())

# 创建全局的数据库连接对象，一个数据库连接对象下执行同一个session
conn = SQLAlchemy(app)


# 批量创建或更新核心指数表
def createOrUpdateCoreIndex():
    keys = ['code', 'name', 'core']
    file = get_file_names()
    if len(file) <= 0:
        app.logger.info('没有需要计算的核心指标数据')
        return
    filePath = file[0][0]
    fileName = file[0][1]
    # 1.将数据更新为：毫秒值-[读取中]
    update_batch_files_status(conn, fileName, str(round(time.time() * 1000)), '')
    try:
        # 2.读取excel中核心指标信息对象列表
        excelData = readExcel(filePath, fileName, 0, 2, keys)
        # 3.查询核心指数表中的所有信息
        coreIndexData = conn.session.query(MbaCoreIndex).all()
        # 4.当核心指数表的数据不为空时：新增并更新核心指数表
        if len(coreIndexData) > 0:
            app.logger.info('start------计算核心指标文件: ' + fileName)
            # 将上一期的数据原封不动插入到历史表中
            backup_hist()
            # 创建核心指数数据
            create_core_index(excelData, coreIndexData)
            # 更新核心指数数据
            update_core_index(excelData, coreIndexData)
            # 更新计算日期：更新为当前时间
            update_cal_date()
            # 更新展示次数
            update_show_times()
            app.logger.info('end------计算核心指标文件: ' + fileName)
        else:
            app.logger.info('start------首次初始化核心指标数据文件: ' + fileName)
            create_core_index(excelData, coreIndexData)
            app.logger.info('end------首次初始化核心指标数据文件完成')
        # 提交核心指标计算后的数据
        conn.session.commit()
        # 更新数据读取状态为：2-成功
        update_batch_files_status(conn, fileName, '2', '')
    except Exception as e:
        app.logger.info('读取核心指标文件失败 [' + str(e) + ']')
        conn.session.rollback()
        # 更新数据读取状态为：1-失败
        update_batch_files_status(conn, fileName, '1', str(e))
    finally:
        conn.session.close()


# 查询mba_batch_files表中需要写入的核心指标文件的路径和文件名
def get_file_names():
    slq = conn.session.query(MbaBatchFiles.file_path, MbaBatchFiles.file_name).\
        filter(and_(MbaBatchFiles.file_name.startswith('HXZB'),
                    # 根据字段排序加 -MbaBatchFiles.file_name是降序
                    MbaBatchFiles.status.__eq__('0'))).order_by(MbaBatchFiles.file_name).limit(1)
    return slq.all()


# 再更新和新增mba_core_index之前将所有数据备份到mba_core_index_hist中
def backup_hist():
    app.logger.info('开始备份上期数据')
    try:
        sql = "insert into mba_core_index_hist select * from mba_core_index"
        conn.session.execute(sql)
    except Exception as e:
        app.logger.error('上期数据数据备份失败:' + str(e))
        raise Exception("上期数据数据备份失败")


# 新增核心指数表数据
def create_core_index(excelData, coreIndexData):
    app.logger.info('新增核心指标数据')
    try:
        insertList = filterNewDictList(excelData, coreIndexData, 'code')
        if len(insertList) != 0:
            sql = "insert into mba_core_index " \
                  "(is_deleted, code, code_name, current_core, period_core, " \
                  "final_cal_core, status, show_times, cal_date, create_time, " \
                  "update_time) values " \
                  "('0', :code, :name, :core, '0', '0.00', '1', 0, now(), now(), now())"
            conn.session.execute(sql, insertList)
    except Exception as e:
        app.logger.error('新增核心指标数据失败:' + str(e))
        raise Exception("新增核心指标数据失败")


# 更新核心指数表数据
def update_core_index(excelData, coreIndexData):
    app.logger.info('更新核心指标数据')
    try:
        # 组装数据列表
        updateList = []
        for coreIndexObj in coreIndexData:
            for excelDataDic in excelData:
                updateDic = assembleData(coreIndexObj, excelDataDic)
                # 当结果不为空的时候，将字典更新到updateList中
                if bool(updateDic):
                    updateList.append(updateDic)
        # 更新核心指数列表
        if len(updateList) != 0:
            sql = "update mba_core_index set " \
                  "current_core = :current_core, period_core = :period_core, " \
                  "final_cal_core = :final_cal_core, update_time = :update_time, " \
                  "status = :status, cal_date = now() where code = :code"
            conn.session.execute(sql, updateList)
    except Exception as e:
        app.logger.error('更新核心指标数据失败:' + str(e))
        raise Exception("更新核心指标数据失败")


# 更新计算日期：更新为当前时间
def update_cal_date():
    app.logger.info('更新计算日期')
    try:
        sql = "update mba_core_index set cal_date = NOW() "
        conn.session.execute(sql)
    except Exception as e:
        app.logger.error('更新计算日期失败:' + str(e))
        raise Exception("更新计算日期失败")


# 更新展示次数：每展示一次就加1
def update_show_times():
    app.logger.info('更新展示次数')
    try:
        sql = "update mba_core_index set show_times = show_times + 1 where status = '0' "
        conn.session.execute(sql)
    except Exception as e:
        app.logger.error('更新展示次数失败:' + str(e))
        raise Exception("更新展示次数失败")


# 组装数据
def assembleData(coreIndexObj, excelDataDic):
    returnDataDic = dict()
    if coreIndexObj['code'] == excelDataDic['code']:
        # 非字符串类型，转换成字符串
        if not isinstance(excelDataDic['core'], str):
            excelDataDic['core'] = str(int(excelDataDic['core']))
        # 判断excel是否上传当期核心指标，没传递则将status状态修改成：1-不展示
        if len(excelDataDic['core'].strip()) <= 0:
            returnDataDic['status'] = '1'
            returnDataDic['period_core'] = coreIndexObj['period_core']
            returnDataDic['current_core'] = coreIndexObj['current_core']
            returnDataDic['final_cal_core'] = coreIndexObj['final_cal_core']
        else:
            # 将表中current_core的值与excel中的核心指标进行对比：如果不一样则进行计算
            currentCore = coreIndexObj['current_core']
            core = excelDataDic['core']
            # 判断查询出的数据是否为空字符，为空则将status修改成：1-不展示
            if len(currentCore.strip()) <= 0:
                returnDataDic['status'] = '1'
                # 上期核心指标换成当期核心指标
                returnDataDic['period_core'] = currentCore
                # 当期核心指标换成excel传入的核心指标
                returnDataDic['current_core'] = core
                # 核心指标不计算
                returnDataDic['final_cal_core'] = coreIndexObj['final_cal_core']
            else:
                if currentCore != core:
                    # 将current_core的数据赋值给period_core
                    returnDataDic['period_core'] = currentCore
                    # 将excel中的当期核心指标赋值给current_core
                    returnDataDic['current_core'] = core
                    # 计算：(current_core - period_core) / period_core 结果保留2为小数
                    finalCalCore = format((float(core) - float(currentCore)) / float(currentCore),
                                          '.2f')
                    # 将计算结果赋值给final_cal_core
                    returnDataDic['final_cal_core'] = finalCalCore
                    # 将计算结果小于 -0.1 的status状态修改成：0-展示  否则修改成：1-不展示
                    if float(finalCalCore) < -0.1:
                        returnDataDic['status'] = 0
                    else:
                        returnDataDic['status'] = 1
                else:
                    # 当excel上传的核心指标与上次的核心指标一样，则保留上次的展示结果
                    return dict()
        returnDataDic['code'] = coreIndexObj['code']
        returnDataDic['update_time'] = datetime.datetime.now()
        return returnDataDic
    # 如果没有匹配上任何条件则返回空字典
    return dict()
