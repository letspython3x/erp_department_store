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
    def get(self, quotation_id):
        print("Need to fetch data for Quotation ID: %s" % quotation_id)
        status = 404
        # if not request.json:
        #     abort(status)
        print("Need to fetch data for Quotation ID: %s" % quotation_id)
        quotation = None
        if quotation_id:
            qm = QuotationModel()
            quotation = qm.search_by_id('quotation_id', int(quotation_id))
            if quotation:
                status = 200
                message = "SUCCESS"
            else:
                message = "Quotation does not exist"
        else:
            message = "Please provide numeric quotation ID"

        data = dict(quotation_id=quotation_id,
                    quotation=quotation,
                    message=message)
        payload = json.dumps(data, use_decimal=True)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def delete(self):
        """
        A quotation will never be deleted, once created
        :return:
        """


class SaveQuotation(Resource):
    def post(self):
        status = 404
        if not request.json:
            abort(status)
        quotation = request.json
        print(quotation)
        quotation_id = None
        vf = ValidateQuotation(quotation)

        if vf.validate():
            qm = QuotationModel(quotation)
            if qm.create():
                status = 200
                quotation_id = qm.quotation_id
                message = "Quotation created Successfully"
            else:
                message = "No Quotation Saved, Some internal error"
        else:
            message = "Invalid Quotation details"

        data = dict(quotation_id=quotation_id,
                    message=message)
        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(SaveQuotation, "/")
api.add_resource(Quotation, "/<int:quotation_id>")
