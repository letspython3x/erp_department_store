import simplejson as json
from flask import Response
from flask_restplus import Resource, Api

from api import bp_report
from models.report_model import ReportModel
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_report)


class ReportApi(Resource):
    def get(self):
        status = 200
        rm = ReportModel()
        data = dict(
            products=rm.get_count_of_active_products(),
            orders=rm.get_count_of_current_month_orders(),
            clients=rm.get_count_of_clients(),
            revenue=rm.get_revenue_generated_current_month()
        )

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(ReportApi, "/")
