from lin import InfoCrud
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


# 核心指标表
class MbaCoreIndex(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    current_core = Column(String(20), nullable=False, comment='最新核心指标')
    period_core = Column(String(20), nullable=False, comment='次新核心指标')
    final_cal_core = Column(String(20), nullable=False, comment='最终计算核心指数')
    periods = Column(Integer, comment='期数')
    status = Column(String(5), nullable=False, comment='展示状态：0-展示 1-不展示')
    show_times = Column(Integer, default=0, comment='展示次数')
    cal_date = Column(DateTime, comment='计算日期')
    report_date = Column(DateTime, comment='报告日期')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        core_index = {
            'code': self.code,
            'code_name': self.code_name,
            'current_core': self.current_core,
            'period_core': self.period_core,
            'final_cal_core': self.final_cal_core,
            'periods': self.periods,
            'status': self.status,
            'show_times': self.show_times,
            'cal_date': self.cal_date,
            'report_date': self.report_date,
            'create_time': self.create_time,
            'update_time': self.update_time
        }
        return core_index


# 核心指标历史表
class MbaCoreIndexHist(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    current_core = Column(String(20), nullable=False, comment='最新核心指标')
    period_core = Column(String(20), nullable=False, comment='次新核心指标')
    final_cal_core = Column(String(20), nullable=False, comment='最终计算核心指数')
    periods = Column(Integer, primary_key=True, comment='期数')
    status = Column(String(5), nullable=False, comment='展示状态：0-展示 1-不展示')
    show_times = Column(Integer, default=0, comment='展示次数')
    cal_date = Column(DateTime, comment='计算日期')
    report_date = Column(DateTime, comment='报告日期')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        core_index_hist = {
            'code': self.code,
            'code_name': self.code_name,
            'current_core': self.current_core,
            'period_core': self.period_core,
            'final_cal_core': self.final_cal_core,
            'periods': self.periods,
            'status': self.status,
            'show_times': self.show_times,
            'cal_date': self.cal_date,
            'report_date': self.report_date,
            'create_time': self.create_time,
            'update_time': self.update_time
        }
        return core_index_hist
