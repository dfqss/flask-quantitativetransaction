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
import datetime
from app.api.investmentV1.scheduler.tasking.batchFiles import readFile
from app.api.investmentV1.scheduler.tasking.coreIndex import createOrUpdateCoreIndex
from app.config.development import DevelopmentConfig

# 定义全局变量
app = Flask(__name__)

# 加载数据配置
app.config.from_object(DevelopmentConfig())

# 创建一个全局的数据库连接对象，一个数据库连接对象下执行与同一个session
# conn = SQLAlchemy(app)

# 获取定时器对象
scheduler = APScheduler()

# 核心指标文件地址
path_coreIndex = DevelopmentConfig.BATCH_FILES_PATH_CORE_INDEX


# 定时任务实现代码：预读excel文件
@scheduler.task('interval', id='do_job_1', seconds=15, misfire_grace_time=900)
def read_core_index_excel():
    # 创建局部数据库对象
    conn = SQLAlchemy(app)
    print(str(datetime.datetime.now()) + ' Job 1 executed')
    readFile(conn, path_coreIndex)


# 定时任务实现代码：将excel数据导入数据库
@scheduler.task('interval', id='do_job_2', seconds=120, misfire_grace_time=900)
def import_core_index_data():
    # 创建局部数据库对象
    conn = SQLAlchemy(app)
    print(str(datetime.datetime.now()) + ' Job 2 executed')
    try:
        createOrUpdateCoreIndex(conn)
        conn.session.commit()
    except Exception as e:
        print('开始回滚数据:' + str(e))
        conn.session.rollback()


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
