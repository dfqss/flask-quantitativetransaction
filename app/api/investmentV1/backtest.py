from itertools import zip_longest

from flask import Blueprint, request, Flask
from lin import login_required, db
from sqlalchemy import and_

from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.backtest import MbaCoreIndexBack, MbaFinAnalysisIndexBack, \
    MbaRangeRiseRare, MbaRangeRiseCommon

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
        print(split[0])
        print(split[1])
        filterList.append(MbaCoreIndexBack.cal_date.between(split[0], split[1]))
    try:
        # 分页查询
        pageData = db.session.query(MbaCoreIndexBack.code,
                                    MbaCoreIndexBack.code_name,
                                    MbaCoreIndexBack.periods,
                                    MbaCoreIndexBack.final_cal_core,
                                    MbaFinAnalysisIndexBack.roe_avg,
                                    MbaRangeRiseCommon.quarter_rise,
                                    MbaRangeRiseCommon.half_year_rise) \
            .outerjoin(MbaFinAnalysisIndexBack,
                       and_(MbaCoreIndexBack.code == MbaFinAnalysisIndexBack.code,
                            MbaCoreIndexBack.periods == MbaFinAnalysisIndexBack.periods)
                       ) \
            .outerjoin(MbaRangeRiseCommon, and_(MbaCoreIndexBack.code == MbaRangeRiseCommon.code,
                                                MbaCoreIndexBack.periods == MbaRangeRiseCommon.periods)
                       ) \
            .filter(*filterList).order_by(MbaCoreIndexBack.code) \
            .offset(startIndex).limit(pageSize).all()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'periods', 'finalCalCore', 'roeAvg', 'quarterRise',
                   'halfYearRise']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
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
