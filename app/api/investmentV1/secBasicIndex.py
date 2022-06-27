from flask import Blueprint, request, Flask
from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.secBasicIndex import MbaSecBasicIndex
from app.util.common import addFieldByConditions
from itertools import zip_longest
from lin import db, login_required
from app.api.investmentV1.model.coreIndex import MbaCoreIndex

app = Flask(__name__)
secBasicIndex_api = Blueprint("secBasicIndex", __name__)


# 查询证券基础指标列表
@secBasicIndex_api.route("/getSecBasicIndexList", methods=["post"])
@login_required
def getSecBasicIndexList():
    params = request.json
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    flag = params.get('flag')
    # 拼接查询条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaSecBasicIndex.code == code)
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaSecBasicIndex.code_name == codeName)
    # 分页查询
    try:
        if flag is not None and len(flag.strip()) > 0 and flag == 'byCode':
            # 分页查询
            filterList.append(MbaCoreIndex.status == 0)
            pageData = db.session.query(MbaSecBasicIndex.code,
                                        MbaSecBasicIndex.code_name,
                                        MbaSecBasicIndex.total_shares,
                                        MbaSecBasicIndex.free_float_shares,
                                        MbaSecBasicIndex.share_issuing_mkt,
                                        MbaSecBasicIndex.rt_mkt_cap,
                                        MbaSecBasicIndex.rt_float_mkt_cap) \
                .filter(*filterList) \
                .outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaSecBasicIndex.code) \
                .order_by(MbaSecBasicIndex.code) \
                .offset(startIndex).limit(pageSize).all()
            totalNum = MbaSecBasicIndex.query.filter(*filterList). \
                outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaSecBasicIndex.code).count()
        else:
            pageData = db.session.query(MbaSecBasicIndex.code,
                                        MbaSecBasicIndex.code_name,
                                        MbaSecBasicIndex.total_shares,
                                        MbaSecBasicIndex.free_float_shares,
                                        MbaSecBasicIndex.share_issuing_mkt,
                                        MbaSecBasicIndex.rt_mkt_cap,
                                        MbaSecBasicIndex.rt_float_mkt_cap)\
                .filter(*filterList) \
                .order_by(MbaSecBasicIndex.code) \
                .offset(startIndex).limit(pageSize).all()
            # 获取分页总条数
            totalNum = MbaSecBasicIndex.query.filter(*filterList).count()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['code', 'code_name', 'total_shares', 'free_float_shares', 'share_issuing_mkt',
                   'rt_mkt_cap', 'rt_float_mkt_cap', 'create_time', 'update_time']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
    except Exception as e:
        app.logger.error('查询证券基础指标失败:' + str(e))
        return failed(10302)
    # 添加资本市场指标
    dataList = addFieldByConditions(dataList)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    return successMap
