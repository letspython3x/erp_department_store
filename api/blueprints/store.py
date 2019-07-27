import simplejson as json
from flask import request, Response
from flask_restplus import Resource, Api, abort

from api import bp_store, ValidateStore
from models.store_model import StoreModel
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_store,
          title='Store API',
          version='v0.1',
          description="Manage Stores",
          doc='/api/documentation')


#
# store_fields = api.model('storeRequestFields', {
#     'store_id': fields.Integer(),
#     'name': fields.String('Name of Store'),
#     'category': fields.String('Store Category'),
#     'address': fields.String('Address of Store'),
#     'country': fields.String('Country of Store'),
# })
#
# store_res_model = api.model('storeResponse', {
#     'message': fields.String('SUCCESS'),
#     'store': fields.Nested(store_fields)
# })
#
#
# @api.route('/')
class StoreApi(Resource):
    # @api.response(401, "Unauthorized")
    # @api.response(500, "Internal Server Error")
    # @api.doc(params={'store_id': 'An ID'})
    # @api.marshal_with(store_res_model, envelope="data")
    def get(self):
        store_id = request.args.get('store_id', '')
        print("Need to fetch data for Store ID: %s" % store_id)
        sm = StoreModel()
        if store_id not in ['null', '', None]:
            data = sm.search_by_store_id(store_id)
            if not data:
                abort(404, "Resource Not Found")
        else:
            logger.info("Fetching all stores")
            data = sm.get_all_stores()

        # data = dict(store=store)
        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return data

    # @api.response(401, "Unauthorized")
    # @api.response(500, "Internal Server Error")
    # @api.response(201, "Resource successfully added")
    # @api.expect(store_fields)
    def post(self):
        status = 201
        if not request.json:
            abort(status)
        store = request.json

        store_id = None
        vf = ValidateStore(store)
        if vf.validate():
            # single product
            sm = StoreModel()
            store_id = sm.insert(store)
            message = "Store added Successfully"
        else:
            message = "Invalid Store details"

        data = dict(store_id=store_id,
                    message=message)

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(StoreApi, "/")
