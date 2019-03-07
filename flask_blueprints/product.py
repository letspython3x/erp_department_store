import json

from flask import request, abort, Blueprint, Response
from flask_restplus import Resource, Api

from apps.validate_forms import ValidateProductForm
from utils.generic_utils import get_logger

logger = get_logger(__name__)
bp_product = Blueprint("product_view", __name__)
api = Api(bp_product)


class Product(Resource):
    def post(self):
        if not request.json:
            abort(404)
        form_data = request.json
        vf = ValidateProductForm(form_data)
        vf.validate()

        payload = dict()

        payload = json.dumps(payload)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def get(self):
        pass


api.add_resource(Product, "/")
