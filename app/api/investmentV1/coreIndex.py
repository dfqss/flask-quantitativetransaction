from lin import NotFound
from flask import Blueprint, request, Flask
# start 模型必须引用后才能在数据库初始化对应表
from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.coreIndex import MbaCoreIndex
from app.api.investmentV1.model.coreIndex import MbaCoreIndexHist
from app.api.investmentV1.model.listingDateCal import MbaListingDateCal
from app.api.investmentV1.model.stockPool import MbaStockPool
from app.util.common import addFieldByConditions
# end 模型必须引用后才能在数据库初始化对应表
from sqlalchemy import func
from lin import db
from itertools import zip_longest
from sqlalchemy import or_, and_, not_
# from flask import jsonify

app = Flask(__name__)
coreIndex_api = Blueprint("coreIndex", __name__)


# 核心指数分页查询
@coreIndex_api.route("/getCoreIndexList", methods=["post"])
# @login_required
def getCoreIndexList():
    params = request.json
    app.logger.info('start service getCoreIndexList------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    # 拼接查询条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaCoreIndex.code.startswith(code))
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaCoreIndex.code_name.startswith(codeName))
    # 查询展示状态为 0-展示 的数据
    filterList.append(MbaCoreIndex.status == '0')
    # 分页查询
    try:
        pageData = db.session.query(MbaCoreIndex.code,
                                    MbaCoreIndex.code_name,
                                    MbaCoreIndex.final_cal_core,
                                    MbaCoreIndex.show_times,
                                    MbaCoreIndex.periods,
                                    MbaCoreIndex.cal_date,
                                    MbaListingDateCal.is_new_shares,
                                    MbaStockPool.in_pool_status) \
            .outerjoin(MbaListingDateCal, MbaCoreIndex.code == MbaListingDateCal.code) \
            .outerjoin(MbaStockPool, MbaCoreIndex.code == MbaStockPool.code) \
            .filter(*filterList) \
            .order_by(MbaCoreIndex.code) \
            .offset(startIndex).limit(pageSize).all()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'finalCalCore', 'showTimes', 'periods',
                   'calDate', 'isNewShares', 'inPoolStatus']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
        # 获取分页总条数
        totalNum = MbaCoreIndex.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询核心指数失败:' + str(e))
        return failed(10202)
    # 添加资本市场指标
    dataList = addFieldByConditions(dataList)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getCoreIndexList------服务出参：' + str(successMap))
    return successMap


# 查询核心指数历史记录分页查询
@coreIndex_api.route("/getCoreIndexHistoryList", methods=["post"])
# @login_required
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
                                    MbaCoreIndexHist.final_cal_core,
                                    MbaCoreIndexHist.cal_date,
                                    MbaCoreIndexHist.periods,
                                    MbaListingDateCal.is_new_shares) \
            .outerjoin(MbaListingDateCal, MbaCoreIndexHist.code == MbaListingDateCal.code) \
            .filter(*filterList) \
            .order_by(MbaCoreIndexHist.periods, MbaCoreIndexHist.code) \
            .offset(startIndex).limit(pageSize).all()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'finalCalCore', 'calDate', 'periods', 'isNewShares']
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


# 根据股票编码：code查询核心指数信息
@coreIndex_api.route('/<id>', methods=['GET'])
def get_coreIndex(id):
    coreIndex = MbaCoreIndex.query.filter_by(code=id).first()
    if coreIndex:
        return coreIndex
    raise NotFound('没有找到对应的股票代码')


# 查询全部的核心指数列表
@coreIndex_api.route("")
def get_all_coreIndex():
    return MbaCoreIndex.get(one=False)


# 核心指数分页查询
@coreIndex_api.route('/getCoreIndexByPage/<int:page>,<int:limit>', methods=["GET"])
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
