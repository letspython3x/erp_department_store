import json

from flask import request, abort, Response
from flask_restplus import Resource, Api

from quotation_app import bp_customer, ValidateCustomerForm
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_customer)


class Customer(Resource):
    def post(self):
        if not request.json:
            abort(404)
        form_data = request.json
        vf = ValidateCustomerForm(**form_data)
        vf.validate()

        payload = dict()

        payload = json.dumps(payload)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=200, mimetype="application/json")

    def get(self):
        pass


api.add_resource(Customer, "/")
