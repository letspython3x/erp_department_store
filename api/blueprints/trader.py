from flask_restplus import Resource, Api, fields, abort
from flask import request
from api import bp_trader, ValidateTrader
from models.trader_model import TraderModel
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_trader,
          title='Trader API',
          version='v0.1',
          description="Manage Traders",
          doc='/api/documentation')

trader_fields = api.model('traderRequestFields', {
    'trader_id': fields.Integer(),
    'name': fields.String('Name of trader'),
    'address': fields.String('Address of trader'),
    'country': fields.String('Country of trader'),
})

trader_res_model = api.model('traderResponse', {
    'message': fields.String('SUCCESS'),
    'trader': fields.Nested(trader_fields)
})


@api.route('/')
class TraderApi(Resource):
    @api.response(401, "Unauthorized")
    @api.response(500, "Internal Server Error")
    @api.doc(params={'trader_id': 'An ID'})
    @api.marshal_with(trader_res_model, envelope="data")
    def get(self):
        trader_id = request.args.get('trader_id')
        print("Need to fetch data for trader ID: %s" % trader_id)
        tm = TraderModel()
        if trader_id is not None:
            trader = tm.get_record_by_id(int(trader_id))
            if not trader:
                abort(404, "Resource Not Found")
        else:
            print("trader id absent")
            trader = tm.get_all_records()

        data = dict(trader=trader)

        logger.info("PAYLOAD SENT: %s" % data)
        return data

    @api.response(401, "Unauthorized")
    @api.response(500, "Internal Server Error")
    @api.response(201, "Resource successfully added")
    @api.expect(trader_fields)
    def post(self):
        trader = api.payload
        print(trader)
        vf = ValidateTrader(trader)
        vf.validate()
        tm = TraderModel(trader)
        tm.create()

        data = dict(trader_id=tm.trader_id)
        logger.info("PAYLOAD SENT: %s" % data)
        return data


api.add_resource(TraderApi, "/")
