import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api

from api import bp_customer, ValidateUser
from models.customer_model import CustomerModel
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_customer)


class Customer(Resource):
    def get(self):
        status = 200
        customer_id = request.args.get('customer_id', '')
        phone = request.args.get('phone', '')
        email = request.args.get('email', '')

        cm = CustomerModel()
        if customer_id not in [0, 'null']:
            data = cm.search_by_customer_id(customer_id)
        elif phone not in [0, 'null']:
            data = cm.search_by_phone(phone)
        elif email not in [0, 'null']:
            data = cm.search_by_email(email)
        else:
            data = cm.get_recent_customers(limit=10)

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def post(self):
        status = 201
        if not request.json:
            abort(status)
        customer = request.json

        customer_id = None
        vf = ValidateUser(customer)
        if vf.validate():
            cm = CustomerModel()
            customer_id = cm.insert(customer)
            message = "Customer added Successfully"
        else:
            message = "Invalid Customer details"

        data = dict(customer_id=customer_id,
                    message=message)

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def delete(self):
        customer_id = request.args.get('customer_id')
        status = 200
        if customer_id:
            cm = CustomerModel()
            customer = cm.delete_customer(customer_id)
            if customer:
                data = dict(message=f"DELETE Customer SUCCESS, ID: {customer_id}")
            else:
                data = dict(message=f"DELETE Customer FAILURE, ID: {customer_id}")
        else:
            data = dict(message="Customer ID can't be empty")
            status = 404

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def put(self):
        """
        Will update the details of a product
        :return: response
        """
        status = 400
        if not request.json:
            abort(403)

        customer = request.json
        customer_id = customer.get('customer_id')

        if customer_id:
            pm = CustomerModel()
            is_updated = pm.update_product_item(customer_id, customer)
            if is_updated:
                status = 200
                data = dict(message=f"UPDATE Customer SUCCESS, ID: {customer_id}")
            else:
                data = dict(message=f"UPDATE Customer FAILURE, ID: {customer_id}")
        else:
            data = dict(message='Invalid Customer ID')

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(Customer, "/")
