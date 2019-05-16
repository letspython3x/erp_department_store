# import json
import simplejson as json

from flask import request, abort, Response
from flask_restplus import Resource, Api, fields
from models.quotation_model import QuotationModel
from api import bp_quotation, ValidateQuotation
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_quotation,
          title='Quotation API',
          version='v0.1',
          doc='/api/documentation')

quotation_model = api.model('Quotation', {'quotation_id': fields.Integer()})


@api.route('/quotation')
class Quotation(Resource):
    def get(self):
        status = 404
        quotation_id = request.args.get('quotation_id', None)
        print("Need to fetch data for Quotation ID: %s" % quotation_id)

        if quotation_id is not None:
            qm = QuotationModel()
            quotation = qm.search_by_id('quotation_id', int(quotation_id))
            if quotation:
                status = 200
                message = "Quotation Found"
            else:
                message = "Invalid Quotation, Please provide correct quotation ID"
        else:
            message = "Please provide quotation ID"
            quotation = None

        data = dict(quotation_id=quotation_id,
                    quotation=quotation,
                    message=message)
        payload = json.dumps(data, use_decimal=True)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

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
                status = 201
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

    def delete(self):
        """
        A quotation will never be deleted, once created
        :return:
        """

# api.add_resource(Quotation, "/")
