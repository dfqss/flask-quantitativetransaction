from lin import InfoCrud
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


# 杜邦分析指标
class MbaDupontAnalysisIndex(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    roe = Column(String(30), comment='净资产收益率ROE')
    assets_turn = Column(String(30), comment='总资产周转率')
    dupont_np = Column(String(30), comment='归属母公司股东的净利润/净利润')
    profit_to_gr = Column(String(30), comment='净利润/营业总收入')
    dupont_tax_burden = Column(String(30), comment='净利润/利润总额')
    dupont_int_burden = Column(String(30), comment='利润总额/息税前利润')
    ebi_to_gr = Column(String(30), comment='息税前利润/营业总收入')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    @staticmethod
    def key_to_list():
        keys_list = [
            'code', 'code_name', 'roe', 'assets_turn', 'dupont_np',
            'profit_to_gr', 'dupont_tax_burden', 'dupont_int_burden', 'ebi_to_gr',
        ]
        return keys_list
