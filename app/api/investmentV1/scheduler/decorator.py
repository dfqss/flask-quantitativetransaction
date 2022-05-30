"""
# coding:utf-8
@Time    : 2022/04/30
@Author  : sushuai
@desc    : 使用装饰器定时启动任务
@notes   : 使用时将业务代码写入job函数中，并在需要的时候调用executeJob函数执行定时任务
           job1: 每间隔30s执行一次函数
           job2: 每分钟执行一次函数
           job3: 每周的星期天执行一次函数
           job4: 每天的13:26:05时刻执行一次函数
"""
# # interval examples
# @scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
# def job1():
#     print(str(datetime.datetime.now()) + ' Job 1 executed')

# # cron examples
# @scheduler.task('cron', id='do_job_2', minute='*')
# def job2():
#     print(str(datetime.datetime.now()) + ' Job 2 executed')

# @scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
# def job3():
#     print(str(datetime.datetime.now()) + ' Job 3 executed')

# @scheduler.task('cron', id='do_job_3', day='*', hour='13', minute='26', second='05')
# def job4():
#     print(str(datetime.datetime.now()) + ' Job 4 executed')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
# import datetime
from app.api.investmentV1.scheduler.tasking.batchFiles import readFile
from app.api.investmentV1.scheduler.tasking.coreIndex import createOrUpdateCoreIndex
from app.config.development import DevelopmentConfig

# 定义全局变量
app = Flask(__name__)

# 加载配置
app.config.from_object(DevelopmentConfig())

# 创建全局的数据库连接对象，一个数据库连接对象下执行与同一个session
job_conn1 = SQLAlchemy(app)
job_conn2 = SQLAlchemy(app)

# 获取定时器对象
scheduler = APScheduler()

# 核心指标文件地址
path_coreIndex = DevelopmentConfig.BATCH_FILES_PATH_CORE_INDEX


# 定时任务实现代码：预读excel文件
@scheduler.task('interval', id='do_job_1', seconds=45, misfire_grace_time=900)
def read_core_index_excel():
    # 创建局部数据库对象
    # print(str(datetime.datetime.now()) + ' Job 1 executed')
    app.logger.info('Job 1 executed-读取核心指标文件')
    try:
        readFile(job_conn1, path_coreIndex)
    except Exception as e:
        app.logger.error('读取核心指标文件失败，开始事务回滚:' + str(e))
        job_conn1.session.rollback()


# 定时任务实现代码：将excel数据导入数据库
@scheduler.task('interval', id='do_job_2', seconds=180, misfire_grace_time=900)
def import_core_index_data():
    # 创建局部数据库对象
    # print(str(datetime.datetime.now()) + ' Job 2 executed')
    app.logger.info('Job 2 executed-核心指标数据计算入库')
    try:
        createOrUpdateCoreIndex(job_conn2)
        job_conn2.session.commit()
    except Exception as e:
        app.logger.error('核心指标数据入库失败:' + str(e))
        job_conn2.session.rollback()


# 执行定时任务
def executeJob():
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()


# 测试函数
# if __name__ == '__main__':
#     executeJob()
#     app.run(port=5000)
