from lin import InfoCrud
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


# 股票上市日期计算表（是否新股）
class MbaListingDateCal(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    is_new_shares = Column(String(1), nullable=False, comment='是否新股')
    listing_day = Column(Integer, comment='上市天数')
    ipo_date = Column(DateTime, nullable=False, comment='上市日期')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
