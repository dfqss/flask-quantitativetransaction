from flask import Blueprint, request, Flask

from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.stockPool import MbaStockPool
from app.api.investmentV1.model.industryClass import MbaIndustryClass
from app.util.common import addFieldByConditions
from lin import db, login_required, permission_meta, group_required
from itertools import zip_longest

app = Flask(__name__)
StockPool_api = Blueprint("stockPool", __name__)


# 查询股票池
@StockPool_api.route("/getStockPoolList", methods=["post"])
@login_required
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
                                    MbaStockPool.remark,
                                    MbaIndustryClass.industry_sw,
                                    MbaIndustryClass.industry_cit) \
            .outerjoin(MbaIndustryClass, MbaStockPool.code == MbaIndustryClass.code) \
            .filter(*filterList).order_by(MbaStockPool.code) \
            .offset(startIndex).limit(pageSize).all()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'codeName', 'periods', 'create_time', 'remark', 'industry_sw', 'industry_cit']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
        # 获取分页总条数
        totalNum = MbaStockPool.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询股票池信息失败:' + str(e))
        return failed(10203)
    # 添加资本市场指标
    dataList = addFieldByConditions(dataList)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getStockPoolList------服务出参：' + str(successMap))
    return successMap

# 新增股票池股票
@StockPool_api.route("/insertStockPool", methods=["post"])
@permission_meta(name="新增股票池股票", module="股票池", mount=True)
@group_required
@login_required
def insertStockPool():
    params = request.json
    app.logger.info('start service insertStockPool------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    remark = params.get('remark')
    try:
        value = [{"code": code, "codeName": codeName, "remark": remark}]
        sql = "insert into mba_stock_pool(is_deleted,code,code_name,remark,create_time,update_time)" \
              "values(0,:code,:codeName,:remark,now(),now())"
        db.session.execute(sql, value)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error('新增股票池股票失败:' + str(e))
        return failed(10309)
    finally:
        db.session.close()
    app.logger.info('end service insertStockPool------服务出参：' + str(params))
    return success(102)


# 批量插入股票池
@StockPool_api.route("/batchInsertStockPool", methods=["post"])
@permission_meta(name="加入股票池", module="投资标初选", mount=True)
# 只有在分组授权后才可访问
@group_required
@login_required
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


# 修改股票池股票备注
@StockPool_api.route("/updateStockPoolByCode", methods=["post"])
@permission_meta(name="修改股票池备注", module="股票池", mount=True)
@group_required
@login_required
def updateStockPoolByCode():
    params = request.json
    app.logger.info('start service updateStockPoolByCode------服务入参：' + str(params))
    code = params.get('code')
    remark = params.get('remark')
    try:
        value = [{"code": code, "remark": remark}]
        sql = "update mba_stock_pool set remark = :remark " \
              "where code = :code"
        db.session.execute(sql, value)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error('修改股票池股票备注失败:' + str(e))
        return failed(10305)
    finally:
        db.session.close()
    app.logger.info('end service updateStockPoolByCode------服务出参：' + str(params))
    return success(100)


# 批量删除股票池
@StockPool_api.route("/batchDeleteStockPool", methods=["post"])
@permission_meta(name="移出股票池", module="股票池", mount=True)
@group_required
@login_required
def batchDeleteStockPool():
    params = request.json
    app.logger.info('start service batchDeleteStockPool------服务入参：' + str(params))
    deleteData = params.get('deleteData')
    try:
        if len(deleteData) > 0:
            sql = "delete from mba_stock_pool where code = :code"
            db.session.execute(sql, deleteData)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error('批量删除股票池:' + str(e))
        return failed(10306)
    finally:
        db.session.close()
    app.logger.info('end service batchDeleteStockPool------服务出参：' + str(params))
    return success(101)
