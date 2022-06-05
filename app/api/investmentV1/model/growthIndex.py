from lin import InfoCrud
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


# 成长指标
class MbaGrowthIndex(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    yoy_eps_basic = Column(String(30), comment='基本每股收益(同比增长率)')
    yoy_tr = Column(String(30), comment='营业总收入(同比增长率)')
    yoy_or = Column(String(30), comment='营业收入(同比增长率)')
    yoy_op = Column(String(30), comment='营业利润(同比增长率)')
    yoy_ebt = Column(String(30), comment='利润总额(同比增长率)')
    yoy_profit = Column(String(30), comment='净利润(同比增长率)')
    yoy_equity = Column(String(30), comment='净资产(同比增长率)')
    fa_yoy = Column(String(30), comment='研发费用同比增长')
    yoy_debt = Column(String(30), comment='总负债(同比增长率)')
    yoy_assets_tb = Column(String(30), comment='总资产(同比增长率)')
    yoy_bps = Column(String(30), comment='每股净资产(相对年初增长率)')
    yoy_assets_hb = Column(String(30), comment='资产总计(相对年初增长率)')
    growth_gr = Column(String(30), comment='营业总收入(N年,增长率)')
    growth_gc = Column(String(30), comment='营业总成本(N年,增长率)')
    growth_or = Column(String(30), comment='营业收入(N年,增长率)')
    growth_op = Column(String(30), comment='营业利润(N年,增长率)')
    qfa_cgr_sales = Column(String(30), comment='单季度.营业收入环比增长率')
    qfa_cgr_op = Column(String(30), comment='单季度.营业利润环比增长率')
    qfa_cgr_profit = Column(String(30), comment='单季度.净利润环比增长率')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    @staticmethod
    def key_to_list():
        keys_list = [
            'code', 'code_name', 'yoy_eps_basic', 'yoy_tr', 'yoy_or',
            'yoy_op', 'yoy_ebt', 'yoy_profit', 'yoy_equity', 'fa_yoy',
            'yoy_debt', 'yoy_assets_tb', 'yoy_bps', 'yoy_assets_hb', 'growth_gr',
            'growth_gc', 'growth_or', 'growth_op', 'qfa_cgr_sales', 'qfa_cgr_op', 'qfa_cgr_profit'
        ]
        return keys_list
