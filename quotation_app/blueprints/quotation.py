# import json
import simplejson as json

from flask import request, abort, Response
from flask_restplus import Resource, Api
from models.models import QuotationModel
from quotation_app import bp_quotation, ValidateQuotation
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_quotation)


class Quotation(Resource):
    def get(self):
        if not request.json:
            abort(404)
        payload = request.json
        status = 404

        quotation_id = payload.get('quotation_id')
        if quotation_id:
            qm = QuotationModel()
            data = qm.search_by_id('quotation_id', int(quotation_id))
            if data:
                status = 200
            else:
                data = dict(message="Quotation does not exist")
        else:
            data = dict(message="Please provide quotation ID")

        payload = json.dumps(data, use_decimal=True)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def put(self):
        if not request.json:
            abort(404)
        quotation = request.json
        status = 404
        # vf = ValidateQuotation(**form_data)
        # if vf.validate():
        if quotation:
            qm = QuotationModel(quotation)
            qm.create()
            status = 200
            data = dict(quotation_id=qm.quotation_id,
                        message="quotation created Successfully")
        else:
            data = dict(message="Please provide quotation details to save")

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def delete(self):
        """
        A quotation will never be deleted, once created
        :return:
        """

    def post(self):
        """
        A quotation will never be updated, once created
        :return:
        """


api.add_resource(Quotation, "/")
