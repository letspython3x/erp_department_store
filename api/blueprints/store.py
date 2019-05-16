from flask_restplus import Resource, Api, fields, abort
from flask import request
from api import bp_store, ValidateStore
from models.store_model import StoreModel
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_store,
          title='Store API',
          version='v0.1',
          description="Manage Stores",
          doc='/api/documentation')

store_fields = api.model('storeRequestFields', {
    'store_id': fields.Integer(),
    'name': fields.String('Name of Store'),
    'address': fields.String('Address of Store'),
    'country': fields.String('Country of Store'),
})

store_res_model = api.model('storeResponse', {
    'message': fields.String('SUCCESS'),
    'store': fields.Nested(store_fields)
})


#@api.route('/<store_id>')
@api.route('/')
class Store(Resource):
    @api.response(401, "Unauthorized")
    @api.response(500, "Internal Server Error")
    @api.doc(params={'store_id': 'An ID'})
    @api.marshal_with(store_res_model, envelope="data")
    def get(self, store_id=None):
        store_id = request.args.get('store_id')
        print("Need to fetch data for Store ID: %s" % store_id)
        sm = StoreModel()
        if store_id is not None:
            store = sm.get_record_by_id(int(store_id))
            if not store:
                abort(404, "Resource Not Found")
        else:
            print("Store id absent")
            store = sm.get_all_records()

        print(store)
        data = dict(store=store)
        logger.info("PAYLOAD SENT: %s" % data)
        return data

    @api.response(401, "Unauthorized")
    @api.response(500, "Internal Server Error")
    @api.response(201, "Resource successfully added")
    @api.expect(store_fields)
    def post(self):
        store = api.payload
        print(store)
        vf = ValidateStore(store)
        vf.validate()
        sm = StoreModel(store)
        sm.create()
        data = dict(store_id=sm.store_id)
        logger.info("PAYLOAD SENT: %s" % data)
        return data
