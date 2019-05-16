import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api

from api import bp_product, ValidateProduct
from utils.generic_utils import get_logger
from models.product_model import ProductModel

logger = get_logger(__name__)
api = Api(bp_product)


# class BulkProduct(Resource):
#     def get(self):
#         pm = ProductModel()
#         data = pm.fetch_all()
#         payload = json.dumps(data)
#         logger.info("PAYLOAD SENT: %s" % payload)
#         return Response(payload, status=200, mimetype="application/json")
#
#     def post(self):
#         status = 404
#         if not request.json:
#             abort(status)
#         product = request.json
#         try:
#             vf = ValidateProduct(product)
#             if vf.validate():
#                 # single product
#                 p = ProductModel(product)
#                 product_id = p.create()
#                 data = {
#                     "name": p.product_name,
#                     "product_id": product_id
#                 }
#                 status = 200
#         except AssertionError as ae:
#             data = dict(message="Please check the product details")
#             print(ae)
#         except Exception as e:
#             data = dict(message="Unable to Add product")
#             logger.error(e)
#
#         payload = json.dumps(data)
#         logger.info("PAYLOAD SENT: %s" % payload)
#         return Response(payload, status=status, mimetype="application/json")
#

class Product(Resource):
    def get(self):
        status = 200
        product_id = request.args.get('product_id', 0)
        name = request.args.get('name', None)
        serial_no = request.args.get('serial_no', None)

        pm = ProductModel()
        if product_id != 0:
            data = pm.search_by_id('product_id', int(product_id))
        elif name is not None:
            data = pm.search_by_name(name)
        elif serial_no is not None:
            data = pm.search_by_serial_no(serial_no)
        else:
            data = pm.fetch_all()

        # print(data)
        if data is None:
            data = {
                "message": "No records found",
            }

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def post(self):
        status = 404
        if not request.json:
            abort(status)
        product = request.json
        product_id = None
        vf = ValidateProduct(product)
        if vf.validate():
            # single product
            p = ProductModel(product)
            product_id = p.create()
            message = "Product added Successfully"
            status = 200
        else:
            message = "Please check the product details"

        data = dict(product_id=product_id,
                    message=message)
        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def delete(self):
        if not request.json:
            abort(404)
        product_id = request.json.get('product_id')
        status = 200
        if product_id:
            pm = ProductModel()
            product = pm.search_by_id(pk_key='product_id', pk_val=int(product_id))
            if product:
                if pm.deactivate(product):
                    data = dict(message=f"DELETE Product SUCCESS, ID: {product_id}")
                else:
                    data = dict(message=f"DELETE Product FAILURE, ID: {product_id}")
                    status = 404
            else:
                data = dict(message='Invalid Product ID')
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
        if not request.json:
            abort(403)
        status = 400
        data = request.json

        product_id = data.get('product_id')
        # product_name = request.json.get("product_name")

        if product_id:
            pm = ProductModel()
            is_updated = pm.update_details(product_id, data)
            if is_updated:
                status = 200
                data = dict(message=f"UPDATE Product SUCCESS, ID: {product_id}")
            else:
                data = dict(message=f"UPDATE Product FAILURE, ID: {product_id}")
        else:
            data = dict(message='Invalid Product ID')

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


# api.add_resource(BulkProduct, "/")
api.add_resource(Product, "/")
