from lin import InfoCrud
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func


# 财务分析指标（盈利指标和每股指标）
class MbaFinAnalysisIndex(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
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
