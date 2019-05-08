import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api
from models.models import CustomerModel
from quotation_app import bp_customer, ValidateUser
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_customer)


#
# class BulkCustomer(Resource):
#     # def get(self):
#     #     cm = CustomerModel()
#     #     data = cm.fetch_all()
#     #     payload = json.dumps(data)
#     #     logger.info("PAYLOAD SENT: %s" % payload)
#     #     return Response(payload, status=200, mimetype="application/json")
#
#     def post(self):
#         status = 400
#         if not request.json:
#             abort(status)
#         customer_form = request.json
#
#         vf = ValidateUser(customer_form)
#         customer_id = None
#         if vf.validate():
#             cm = CustomerModel(customer_form)
#             customer_id = cm.create()
#             status = 200
#             message = "Customer created Successfully"
#         else:
#             message = "Invalid Customer details"
#
#         data = dict(customer_id=customer_id,
#                     message=message)
#
#         payload = json.dumps(data)
#         logger.info("PAYLOAD SENT: %s" % payload)
#
#         return Response(payload, status=status, mimetype="application/json")


class Customer(Resource):
    def get(self):
        status = 200
        customer_id = request.args.get('customer_id', 0)
        phone = request.args.get('phone', None)
        email = request.args.get('email', None)

        cm = CustomerModel()
        if customer_id != 0:
            data = cm.search_by_id('customer_id', int(customer_id))
        elif phone is not None:
            data = cm.search_by_phone(phone)[0]
        elif email is not None:
            data = cm.search_by_email(email)[0]
        else:
            data = cm.fetch_all()

        if data is None:
            data = {
                "message": "No records found",
            }

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def post(self):
        status = 400
        if not request.json:
            abort(status)
        customer_form = request.json

        vf = ValidateUser(customer_form)
        customer_id = None
        if vf.validate():
            cm = CustomerModel(customer_form)
            customer_id = cm.create()
            status = 200
            message = "Customer created Successfully"
        else:
            message = "Invalid Customer details"

        data = dict(customer_id=customer_id,
                    message=message)

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)

        return Response(payload, status=status, mimetype="application/json")

    def delete(self, param):
        if not request.json:
            abort(404)
        # product_id = request.json.get('customer_id')
        status = 200
        if param:
            cm = CustomerModel()
            customer = cm.search_by_id(pk_key='customer_id', pk_val=int(param))
            if customer:
                if cm.deactivate(customer):
                    data = dict(message=f"DELETE Product SUCCESS, ID: {param}")
                else:
                    data = dict(message=f"DELETE Product FAILURE, ID: {param}")
                    status = 404
            else:
                data = dict(message='Invalid Customer ID')
        else:
            data = dict(message="Product ID can't be empty")
            status = 404

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def put(self, param):
        """
        Will update the details of a product
        :return: response
        """
        status = 400
        if not request.json:
            abort(status)
        customer = request.json

        if param:
            cm = CustomerModel()
            is_updated = cm.update_details(param, customer)
            if is_updated:
                status = 200
                data = dict(message=f"UPDATE Customer SUCCESS, ID: {param}")
            else:
                data = dict(message=f"UPDATE Customer FAILURE, ID: {param}")
        else:
            data = dict(message='Invalid Customer ID')

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


# api.add_resource(Customer, "/?customer_id=<int:customer_id>&phone=<string:phone>&email=<string:email>")
# api.add_resource(Customer, "?<int:customer_id>&<string:phone>&<string:email>")
api.add_resource(Customer, "/")
# api.add_resource(BulkCustomer, "/")
# api.add_resource(Customer, "/<string:param>")
