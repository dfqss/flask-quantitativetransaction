from flask import Blueprint, request, Flask

from app.api.investmentV1.exception.result import failed, success
from app.api.investmentV1.model.dupontAnalysisIndex import MbaDupontAnalysisIndex
from app.api.investmentV1.model.coreIndex import MbaCoreIndex

app = Flask(__name__)
dupontAnalysisIndex_api = Blueprint("dupontAnalysisIndex", __name__)


@dupontAnalysisIndex_api.route("/getDupontAnalysisIndex", methods=["post"])
# @login_required
def getDupontAnalysisIndex():
    params = request.json
    app.logger.info('start service getDupontAnalysisIndex------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    flag = params.get('flag')
    startIndex = (pageNum - 1) * pageSize
    # 拼接条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaDupontAnalysisIndex.code.startswith(code))
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaDupontAnalysisIndex.code_name.startswith(codeName))
    try:
        totalNum = 0
        if flag is not None and len(flag.strip()) > 0 and flag == 'byCode':
            # 分页查询
            filterList.append(MbaCoreIndex.status == 0)
            dataList = MbaDupontAnalysisIndex.query.filter(*filterList) \
                .outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaDupontAnalysisIndex.code) \
                .order_by(MbaDupontAnalysisIndex.code) \
                .offset(startIndex).limit(pageSize).all()
            totalNum = MbaDupontAnalysisIndex.query.filter(*filterList).\
                outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaDupontAnalysisIndex.code).count()
        else:
            # 分页查询
            dataList = MbaDupontAnalysisIndex.query.filter(*filterList) \
                .order_by(MbaDupontAnalysisIndex.code) \
                .offset(startIndex).limit(pageSize).all()
            # 获取分页总条数
            totalNum = MbaDupontAnalysisIndex.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询杜邦指标信息失败:' + str(e))
        return failed(10205)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getDupontAnalysisIndex------服务出参：' + str(successMap))
    return successMap


