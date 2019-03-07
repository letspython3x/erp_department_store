import json

from flask import request, abort, Blueprint, Response
from flask_restplus import Resource, Api

from apps.validate_forms import ValidateQuotationForm
from utils.generic_utils import get_logger

logger = get_logger(__name__)
bp_quotation = Blueprint("quotation_view", __name__)
api = Api(bp_quotation)


class Quotation(Resource):
    def post(self):
        if not request.json:
            abort(404)
        form_data = request.json
        vf = ValidateQuotationForm(form_data)
        vf.validate()

        payload = dict()

        payload = json.dumps(payload)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def get(self):
        pass


api.add_resource(Quotation, "/")
