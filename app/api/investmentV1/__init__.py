from flask import Blueprint

from app.api.investmentV1.coreIndex import coreIndex_api


def create_investmentV1():
    bp_v1 = Blueprint("investmentV1", __name__)
    bp_v1.register_blueprint(coreIndex_api, url_prefix="/coreIndex")
    return bp_v1
