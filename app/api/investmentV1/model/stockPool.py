from lin import InfoCrud
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


# 核心指标表
class MbaStockPool(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    periods = Column(Integer, comment='期数')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
