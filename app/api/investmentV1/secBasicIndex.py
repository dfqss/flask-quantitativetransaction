from flask import Blueprint, request
from app.api.investmentV1.model.secBasicIndex import MbaSecBasicIndex

secBasicIndex_api = Blueprint("secBasicIndex", __name__)


# 查询证券基础指标列表
@secBasicIndex_api.route("/getSecBasicIndexList", methods=["post"])
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
        filterList.append(MbaSecBasicIndex.code == code)
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaSecBasicIndex.code_name == codeName)
    # 分页查询
    dataList = MbaSecBasicIndex.query.filter(*filterList)\
        .order_by(MbaSecBasicIndex.code)\
        .offset(startIndex).limit(pageSize).all()
    # 获取分页总条数
    totalNum = MbaSecBasicIndex.query.filter(*filterList).count()
    # 返回参数信息
    returnDict = dict()
    returnDict['dataList'] = dataList
    returnDict['totalNum'] = totalNum
    return returnDict
