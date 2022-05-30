from lin import NotFound
from flask import Blueprint
# start 模型必须引用后才能在数据库初始化对应表
from app.api.investmentV1.model.coreIndex import MbaCoreIndex
from app.api.investmentV1.model.listingDateCal import MbaListingDateCal
# end 模型必须引用后才能在数据库初始化对应表
from lin import db
from itertools import zip_longest
from sqlalchemy import or_, and_, not_
# from flask import jsonify

coreIndex_api = Blueprint("coreIndex", __name__)


# 根据股票编码：code查询核心指数信息
@coreIndex_api.route('/<id>', methods=['GET'])
def get_coreIndex(id):
    coreIndex = MbaCoreIndex.query.filter_by(code=id).first()
    if coreIndex:
        return coreIndex
    raise NotFound('没有找到对应的股票代码')


# 查询全部的核心指数列表
@coreIndex_api.route("")
def get_coreIndexs():
    return MbaCoreIndex.get(one=False)


# 核心指数分页查询
@coreIndex_api.route('/getcoreIndexsByPage/<int:page>,<int:limit>', methods=["GET"])
def get_coreIndexsByPage(page, limit):
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


# 核心指数分页查询
@coreIndex_api.route('/getcoreIndexsTotal', methods=["GET"])
def get_coreIndexsTotal():
    pageData = (
        db.session.query(MbaCoreIndex.code,
        MbaCoreIndex.code_name,
        MbaCoreIndex.final_cal_core,
        MbaCoreIndex.cal_date,
        MbaListingDateCal.is_new_shares)
        .outerjoin(MbaListingDateCal, MbaCoreIndex.code == MbaListingDateCal.code)
        .filter(and_(MbaCoreIndex.status.__eq__('0'))).count()
    )
    return pageData
    # return MbaCoreIndex.query.count()
