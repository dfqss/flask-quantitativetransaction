from flask import Blueprint, request, Flask

from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.finAnalysisIndex import MbaFinAnalysisIndex
from app.api.investmentV1.model.coreIndex import MbaCoreIndex

app = Flask(__name__)
finAnalysisIndex_api = Blueprint("finAnalysisIndex", __name__)


# 查询财务分析指标（盈利指标和每股指标）列表
@finAnalysisIndex_api.route("/getFinAnalysisIndexList", methods=["post"])
# @login_required
def getFinAnalysisIndexList():
    params = request.json
    app.logger.info('start service getFinAnalysisIndexList------服务入参：' + str(params))
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
        filterList.append(MbaFinAnalysisIndex.code.startswith(code))
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaFinAnalysisIndex.code_name.startswith(codeName))
    try:
        if flag is not None and len(flag.strip()) > 0 and flag == 'byCode':
            # 分页查询
            filterList.append(MbaCoreIndex.status == 0)
            dataList = MbaFinAnalysisIndex.query.filter(*filterList) \
                .outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaFinAnalysisIndex.code) \
                .order_by(MbaFinAnalysisIndex.code) \
                .offset(startIndex).limit(pageSize).all()
            totalNum = MbaFinAnalysisIndex.query.filter(*filterList). \
                outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaFinAnalysisIndex.code).count()
        else:
            # 分页查询
            dataList = MbaFinAnalysisIndex.query.filter(*filterList) \
                .order_by(MbaFinAnalysisIndex.code) \
                .offset(startIndex).limit(pageSize).all()
            # 获取分页总条数
            totalNum = MbaFinAnalysisIndex.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询财务分析指标信息失败:' + str(e))
        return failed(10206)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getFinAnalysisIndexList------服务出参：' + str(successMap))
    return successMap
