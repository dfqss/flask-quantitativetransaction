from lin import NotFound, login_required, permission_meta, group_required
from flask import Blueprint, request, Flask
# start 模型必须引用后才能在数据库初始化对应表
from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.coreIndex import MbaCoreIndex
from app.api.investmentV1.model.coreIndex import MbaCoreIndexHist
from app.api.investmentV1.model.industryClass import MbaIndustryClass
from app.api.investmentV1.model.listingDateCal import MbaListingDateCal
from app.api.investmentV1.model.stockPool import MbaStockPool
from app.util.common import addFieldByConditions, judgeOrder
# end 模型必须引用后才能在数据库初始化对应表
from sqlalchemy import func
from lin import db
from datetime import datetime
from itertools import zip_longest
from sqlalchemy import or_, and_, not_

# from flask import jsonify

app = Flask(__name__)
coreIndex_api = Blueprint("coreIndex", __name__)


# 核心指数分页查询
@coreIndex_api.route("/getCoreIndexList", methods=["post"])
@login_required
def getCoreIndexList():
    params = request.json
    app.logger.info('start service getCoreIndexList------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    orderBy = params.get('orderBy')
    flag = params.get('flag')
    isNewShares = params.get('isNewShares')
    isShowTimes = params.get('isShowTimes')
    startIndex = (pageNum - 1) * pageSize
    # 拼接查询条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaCoreIndex.code.startswith(code))
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaCoreIndex.code_name.startswith(codeName))
    # 根据是否新股查询
    if isNewShares is not None and len(isNewShares.strip()) > 0:
        filterList.append(MbaListingDateCal.is_new_shares == isNewShares)
    # 根据是否本期新增查询
    if isShowTimes is not None and len(isShowTimes.strip()) > 0:
        if isShowTimes == 'Y':
            filterList.append(MbaCoreIndex.show_times == 1)
        elif isShowTimes == 'N':
            filterList.append(MbaCoreIndex.show_times != 1)
    # 根据排序字段查询排序
    if orderBy is not None and len(orderBy.strip()) > 0:
        orderByList = judgeOrder(orderBy, flag, "code", "cal_date", "final_cal_core",
                                 "pre_final_cal_core")
    # 查询展示状态为 0-展示 的数据
    filterList.append(MbaCoreIndex.status == '0')
    filterList.append(MbaCoreIndexHist.periods == MbaCoreIndex.periods - 1)
    # 分页查询
    try:
        pageData = db.session.query(MbaCoreIndex.code,
                                    MbaCoreIndex.code_name,
                                    MbaCoreIndex.final_cal_core,
                                    MbaCoreIndex.show_times,
                                    MbaCoreIndex.periods,
                                    MbaCoreIndex.cal_date,
                                    MbaCoreIndex.report_date,
                                    MbaIndustryClass.industry_sw,
                                    MbaListingDateCal.is_new_shares,
                                    MbaStockPool.in_pool_status,
                                    MbaCoreIndexHist.final_cal_core.label("pre_final_cal_core")) \
            .outerjoin(MbaListingDateCal, MbaCoreIndex.code == MbaListingDateCal.code) \
            .outerjoin(MbaStockPool, MbaCoreIndex.code == MbaStockPool.code) \
            .outerjoin(MbaIndustryClass, MbaCoreIndex.code == MbaIndustryClass.code) \
            .outerjoin(MbaCoreIndexHist, MbaCoreIndex.code == MbaCoreIndexHist.code) \
            .filter(*filterList) \
            .order_by(*orderByList) \
            .offset(startIndex).limit(pageSize).all()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'finalCalCore', 'showTimes', 'periods',
                   'calDate', 'reportDate', 'industrySw', 'isNewShares', 'inPoolStatus',
                   'preFinalCalCore']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
        # 将list中的sql模板对象属性由datetime转为字符串类型
        dataList = datetimeToString(dataList, "calDate")
        dataList = datetimeToString(dataList, "reportDate")
        # 获取分页总条数
        totalNum = MbaCoreIndex.query \
            .outerjoin(MbaListingDateCal, MbaCoreIndex.code == MbaListingDateCal.code) \
            .outerjoin(MbaStockPool, MbaCoreIndex.code == MbaStockPool.code) \
            .outerjoin(MbaIndustryClass, MbaCoreIndex.code == MbaIndustryClass.code) \
            .outerjoin(MbaCoreIndexHist, MbaCoreIndex.code == MbaCoreIndexHist.code) \
            .filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询核心指数失败:' + str(e))
        return failed(10202)
    # 添加资本市场指标
    dataList = addFieldByConditions(dataList)
    # 返回参数信息
    successMap = success()
    if dataList is not None and len(dataList) > 0:
        successMap['periods'] = dataList[0]['periods']
    else:
        successMap['periods'] = 0
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getCoreIndexList------服务出参：' + str(successMap))
    return successMap


