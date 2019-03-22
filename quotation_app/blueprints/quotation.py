import json

from flask import request, abort, Response, render_template, url_for
from flask_restplus import Resource, Api

from quotation_app import bp_quotation, ValidateQuotationForm
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_quotation)


class Quotation(Resource):
    def post(self):
        if not request.json:
            abort(404)
        form_data = request.json
        # vf = ValidateQuotationForm(**form_data)
        # vf.validate()
        print(form_data)

        payload = dict(quotation_id=1,
                       products=[
                           {
                               'product_name': 'p1',
                           },
                           {
                               'product_name': 'p2',
                           }
                       ])

        payload = json.dumps(payload)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=200, mimetype="application/json")

    def get(self):
        payload = dict(quotation_id=1,
                       products=[
                           {
                               'product_name': 'p1',
                           },
                           {
                               'product_name': 'p2',
                           }
                       ])

        payload = json.dumps(payload)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=200, mimetype="application/json")

    def put(self):
        return Response("{'status':'OK'}", status=200, mimetype="application/json")

    def delete(self):
        pass


api.add_resource(Quotation, "/")
