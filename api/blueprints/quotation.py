import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api, fields

from api import bp_quotation, ValidateQuotation
from models.quotation_model import QuotationModel
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_quotation,
          title='Quotation API',
          version='v0.1',
          doc='/api/documentation')

quotation_model = api.model('Quotation', {'quotation_id': fields.Integer()})


# @api.route('/quotation')
class Quotation(Resource):
    def get(self):
        quotation_id = request.args.get('quotation_id', 0)
        customer_id = request.args.get('customer_id', 0)
        employee_id = request.args.get('employee_id', 0)
        store_id = request.args.get('store_id', 0)
        quotation_type = request.args.get('quotation_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        # print("Need to fetch data for Quotation ID: %s" % quotation_id)

        qm = QuotationModel()
        quotation = None if quotation_id == 0 else qm.search_by_order_id(int(quotation_id))
        quotation_by_customer = None if customer_id == 0 else qm.search_by_customer_id(int(customer_id))
        quotation_by_employee = None if employee_id == 0 else qm.search_by_employee_id(int(employee_id))
        quotation_by_store = None if store_id == 0 else qm.search_by_store_id(int(store_id))

        data = dict(data=quotation or quotation_by_customer or quotation_by_employee)
        payload = json.dumps(data, use_decimal=True)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=200, mimetype="application/json")

    def post(self):
        # assert isinstance(request, HttpRequest)
        status = 404
        quotation = request.json
        if not quotation:
            abort(status)

        print(quotation)
        quotation_id = None
        vf = ValidateQuotation(quotation)
        print(vf.validate())
        if vf.validate():
            qm = QuotationModel()
            quotation_id = qm.insert(quotation)

            if quotation_id:
                status = 201
                message = "Quotation created Successfully"
            else:
                message = "No Quotation Saved, Some internal error"
        else:
            message = "Invalid Quotation details"

        data = dict(quotation_id=quotation_id, message=message)
        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(Quotation, "/")