# 查询核心指数历史记录分页查询
@coreIndex_api.route("/getCoreIndexHistoryList", methods=["post"])
@login_required
def getCoreIndexHistoryList():
    params = request.json
    app.logger.info('start service getCoreIndexHistoryList------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    calDate = params.get('calDate')
    periods = params.get('periods')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    # 拼接查询条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaCoreIndexHist.code.startswith(code))
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaCoreIndexHist.code_name.startswith(codeName))
    # 根据时间戳查询
    if calDate is not None and len(calDate.strip()) > 0:
        filterList.append(func.date_format(calDate, "%Y-%m-%d") ==
                          func.date_format(MbaCoreIndexHist.cal_date, "%Y-%m-%d"))
    # 根据期数查询
    if periods is not None and len(periods.strip()) > 0:
        filterList.append(MbaCoreIndexHist.periods == periods)
    try:
        # 分页查询
        pageData = db.session.query(MbaCoreIndexHist.code,
                                    MbaCoreIndexHist.code_name,
                                    MbaCoreIndexHist.current_core,
                                    MbaCoreIndexHist.period_core,
                                    MbaCoreIndexHist.final_cal_core,
                                    MbaCoreIndexHist.cal_date,
                                    MbaCoreIndexHist.periods,
                                    MbaListingDateCal.is_new_shares) \
            .outerjoin(MbaListingDateCal, MbaCoreIndexHist.code == MbaListingDateCal.code) \
            .filter(*filterList) \
            .order_by(MbaCoreIndexHist.periods, MbaCoreIndexHist.code) \
            .offset(startIndex).limit(pageSize).all()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'currentCore', 'periodCore', 'finalCalCore', 'calDate', 'periods', 'isNewShares']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
        # 获取分页总条数
        totalNum = MbaCoreIndexHist.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询核心指数历史数据失败:' + str(e))
        return failed(10204)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getCoreIndexHistoryList------服务出参：' + str(successMap))
    return successMap


# 查询核心指数历史记录分页查询
@coreIndex_api.route("/validatePeriods", methods=["post"])
@login_required
def validatePeriods():
    params = request.json
    app.logger.info('start service validatePeriods------服务入参：' + str(params))
    periods = params.get('periods')
    try:
        if MbaCoreIndexHist.query.filter_by(periods=periods).count() < 1:
            return failed(10213)
    except Exception as e:
        app.logger.error('查询核心指数历史数据失败:' + str(e))
        return failed(10204)
    # 返回参数信息
    successMap = success(18)
    app.logger.info('end service validatePeriods------服务出参：' + str(successMap))
    return successMap


# 根据股票编码：code查询核心指数信息
@coreIndex_api.route('/<id>', methods=['GET'])
@login_required
def get_coreIndex(id):
    coreIndex = MbaCoreIndex.query.filter_by(code=id).first()
    if coreIndex:
        return coreIndex
    raise NotFound('没有找到对应的股票代码')


# 查询全部的核心指数列表
@coreIndex_api.route("")
@login_required
def get_all_coreIndex():
    return MbaCoreIndex.get(one=False)


# 核心指数分页查询
@coreIndex_api.route('/getCoreIndexByPage/<int:page>,<int:limit>', methods=["GET"])
@login_required
def get_coreIndexByPage(page, limit):
    startIndex = (page - 1) * limit
    # pageData = db.session.query(MbaCoreIndex).offset(startIndex).limit(limit)
    pageData = (
        db.session.query(MbaCoreIndex.code,
                         MbaCoreIndex.code_name,
                         MbaCoreIndex.final_cal_core,
                         MbaCoreIndex.cal_date,
                         MbaListingDateCal.is_new_shares)
            .outerjoin(MbaListingDateCal, MbaCoreIndex.code == MbaListingDateCal.code)
            .filter(and_(MbaCoreIndex.status.__eq__('0')))
            .offset(startIndex)
            .limit(limit)
    )
    # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
    mapList = ['code', 'codeName', 'finalCalCore', 'calDate', 'isNewShares']
    returnData = []
    for dataList in pageData:
        returnData.append(dict(zip_longest(mapList, dataList)))
    return returnData


# 根据code值删除核心指标
@coreIndex_api.route('/updateCoreIndexByCode', methods=["POST"])
@permission_meta(name="删除投资标初选数据", module="投资标初选", mount=True)
@group_required
@login_required
def updateCoreIndexByCode():
    params = request.json
    app.logger.info('start service updateCoreIndexByCode------服务入参：' + str(params))
    dicaDate = params.get("date")
    app.logger.info(dicaDate)
    if not isinstance(dicaDate, dict):
        dicaDate = dicaDate.to_dict()
    try:
        MbaCoreIndex.query.filter_by(code=dicaDate["code"]).update({"status": "2"})
        db.session.commit()
    except Exception as e:
        app.logger.error('根据code值删除核心指标失败:' + str(e))
        return failed(10307)
    # 返回参数信息
    successMap = success()
    app.logger.info('end service updateCoreIndexByCode------服务出参：' + str(successMap))
    return successMap


# 将list中的sql模板对象属性由datetime转为字符串类型
def datetimeToString(inList, key):
    resultList = []
    for dictDate in inList:
        resultStr = datetime.strftime(dictDate[key], '%Y-%m-%d %H:%M:%S')
        dictDate[key] = resultStr
        resultList.append(dictDate)
    return resultList
