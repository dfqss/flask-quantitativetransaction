from lin import InfoCrud
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


# 股票估值
class MbaStockValue(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    ev = Column(String(30), comment='总市值1[单位]元')
    mkt_cap_float = Column(String(30), comment='流通市值(含限售股)[单位]元')
    mkt_free_shares = Column(String(30), comment='自由流通市值[单位]元')
    pb_mrq = Column(String(30), comment='市净率PB(MRQ)')
    pb_lyr = Column(String(30), comment='市净率PB(LYR)')
    gr_ttm = Column(String(30), comment='营业总收入(TTM)_PIT[单位]元')
    or_ttm = Column(String(30), comment='营业收入(TTM)_VAL_PIT[单位]元')
    profit_ttm = Column(String(30), comment='净利润(TTM)_PIT[单位]元')
    eps_ttm = Column(String(30), comment='每股收益EPS(TTM)_PIT')
    or_ps_ttm = Column(String(30), comment='每股营业收入(TTM)_PIT')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    @staticmethod
    def key_to_list():
        keys_list = [
            'code', 'code_name', 'ev', 'mkt_cap_float', 'mkt_free_shares',
            'pb_mrq', 'pb_lyr', 'gr_ttm', 'or_ttm', 'profit_ttm',
            'eps_ttm', 'or_ps_ttm'
        ]
        return keys_list
