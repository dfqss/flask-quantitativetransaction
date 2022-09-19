from itertools import zip_longest

from flask import Blueprint, request, Flask
from lin import login_required, db
from sqlalchemy import and_

from app.api.investmentV1.coreIndex import datetimeToString
from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.backtest import MbaCoreIndexBack, MbaFinAnalysisIndexBack, \
    MbaRangeRiseRare, MbaRangeRiseCommon
from app.util.common import judgeOrder

app = Flask(__name__)
backtest_api = Blueprint("backtest", __name__)


# 查询回测列表
@backtest_api.route("/getBacktestList", methods=["post"])
@login_required
def getFinAnalysisIndexList():
    params = request.json
    app.logger.info('start service getFinAnalysisIndexList------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    periods = params.get('periods')
    calDate = params.get('calDate')
    orderByList = params.get('orderByList')
    pageSize = params.get('pageSize', 100)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    # 拼接查询条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaCoreIndexBack.code.startswith(code))
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaCoreIndexBack.code_name.startswith(codeName))
    # 根据股票期数查询
    if periods is not None and len(periods.strip()) > 0:
        filterList.append(MbaCoreIndexBack.periods == periods)
    # 根据时间区间查询
    if calDate is not None and len(calDate.strip()) > 0:
        split = str(calDate).split(',')
        filterList.append(MbaCoreIndexBack.cal_date.between(split[0], split[1]))
    # 查询展示状态为 0-展示 的数据
    filterList.append(MbaCoreIndexBack.status == '0')
    # 根据排序字段查询排序
    orderList = []
    if len(orderByList) > 0:
        orderList = getOrderList(orderByList)
    try:
        # 分页查询
        pageData = db.session.query(MbaCoreIndexBack.code,
                                    MbaCoreIndexBack.code_name,
                                    MbaCoreIndexBack.periods,
                                    MbaCoreIndexBack.final_cal_core,
                                    MbaFinAnalysisIndexBack.roe_avg,
                                    MbaRangeRiseCommon.quarter_rise,
                                    MbaRangeRiseCommon.half_year_rise,
                                    MbaCoreIndexBack.cal_date) \
            .outerjoin(MbaFinAnalysisIndexBack,
                       and_(MbaCoreIndexBack.code == MbaFinAnalysisIndexBack.code,
                            MbaCoreIndexBack.periods == MbaFinAnalysisIndexBack.periods)) \
            .outerjoin(MbaRangeRiseCommon,
                       and_(MbaCoreIndexBack.code == MbaRangeRiseCommon.code,
                            MbaCoreIndexBack.periods == MbaRangeRiseCommon.periods)) \
            .filter(*filterList) \
            .order_by(*orderList) \
            .offset(startIndex).limit(pageSize).all()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'periods', 'finalCalCore', 'roeAvg', 'quarterRise',
                   'halfYearRise', 'calDate']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
        # 将list中的sql模板对象属性由datetime转为字符串类型
        dataList = datetimeToString(dataList, "calDate")
        # 获取分页总条数
        totalNum = MbaCoreIndexBack.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询回测信息失败:' + str(e))
        return failed(10311)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getStockPoolList------服务出参：' + str(successMap))
    return successMap


# 获取排序列表
def getOrderList(orderByList):
    orderList = []
    for orderByMap in orderByList:
        orderBy = orderByMap['orderBy']
        if 'des' == orderByMap['orderType']:
            if 'code' == orderBy:
                orderList.append(MbaCoreIndexBack.code.desc())
            elif 'finalCalCore' == orderBy:
                orderList.append((MbaCoreIndexBack.final_cal_core * 1).desc())
            elif 'roeAvg' == orderBy:
                orderList.append((MbaFinAnalysisIndexBack.roe_avg * 1).desc())
            elif 'quarterRise' == orderBy:
                orderList.append((MbaRangeRiseCommon.quarter_rise * 1).desc())
            elif 'halfYearRise' == orderBy:
                orderList.append((MbaRangeRiseCommon.half_year_rise * 1).desc())
        else:
            if 'code' == orderBy:
                orderList.append(MbaCoreIndexBack.code)
            elif 'finalCalCore' == orderBy:
                orderList.append((MbaCoreIndexBack.final_cal_core * 1))
            elif 'roeAvg' == orderBy:
                orderList.append((MbaFinAnalysisIndexBack.roe_avg * 1))
            elif 'quarterRise' == orderBy:
                orderList.append((MbaRangeRiseCommon.quarter_rise * 1))
            elif 'halfYearRise' == orderBy:
                orderList.append((MbaRangeRiseCommon.half_year_rise * 1))
    return orderList
