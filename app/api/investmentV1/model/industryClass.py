from lin import InfoCrud
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


# 行业分类
class MbaIndustryClass(InfoCrud):
    code = Column(String(30), primary_key=True, comment='股票编码')
    code_name = Column(String(60), comment='股票名称')
    industry_sw_code = Column(String(30), comment='所属申万行业代码')
    industry_sw = Column(String(60), comment='所属申万行业名称')
    industry_cit_code = Column(String(30), comment='所属中信行业代码')
    industry_cit = Column(String(60), comment='所属中信行业名称')

    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    @staticmethod
    def key_to_list():
        keys_list = [
            'code', 'code_name', 'industry_sw', 'industry_sw_code', 'industry_cit',
            'industry_cit_code'
        ]
        return keys_list
