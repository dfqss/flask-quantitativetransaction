from lin import InfoCrud
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


# 股票上市日期计算表（是否新股）
class MbaListingDateCal(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    is_new_shares = Column(String(1), nullable=False, comment='是否新股 新股-N 非新股-F 次新股-C')
    listing_day = Column(Integer, comment='上市天数')
    ipo_date = Column(DateTime, nullable=False, comment='上市日期')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def to_dict(self):
        listing_date = {
            'code': self.code,
            'is_new_shares': self.is_new_shares,
            'listing_day': self.listing_day,
            'ipo_date': self.ipo_date,
            'create_time': self.create_time,
            'update_time': self.update_time
        }
        return listing_date


# 股票上市日期
class MbaShares(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    name = Column(String(30), comment='股票名称')
    ipo_date = Column(DateTime, nullable=False, comment='上市日期')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
