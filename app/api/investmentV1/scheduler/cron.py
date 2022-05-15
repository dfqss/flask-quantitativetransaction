"""
# coding:utf-8
@Time    : 2022/04/30
@Author  : sushuai
@desc    : cron启动任务（demo代码）
@notes   : 使用时将业务代码写入task函数中，并在需要的时候调用executeJob函数执行定时任务
"""

from flask import Flask
import datetime
from flask_apscheduler import APScheduler

aps = APScheduler()

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'scheduler:task',
            'args': (1, 2),
            'trigger': 'cron',
            'day': '*',
            'hour': '13',
            'minute': '16',
            'second': '20'
        }
    ]
    SCHEDULER_API_ENABLED = True

# 定时任务实现代码
def task(a, b):
    print(str(datetime.datetime.now()) + ' execute task ' + '{}+{}={}'.format(a, b, a + b))

# 执行定时任务
def executeJob():
    app = Flask(__name__)
    app.config.from_object(Config())
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

# 测试函数
if __name__ == '__main__':
    executeJob()
    app.run(port=5000)