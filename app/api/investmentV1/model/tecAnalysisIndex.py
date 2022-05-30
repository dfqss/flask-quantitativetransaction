from lin import InfoCrud
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


# 技术分析指标
class MbaTecAnalysisIndex(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    tech_bias5 = Column(String(20), comment='5日乖离率_PIT')
    breakout_ma = Column(String(20), comment='向上有效突破均线')
    breakdown_ma = Column(String(20), comment='向下有效突破均线')
    bull_bear_ma = Column(String(20), comment='均线多空头排列看涨看跌')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
