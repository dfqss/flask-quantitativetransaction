from flask import Blueprint, request
from app.api.investmentV1.model.stockPool import MbaStockPool
from app.api.investmentV1.model.industryClass import MbaIndustryClass
# end 模型必须引用后才能在数据库初始化对应表
from lin import db
from itertools import zip_longest
StockPool_api = Blueprint("stockPool", __name__)

#查询股票池
@StockPool_api.route("/getStockPoolList", methods=["post"])
# @login_required
def getStockPoolList():
    params = request.json
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    # 拼接条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaStockPool.code == code)
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaStockPool.code_name == codeName)
    # 分页查询
    pageData = db.session.query(MbaStockPool.code,
                                MbaStockPool.code_name,
                                MbaStockPool.periods,
                                MbaStockPool.create_time,
                                MbaIndustryClass.industry_sw,
                                MbaIndustryClass.industry_cit)\
        .outerjoin(MbaIndustryClass, MbaStockPool.code == MbaIndustryClass.code)\
        .filter(*filterList).order_by(MbaStockPool.code)\
        .offset(startIndex).limit(pageSize).all()
    # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
    mapList = ['code', 'codeName', 'periods', 'create_time', 'industry_sw', 'industry_cit']
    dataList = []
    for returnData in pageData:
        dataList.append(dict(zip_longest(mapList, returnData)))
    # 获取分页总条数
    totalNum = MbaStockPool.query.filter(*filterList).count()
    # 返回参数信息
    returnDict = dict()
    returnDict['dataList'] = dataList
    returnDict['totalNum'] = totalNum
    return returnDict

