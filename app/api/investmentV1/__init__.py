from flask import Blueprint


def create_investmentV1():
    bp_investmentV1 = Blueprint("investmentV1", __name__)
    from app.api.investmentV1.coreIndex import coreIndex_api
    from app.api.investmentV1.finAnalysisIndex import finAnalysisIndex_api
    bp_investmentV1.register_blueprint(coreIndex_api, url_prefix="/coreIndex")
    bp_investmentV1.register_blueprint(finAnalysisIndex_api, url_prefix="/finAnalysisIndex")
    return bp_investmentV1
