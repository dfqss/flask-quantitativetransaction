from datetime import datetime, timedelta

from lin import login_required
from flask import Blueprint, request, Flask
# start 模型必须引用后才能在数据库初始化对应表
from sqlalchemy import func

from app.api.investmentV1.coreIndex import datetimeToString
from app.api.investmentV1.exception.result import success, failed
from app.api.investmentV1.model.coreIndex import MbaCoreIndex
from app.api.investmentV1.model.batchFiles import MbaBatchFiles
from lin import db
from itertools import zip_longest

app = Flask(__name__)
batchFiles_api = Blueprint("batchFiles", __name__)


@batchFiles_api.route("/getBatchFilesList", methods=["post"])
@login_required
def getBatchFilesList():
    params = request.json
    app.logger.info('start service getCoreIndexHistoryList------服务入参：' + str(params))
    fileName = params.get('fileName')
    filePeriods = params.get('filePeriods')
    calDate = params.get('calDate')
    pageSize = params.get('pageSize', 10)
    pageNum = params.get('pageNum', 1)
    startIndex = (pageNum - 1) * pageSize
    # 拼接查询条件
    filterList = []
    # 根据股票代码查询
    if fileName is not None and len(fileName.strip()) > 0:
        filterList.append(MbaBatchFiles.file_name.like('%' + fileName + '%'))
    # 根据股票名称查询
    if filePeriods is not None and len(filePeriods.strip()) > 0:
        filterList.append(MbaBatchFiles.file_periods.startswith(filePeriods))
    # 根据股票名称查询
    if calDate is not None and len(calDate.strip()) > 0:
        filterList.append(func.date_format(calDate, "%Y-%m-%d") ==
                          func.date_format(MbaBatchFiles.cal_date, "%Y-%m-%d"))
    try:
        pageData = db.session.query(MbaBatchFiles.file_name,
                                    MbaBatchFiles.file_path,
                                    MbaBatchFiles.file_periods,
                                    MbaBatchFiles.status,
                                    MbaBatchFiles.description,
                                    MbaBatchFiles.cal_date) \
            .filter(*filterList) \
            .offset(startIndex).limit(pageSize).all()
        # 定义返回参数列表：顺序和字段名称需要和查询的列保持一致
        mapList = ['fileName', 'filePath', 'filePeriods', 'status', 'description', 'calDate']
        dataList = []
        for returnData in pageData:
            dataList.append(dict(zip_longest(mapList, returnData)))
        # 将list中的sql模板对象属性由datetime转为字符串类型
        dataList = datetimeToFormatString(dataList, "calDate", '%Y-%m-%d')
        # 获取分页总条数
        totalNum = MbaBatchFiles.query.count()
    except Exception as e:
        app.logger.error('查询文件失败:' + str(e))
        return failed(10310)
    # 返回参数信息
    successMap = success()
    successMap['dataList'] = dataList
    successMap['totalNum'] = totalNum
    app.logger.info('end service getCoreIndexList------服务出参：' + str(successMap))
    return successMap


# 将list中的sql模板对象属性由datetime转为字符串类型
def datetimeToFormatString(inList, key, dateFormat):
    resultList = []
    for dictDate in inList:
        resultStr = datetime.strftime(dictDate[key], dateFormat)
        dictDate[key] = resultStr
        resultList.append(dictDate)
    return resultList
