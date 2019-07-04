import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api

from api import bp_product, ValidateProduct
from utils.generic_utils import get_logger
from models.product_model import ProductModel

logger = get_logger(__name__)
api = Api(bp_product)


class Product(Resource):
    def get(self):
        status = 200
        product_id = request.args.get('product_id', '')
        name = request.args.get('name', None)
        serial_no = request.args.get('serial_no', None)

        print(product_id)
        pm = ProductModel()
        if product_id not in ['null', '']:
            data = pm.search_by_product_id(int(product_id))
        elif name not in ['null', None, '']:
            data = pm.search_by_name(name)
        elif serial_no not in ['null', None, '']:
            data = pm.search_by_serial_no(serial_no)
        else:
            data = pm.get_recent_products(limit=10)

        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def post(self):
        status = 201
        if not request.json:
            abort(status)
        product = request.json

        product_id = None
        vf = ValidateProduct(product)
        if vf.validate():
            # single product
            p = ProductModel()
            product_id = p.insert(product)
            message = "Product added Successfully"
        else:
            message = "Invalid product details"

        data = dict(product_id=product_id,
                    message=message)
        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def delete(self):
        product_id = request.args.get('product_id')
        print(product_id)
        status = 200
        if product_id:
            pm = ProductModel()
            product = pm.delete_product(product_id)
            if product:
                data = dict(message=f"DELETE Product SUCCESS, ID: {product_id}")
            else:
                data = dict(message='Invalid Product ID')
        else:
            data = dict(message="Product ID can't be empty")
            status = 404

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def put(self):
        """
        Will update the details of a product
        :return: response
        """
        if not request.json:
            abort(403)
        status = 400

        product = request.json
        product_id = product.get('product_id')
        if product_id:
            pm = ProductModel()
            is_updated = pm.update_product_item(product_id, product)
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

    def patch(self):
        if not request.json:
            abort(403)
        status = 400
        data = request.json

        product_id = data.get('productID')
        quantity = data.get('quantity')
        print(quantity)
        if product_id and isinstance(quantity, int):
            pm = ProductModel()
            unitsInStock = pm.update_quantity_in_stocks(product_id, quantity)
            status = 200
            data = dict(
                product_id=product_id,
                unitsInStock=unitsInStock,
                message="Stock Updated"
            )

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(Product, "/")
