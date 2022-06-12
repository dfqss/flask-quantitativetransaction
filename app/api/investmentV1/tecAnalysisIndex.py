from flask import Blueprint, request, Flask
from app.api.investmentV1.model.tecAnalysisIndex import MbaTecAnalysisIndex
from app.api.investmentV1.exception.result import success, failed

app = Flask(__name__)
tecAnalysisIndex_api = Blueprint("tecAnalysisIndex", __name__)


# 查询技术分析指标列表
@tecAnalysisIndex_api.route("/getTecAnalysisIndexList", methods=["post"])
# @login_required
def getTecAnalysisIndexList():
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
        filterList.append(MbaTecAnalysisIndex.code == code)
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaTecAnalysisIndex.code_name == codeName)
    # 分页查询
    try:
        dataList = MbaTecAnalysisIndex.query.filter(*filterList) \
            .order_by(MbaTecAnalysisIndex.code) \
            .offset(startIndex).limit(pageSize).all()
        # 获取分页总条数
        totalNum = MbaTecAnalysisIndex.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询技术分析指标失败:' + str(e))
        return failed(10304)
    # 返回参数信息
    successMap = success()
    returnDict = dict()
    returnDict['dataList'] = dataList
    returnDict['totalNum'] = totalNum
    return returnDict
