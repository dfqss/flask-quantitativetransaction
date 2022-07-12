from lin import login_required
from flask import Blueprint, Flask
from app.api.investmentV1.scheduler.tasking.batchFiles import readFile
from app.api.investmentV1.scheduler.tasking.coreIndex import createOrUpdateCoreIndex
from app.api.investmentV1.scheduler.tasking.listingIndex import createOrUpdateListingDateCal
from app.api.investmentV1.scheduler.tasking.otherIndex import createOrUpdateOtherIndex

app = Flask(__name__)
importData_api = Blueprint("importData", __name__)


# 批量文件入库
@importData_api.route("/readCoreIndexExcel", methods=["post"])
@login_required
def readCoreIndexExcel():
    app.logger.info('start service readCoreIndexExcel from api')
    return readFile()


# 读取核心指标数据
@importData_api.route("/importCoreIndexData", methods=["post"])
@login_required
def importCoreIndexData():
    app.logger.info('start service importCoreIndexData from api')
    return createOrUpdateCoreIndex()


# 读取其他指标数据
@importData_api.route("/importOtherIndexData", methods=["post"])
@login_required
def importOtherIndexData():
    app.logger.info('start service importOtherIndexData from api')
    return createOrUpdateOtherIndex()


# 读取上市日期数据
@importData_api.route("/importListingData", methods=["post"])
@login_required
def importListingData():
    app.logger.info('start service importListingData from api')
    return createOrUpdateListingDateCal()
