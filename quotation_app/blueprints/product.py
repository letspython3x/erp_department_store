import simplejson as json

from flask import request, abort, Response
from flask_cors import CORS, cross_origin
from flask_restplus import Resource, Api
from . import ProductModel
from quotation_app import bp_product, ValidateProduct
from utils.generic_utils import get_logger

logger = get_logger(__name__)
CORS(bp_product, support_credentials=True, resources={r"/foo": {"origins": "http://localhost:4200"}})
api = Api(bp_product)


class BulkProduct(Resource):
    def get(self):
        pm = ProductModel()
        data = pm.fetch_all_products()
        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=200, mimetype="application/json")

    @cross_origin(origin='localhost')
    def put(self):
        status = 404
        if not request.json:
            abort(status)
        product = request.json

        print("Received req: %s" % product)
        print("Received req: %s" % request)
        try:
            vf = ValidateProduct(product)
            if vf.validate():
                # single product
                p = ProductModel(product)
                product_id = p.create()
                data = {
                    "name": p.product_name,
                    "product_id": product_id
                }
                status = 200
        except AssertionError as ae:
            data = dict(message="Please check the product details")
            print(ae)
        except Exception as e:
            data = dict(message="Unable to Add product")
            logger.error(e)

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


class Product(Resource):
    def get(self, product_name):
        status = 404
        pm = ProductModel()
        # data = pm.search_by_name(product_name)
        data = pm.search_by_id('product_id', int(product_name)) or pm.search_by_name(product_name)
        # print(data)
        if data:
            status = 200
        else:
            data = dict(message="Invalid Product name or ID")

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    @cross_origin(origin='localhost', supports_credentials=True)
    def delete(self, product_name):
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

    @cross_origin(origin='localhost', supports_credentials=True)
    def post(self, product_name):
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


api.add_resource(BulkProduct, "/")
api.add_resource(Product, "/<string:product_name>")
