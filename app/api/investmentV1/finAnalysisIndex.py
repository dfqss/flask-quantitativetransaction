from itertools import zip_longest

from flask import Blueprint, request, Flask
from lin import login_required

from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.finAnalysisIndex import MbaFinAnalysisIndex
from app.api.investmentV1.model.coreIndex import MbaCoreIndex
from app.api.investmentV1.model.industryClass import MbaIndustryClass
from lin import db

app = Flask(__name__)
finAnalysisIndex_api = Blueprint("finAnalysisIndex", __name__)


# 查询财务分析指标（盈利指标和每股指标）列表
@finAnalysisIndex_api.route("/getFinAnalysisIndexList", methods=["post"])
@login_required
def getFinAnalysisIndexList():
    params = request.json
    app.logger.info('start service getFinAnalysisIndexList------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    industry_sw = params.get('industry_sw')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    flag = params.get('flag')
    # 拼接查询条件
    filterList = []
    order_byList = []
    order_byList.append(MbaFinAnalysisIndex.code)
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaFinAnalysisIndex.code.startswith(code))
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaFinAnalysisIndex.code_name.startswith(codeName))
    # 根据行业分类查询
    if industry_sw is not None and len(industry_sw.strip()) > 0:
        filterList.append(MbaIndustryClass.industry_sw.startswith(industry_sw))
        order_byList.clear()
        order_byList.append(MbaFinAnalysisIndex.roe_basic * 1)
    try:
        if flag is not None and len(flag.strip()) > 0 and flag == 'byCode':
            # 分页查询
            filterList.append(MbaCoreIndex.status == 0)
            pageData = db.session.query(MbaFinAnalysisIndex.code,
                                        MbaFinAnalysisIndex.code_name,
                                        MbaFinAnalysisIndex.roe_avg,
                                        MbaFinAnalysisIndex.roe_basic,
                                        MbaFinAnalysisIndex.roa,
                                        MbaFinAnalysisIndex.gross_profit_margin,
                                        MbaFinAnalysisIndex.net_profit_margin,
                                        MbaFinAnalysisIndex.tot_ope_rev,
                                        MbaFinAnalysisIndex.ope_rev,
                                        MbaFinAnalysisIndex.goodwill,
                                        MbaFinAnalysisIndex.r_and_d_costs,
                                        MbaFinAnalysisIndex.segment_sales,
                                        MbaFinAnalysisIndex.debt_to_assets,
                                        MbaFinAnalysisIndex.cash_to_current_debt,
                                        MbaFinAnalysisIndex.pe,
                                        MbaFinAnalysisIndex.pb,
                                        MbaFinAnalysisIndex.gr_ps,
                                        MbaFinAnalysisIndex.or_ps,
                                        MbaFinAnalysisIndex.cf_ps,
                                        MbaFinAnalysisIndex.eps_basic,
                                        MbaFinAnalysisIndex.bps,
                                        MbaIndustryClass.industry_sw) \
                .outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaFinAnalysisIndex.code) \
                .outerjoin(MbaIndustryClass, MbaFinAnalysisIndex.code == MbaIndustryClass.code)\
                .filter(*filterList) \
                .order_by(*order_byList) \
                .offset(startIndex).limit(pageSize).all()
            if industry_sw is not None and len(industry_sw.strip()) > 0:
                totalNum = MbaFinAnalysisIndex.query.filter(*filterList)\
                    .outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaFinAnalysisIndex.code)\
                    .outerjoin(MbaIndustryClass, MbaIndustryClass.code == MbaFinAnalysisIndex.code)\
                    .count()
            else:
                totalNum = MbaFinAnalysisIndex.query.filter(*filterList). \
                    outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaFinAnalysisIndex.code).count()
        else:
            # 分页查询
            pageData = db.session.query(MbaFinAnalysisIndex.code,
                                        MbaFinAnalysisIndex.code_name,
                                        MbaFinAnalysisIndex.roe_avg,
                                        MbaFinAnalysisIndex.roe_basic,
                                        MbaFinAnalysisIndex.roa,
                                        MbaFinAnalysisIndex.gross_profit_margin,
                                        MbaFinAnalysisIndex.net_profit_margin,
                                        MbaFinAnalysisIndex.tot_ope_rev,
                                        MbaFinAnalysisIndex.ope_rev,
                                        MbaFinAnalysisIndex.goodwill,
                                        MbaFinAnalysisIndex.r_and_d_costs,
                                        MbaFinAnalysisIndex.segment_sales,
                                        MbaFinAnalysisIndex.debt_to_assets,
                                        MbaFinAnalysisIndex.cash_to_current_debt,
                                        MbaFinAnalysisIndex.pe,
                                        MbaFinAnalysisIndex.pb,
                                        MbaFinAnalysisIndex.gr_ps,
                                        MbaFinAnalysisIndex.or_ps,
                                        MbaFinAnalysisIndex.cf_ps,
                                        MbaFinAnalysisIndex.eps_basic,
                                        MbaFinAnalysisIndex.bps,
                                        MbaIndustryClass.industry_sw) \
                .outerjoin(MbaIndustryClass, MbaFinAnalysisIndex.code == MbaIndustryClass.code) \
                .filter(*filterList) \
                .order_by(*order_byList) \
                .offset(startIndex).limit(pageSize).all()
            if industry_sw is not None and len(industry_sw.strip()) > 0:
                totalNum = MbaFinAnalysisIndex.query \
                    .outerjoin(MbaIndustryClass, MbaFinAnalysisIndex.code == MbaIndustryClass.code) \
                    .filter(*filterList)\
                    .count()
            else:
                totalNum = MbaFinAnalysisIndex.query.filter(*filterList).count()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'code_name', 'roe_avg', 'roe_basic', 'roa',
                   'gross_profit_margin', 'net_profit_margin', 'tot_ope_rev', 'ope_rev', 'goodwill',
                   'r_and_d_costs', 'segment_sales', 'debt_to_assets', 'cash_to_current_debt', 'pe',
                   'pb', 'gr_ps', 'or_ps', 'cf_ps', 'eps_basic', 'bps', 'industry_sw']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
    except Exception as e:
        app.logger.error('查询财务分析指标信息失败:' + str(e))
        return failed(10206)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getFinAnalysisIndexList------服务出参：' + str(successMap))
    return successMap
