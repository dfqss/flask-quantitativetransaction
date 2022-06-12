from flask import Blueprint, request, Flask

from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.stockPool import MbaStockPool
from app.api.investmentV1.model.industryClass import MbaIndustryClass
from lin import db
from itertools import zip_longest

app = Flask(__name__)
StockPool_api = Blueprint("stockPool", __name__)


# 查询股票池
@StockPool_api.route("/getStockPoolList", methods=["post"])
# @login_required
def getStockPoolList():
    params = request.json
    app.logger.info('start service getStockPoolList------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    # 拼接条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaStockPool.code.startswith(code))
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaStockPool.code_name.startswith(codeName))
    try:
        # 分页查询
        pageData = db.session.query(MbaStockPool.code,
                                    MbaStockPool.code_name,
                                    MbaStockPool.periods,
                                    MbaStockPool.create_time,
                                    MbaIndustryClass.industry_sw,
                                    MbaIndustryClass.industry_cit) \
            .outerjoin(MbaIndustryClass, MbaStockPool.code == MbaIndustryClass.code) \
            .filter(*filterList).order_by(MbaStockPool.code) \
            .offset(startIndex).limit(pageSize).all()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'periods', 'create_time', 'industry_sw', 'industry_cit']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
        # 获取分页总条数
        totalNum = MbaStockPool.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询股票池信息失败:' + str(e))
        return failed(10203)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getStockPoolList------服务出参：' + str(successMap))
    return successMap


# 查询股票池
@StockPool_api.route("/batchInsertStockPool", methods=["post"])
# @login_required
def batchInsertStockPool():
    params = request.json
    app.logger.info('start service batchInsertStockPool------服务入参：' + str(params))
    insertData = params.get('insertData')
    try:
        if len(insertData) != 0:
            sql = "insert into mba_stock_pool " \
                  "(is_deleted, code, code_name, periods, in_pool_status, " \
                  "create_time, update_time) values " \
                  "('0', :code, :codeName, :periods, 'in', now(), now()) "
            db.session.execute(sql, insertData)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error('添加股票池失败:' + str(e))
        return failed(10201)
    finally:
        db.session.close()
    app.logger.info('end service batchInsertStockPool------服务出参：' + str(params))
    return success(16)
