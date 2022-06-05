from lin import InfoCrud
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


# 证券基础指标
class MbaSecBasicIndex(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    total_shares = Column(String(30), comment='总股本[单位]股')
    free_float_shares = Column(String(30), comment='自由流通股本[单位]股')
    share_issuing_mkt = Column(String(30), comment='流通股本[单位]股')
    rt_mkt_cap = Column(String(30), comment='总市值')
    rt_float_mkt_cap = Column(String(30), comment='流通市值')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    @staticmethod
    def key_to_list():
        keys_list = [
            'code', 'code_name', 'total_shares', 'free_float_shares', 'share_issuing_mkt',
            'rt_mkt_cap', 'rt_float_mkt_cap'
        ]
        return keys_list
