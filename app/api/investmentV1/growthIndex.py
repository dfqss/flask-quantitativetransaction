from flask import Blueprint, request, Flask

from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.growthIndex import MbaGrowthIndex

app = Flask(__name__)
growthIndex_api = Blueprint("growthIndex", __name__)


@growthIndex_api.route("/getGrowthIndex", methods=["post"])
# @login_required
def getGrowthIndex():
    params = request.json
    app.logger.info('start service getGrowthIndex------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    # 拼接条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaGrowthIndex.code.startswith(code))
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaGrowthIndex.code_name.startswith(codeName))
    try:
        # 分页查询
        dataList = MbaGrowthIndex.query.filter(*filterList) \
            .order_by(MbaGrowthIndex.code) \
            .offset(startIndex).limit(pageSize).all()
        # 获取分页总条数
        totalNum = MbaGrowthIndex.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询成长指标信息失败:' + str(e))
        return failed(10207)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getGrowthIndex------服务出参：' + str(successMap))
    return successMap
