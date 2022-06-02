from flask import Blueprint, request
from app.api.investmentV1.model.stockValue import MbaStockValue

stockValue_api = Blueprint("stockValue", __name__)


# 查询股票估值列表
@stockValue_api.route("/getStockValueList", methods=["post"])
# @login_required
def getSecBasicIndexList():
    params = request.json
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    # 拼接查询条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaStockValue.code == code)
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaStockValue.code_name == codeName)
    # 分页查询
    dataList = MbaStockValue.query.filter(*filterList)\
        .order_by(MbaStockValue.code)\
        .offset(startIndex).limit(pageSize).all()
    # 获取分页总条数
    totalNum = MbaStockValue.query.filter(*filterList).count()
    # 返回参数信息
    returnDict = dict()
    returnDict['dataList'] = dataList
    returnDict['totalNum'] = totalNum
    return returnDict
