import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api, fields

from api import bp_order, ValidateOrder
from models.order_model import OrderModel
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_order,
          title='Order API',
          version='v0.1',
          doc='/api/documentation')

order_model = api.model('Order', {'order_id': fields.Integer()})


# @api.route('/order')
class OrderApi(Resource):
    def get(self):
        order_id = request.args.get('order_id', 0)
        client_id = request.args.get('client_id', 0)
        employee_id = request.args.get('employee_id', 0)
        store_id = request.args.get('store_id', 0)
        order_type = request.args.get('order_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        # print("Need to fetch data for Order ID: %s" % order_id)

        qm = OrderModel()
        order = None if order_id == 0 else qm.search_by_order_id(int(order_id))
        order_by_client = None if client_id == 0 else qm.search_by_client_id(int(client_id))
        order_by_employee = None if employee_id == 0 else qm.search_by_employee_id(int(employee_id))
        order_by_store = None if store_id == 0 else qm.search_by_store_id(int(store_id))
        order_bw_dates = qm.search_between_dates(start_date, end_date)

        data = dict(
            data=order or order_by_client or order_by_employee or order_by_store or order_bw_dates)
        payload = json.dumps(data, use_decimal=True)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=200, mimetype="application/json")

    def post(self):
        # assert isinstance(request, HttpRequest)
        status = 404
        order = request.json
        if not order:
            abort(status)

        print(order)
        order_id = None
        vf = ValidateOrder(order)
        print(vf.validate())
        if vf.validate():
            qm = OrderModel()
            order_id = qm.insert(order)

            if order_id:
                status = 201
                message = "Order created Successfully"
            else:
                message = "No Order Saved, Some internal error"
        else:
            message = "Invalid Order details"

        data = dict(order_id=order_id, message=message)
        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(OrderApi, "/")
