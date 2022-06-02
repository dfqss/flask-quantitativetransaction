from flask import Blueprint


def create_investmentV1():
    bp_investmentV1 = Blueprint("investmentV1", __name__)
    from app.api.investmentV1.coreIndex import coreIndex_api
    from app.api.investmentV1.finAnalysisIndex import finAnalysisIndex_api
    from app.api.investmentV1.secBasicIndex import secBasicIndex_api
    from app.api.investmentV1.stockValue import stockValue_api
    from app.api.investmentV1.tecAnalysisIndex import tecAnalysisIndex_api

    bp_investmentV1.register_blueprint(coreIndex_api, url_prefix="/coreIndex")
    bp_investmentV1.register_blueprint(finAnalysisIndex_api, url_prefix="/finAnalysisIndex")
    bp_investmentV1.register_blueprint(secBasicIndex_api, url_prefix="/secBasicIndex")
    bp_investmentV1.register_blueprint(stockValue_api, url_prefix="/stockValue")
    bp_investmentV1.register_blueprint(tecAnalysisIndex_api, url_prefix="/tecAnalysisIndex")
    return bp_investmentV1
