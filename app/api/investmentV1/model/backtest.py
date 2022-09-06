from lin import InfoCrud
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func


# 核心指标回测表
class MbaCoreIndexBack(InfoCrud):
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


# 财务分析指标回测表（盈利指标和每股指标）
class MbaFinAnalysisIndexBack(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    periods = Column(Integer, primary_key=True, comment='期数')
    roe_avg = Column(String(30), comment='净资产收益率ROE(平均)')
    roe_basic = Column(String(30), comment='净资产收益率ROE(加权)')
    roa = Column(String(30), comment='总资产净利率ROA')
    gross_profit_margin = Column(String(30), comment='销售毛利率')
    net_profit_margin = Column(String(30), comment='销售净利率')
    tot_ope_rev = Column(String(30), comment='营业总收入[单位]元')
    ope_rev = Column(String(30), comment='营业收入[单位]元')
    goodwill = Column(String(30), comment='商誉[单位]元')
    r_and_d_costs = Column(String(30), comment='开发支出[单位]元')
    segment_sales = Column(Text(2000), comment='主营收入构成')
    debt_to_assets = Column(String(30), comment='资产负债率')
    cash_to_current_debt = Column(String(30), comment='现金比率')
    pe = Column(String(30), comment='市盈率PE')
    pb = Column(String(30), comment='市净率PB')
    gr_ps = Column(String(30), comment='每股营业总收入')
    or_ps = Column(String(30), comment='每股营业收入')
    cf_ps = Column(String(30), comment='每股现金流量净额')
    eps_basic = Column(String(30), comment='每股收益EPS-基本')
    bps = Column(String(30), comment='每股净资产BPS')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    @staticmethod
    def key_to_list():
        keys_list = [
            'code', 'code_name', 'roe_avg', 'roe_basic', 'roa',
            'gross_profit_margin', 'net_profit_margin', 'tot_ope_rev', 'ope_rev', 'goodwill',
            'r_and_d_costs', 'segment_sales', 'debt_to_assets', 'cash_to_current_debt', 'pe',
            'pb', 'gr_ps', 'or_ps', 'cf_ps', 'eps_basic', 'bps'
        ]
        return keys_list


# 区间涨幅(常用)表
class MbaRangeRiseCommon(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    periods = Column(Integer, primary_key=True, comment='期数')
    day_rise = Column(String(20), nullable=False, comment='天涨幅')
    week_rise = Column(String(20), nullable=False, comment='周涨幅')
    month_rise = Column(String(20), nullable=False, comment='月涨幅')
    quarter_rise = Column(String(5), nullable=False, comment='季度涨幅')
    half_year_rise = Column(Integer, default=0, comment='半年涨幅')
    year_rise = Column(DateTime, comment='年涨幅')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        range_rise_common = {
            'code': self.code,
            'code_name': self.code_name,
            'periods': self.periods,
            'day_rise': self.day_rise,
            'week_rise': self.week_rise,
            'month_rise': self.month_rise,
            'quarter_rise': self.quarter_rise,
            'half_year_rise': self.half_year_rise,
            'year_rise': self.year_rise,
            'create_time': self.create_time,
            'update_time': self.update_time
        }
        return range_rise_common


# 区间涨幅(扩展)表
class MbaRangeRiseRare(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    periods = Column(Integer, primary_key=True, comment='期数')
    recent_three_years = Column(String(20), nullable=False, comment='近三年涨幅')
    recent_five_years = Column(String(20), nullable=False, comment='近五年涨幅')
    recent_ten_years = Column(String(20), nullable=False, comment='近十年涨幅')
    reserved_year1 = Column(String(5), nullable=False, comment='预留涨幅1')
    reserved_year2 = Column(Integer, comment='预留涨幅2')
    reserved_year3 = Column(DateTime, comment='预留涨幅3')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        range_rise_rare = {
            'code': self.code,
            'code_name': self.code_name,
            'periods': self.periods,
            'recent_three_years': self.recent_three_years,
            'recent_five_years': self.recent_five_years,
            'recent_ten_years': self.recent_ten_years,
            'reserved_year1': self.reserved_year1,
            'reserved_year2': self.reserved_year2,
            'reserved_year3': self.reserved_year3,
            'create_time': self.create_time,
            'update_time': self.update_time
        }
        return range_rise_rare
