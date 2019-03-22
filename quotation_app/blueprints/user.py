import json

from flask import request, abort, Response
from flask_restplus import Resource, Api

from quotation_app import bp_user, ValidateUserForm
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_user)


class User(Resource):
    def post(self):
        if not request.json:
            abort(404)
        form_data = request.json
        vf = ValidateUserForm(**form_data)
        vf.validate()

        payload = dict()

        payload = json.dumps(payload)
        logger.info("PAYLOAD SENT: %s" % payload)
        status = 200
        return Response(payload, status=status, mimetype="application/json")

    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


api.add_resource(User, "/")
