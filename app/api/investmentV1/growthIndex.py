from flask import Blueprint, request
from app.api.investmentV1.model.growthIndex import MbaGrowthIndex

growthIndex_api = Blueprint("growthIndex", __name__)


@growthIndex_api.route("/getGrowthIndex", methods=["post"])
# @login_required
def getGrowthIndex():
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
        filterList.append(MbaGrowthIndex.code == code)
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaGrowthIndex.code_name == codeName)
    # 分页查询
    dataList = MbaGrowthIndex.query.filter(*filterList) \
        .order_by(MbaGrowthIndex.code) \
        .offset(startIndex).limit(pageSize).all()
    # 获取分页总条数
    totalNum = MbaGrowthIndex.query.filter(*filterList).count()
    # 返回参数信息
    returnDict = dict()
    returnDict['dataList'] = dataList
    returnDict['totalNum'] = totalNum
    return returnDict
