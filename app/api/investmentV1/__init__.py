from flask import Blueprint


def create_investmentV1():
    bp_investmentV1 = Blueprint("investmentV1", __name__)
    from app.api.investmentV1.coreIndex import coreIndex_api
    from app.api.investmentV1.finAnalysisIndex import finAnalysisIndex_api
    from app.api.investmentV1.secBasicIndex import secBasicIndex_api
    from app.api.investmentV1.stockValue import stockValue_api
    from app.api.investmentV1.tecAnalysisIndex import tecAnalysisIndex_api
    from app.api.investmentV1.dupontAnalysisIndex import dupontAnalysisIndex_api
    from app.api.investmentV1.growthIndex import growthIndex_api
    from app.api.investmentV1.industryClass import industryClass_api
    from app.api.investmentV1.stockPool import StockPool_api
    from app.api.investmentV1.upload import upload_api
    from app.api.investmentV1.importData import importData_api
    from app.api.investmentV1.download import download_file_api

    bp_investmentV1.register_blueprint(coreIndex_api, url_prefix="/coreIndex")
    bp_investmentV1.register_blueprint(finAnalysisIndex_api, url_prefix="/finAnalysisIndex")
    bp_investmentV1.register_blueprint(secBasicIndex_api, url_prefix="/secBasicIndex")
    bp_investmentV1.register_blueprint(stockValue_api, url_prefix="/stockValue")
    bp_investmentV1.register_blueprint(tecAnalysisIndex_api, url_prefix="/tecAnalysisIndex")
    bp_investmentV1.register_blueprint(dupontAnalysisIndex_api, url_prefix="/dupontAnalysisIndex")
    bp_investmentV1.register_blueprint(growthIndex_api, url_prefix="/growthIndex")
    bp_investmentV1.register_blueprint(industryClass_api, url_prefix="/industryClass")
    bp_investmentV1.register_blueprint(StockPool_api, url_prefix="/stockPool")
    bp_investmentV1.register_blueprint(upload_api, url_prefix="/upload")
    bp_investmentV1.register_blueprint(importData_api, url_prefix="/importData")
    bp_investmentV1.register_blueprint(download_file_api, url_prefix="/download")

    return bp_investmentV1
