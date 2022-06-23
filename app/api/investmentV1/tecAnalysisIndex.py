from flask import Blueprint, request, Flask
from app.api.investmentV1.model.tecAnalysisIndex import MbaTecAnalysisIndex
from app.api.investmentV1.exception.result import success, failed
from lin import db

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
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    return successMap


# 根据code值更新LON和buying
@tecAnalysisIndex_api.route('/updateTecAnalysisIndexByCode', methods=["POST"])
def updateTecAnalysisIndexByCode():
    params = request.json
    app.logger.info('start service updateTecAnalysisIndexByCode------服务入参：' + str(params))
    dicaDate = params.get("date")
    app.logger.info(dicaDate)
    # 定义空字典，用来判断
    addList = {}
    if not isinstance(dicaDate, dict):
        dicaDate = dicaDate.to_dict()
    if dicaDate['LON'] is not None and len(dicaDate['LON'].strip()) > 0:
        addList['LON'] = dicaDate['LON']
    if dicaDate['buying'] is not None and len(dicaDate['buying'].strip()) > 0:
        addList['buying'] = dicaDate['buying']
    try:
        queryDate = MbaTecAnalysisIndex.query.filter_by(code=dicaDate["code"]).update(addList)
        db.session.commit()
    except Exception as e:
        app.logger.error('根据code值更新LON和buying失败:' + str(e))
        return failed(10308)
    # 返回参数信息
    successMap = success()
    app.logger.info('end service updateTecAnalysisIndexByCode------服务出参：' + str(successMap))
    return successMap
