from flask import Blueprint, request, Flask
from lin import login_required

from app.api.investmentV1.model.stockValue import MbaStockValue
from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.coreIndex import MbaCoreIndex

app = Flask(__name__)
stockValue_api = Blueprint("stockValue", __name__)


# 查询股票估值列表
@stockValue_api.route("/getStockValueList", methods=["post"])
@login_required
def getSecBasicIndexList():
    params = request.json
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    flag = params.get('flag')
    # 拼接查询条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaStockValue.code == code)
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaStockValue.code_name == codeName)
    # 分页查询
    try:
        if flag is not None and len(flag.strip()) > 0 and flag == 'byCode':
            # 分页查询
            filterList.append(MbaCoreIndex.status == 0)
            dataList = MbaStockValue.query.filter(*filterList) \
                .outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaStockValue.code) \
                .order_by(MbaStockValue.code) \
                .offset(startIndex).limit(pageSize).all()
            totalNum = MbaStockValue.query.filter(*filterList). \
                outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaStockValue.code).count()
        else:
            dataList = MbaStockValue.query.filter(*filterList) \
                .order_by(MbaStockValue.code) \
                .offset(startIndex).limit(pageSize).all()
            # 获取分页总条数
            totalNum = MbaStockValue.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询股票估值信息失败:' + str(e))
        return failed(10303)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    return successMap
