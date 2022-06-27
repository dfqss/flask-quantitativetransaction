from flask import Blueprint, request, Flask
from lin import login_required

from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.industryClass import MbaIndustryClass
from app.api.investmentV1.model.coreIndex import MbaCoreIndex

app = Flask(__name__)
industryClass_api = Blueprint("industryClass", __name__)

#行业分类
@industryClass_api.route("/getIndustryClassList", methods=["post"])
@login_required
def getIndustryClassList():
    params = request.json
    app.logger.info('start service getStockPoolList------服务入参：' + str(params))
    code = params.get('code')
    codeName = params.get('codeName')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    flag = params.get('flag')
    # 拼接条件
    filterList = []
    # 根据股票代码查询
    if code is not None and len(code.strip()) > 0:
        filterList.append(MbaIndustryClass.code == code)
    # 根据股票名称查询
    if codeName is not None and len(codeName.strip()) > 0:
        filterList.append(MbaIndustryClass.code_name == codeName)
    # 分页查询
    try:
        if flag is not None and len(flag.strip()) > 0 and flag == 'byCode':
            # 分页查询
            filterList.append(MbaCoreIndex.status == 0)
            dataList = MbaIndustryClass.query.filter(*filterList) \
                .outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaIndustryClass.code) \
                .order_by(MbaIndustryClass.code) \
                .offset(startIndex).limit(pageSize).all()
            totalNum = MbaIndustryClass.query.filter(*filterList). \
                outerjoin(MbaCoreIndex, MbaCoreIndex.code == MbaIndustryClass.code).count()
        else:
            dataList = MbaIndustryClass.query.filter(*filterList) \
                .order_by(MbaIndustryClass.code) \
                .offset(startIndex).limit(pageSize).all()
            # 获取分页总条数
            totalNum = MbaIndustryClass.query.filter(*filterList).count()
    except Exception as e:
        app.logger.error('查询行业分类失败:' + str(e))
        return failed(10301)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    return successMap
