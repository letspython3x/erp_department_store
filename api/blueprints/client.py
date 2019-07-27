import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api

from api import bp_client, ValidateUser
from models.client_model import ClientModel
from utils.generic_utils import get_logger

logger = get_logger(__name__)
api = Api(bp_client)


class ClientApi(Resource):
    def get(self):
        status = 200
        client_id = request.args.get('client_id', '')
        phone = request.args.get('phone', '')
        email = request.args.get('email', '')

        cm = ClientModel()
        print(client_id)
        if client_id not in [None, 0, 'null', '']:
            data = cm.search_by_client_id(client_id)
        elif phone not in [None, 0, 'null', '']:
            data = cm.search_by_phone(phone)
        elif email not in [None, 0, 'null', '']:
            data = cm.search_by_email(email)
        else:
            data = cm.get_recent_clients(limit=10)

        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def post(self):
        status = 201
        if not request.json:
            abort(status)
        client = request.json

        client_id = None
        vf = ValidateUser(client)
        if vf.validate():
            cm = ClientModel()
            client_id = cm.insert(client)
            message = "Client added Successfully"
        else:
            message = "Invalid Client details"

        data = dict(client_id=client_id,
                    message=message)

        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def delete(self):
        client_id = request.args.get('client_id')
        status = 200
        if client_id:
            cm = ClientModel()
            client = cm.delete_client(client_id)
            if client:
                data = dict(message=f"DELETE Client SUCCESS, ID: {client_id}")
            else:
                data = dict(message=f"DELETE Client FAILURE, ID: {client_id}")
        else:
            data = dict(message="Client ID can't be empty")
            status = 404

        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def put(self):
        """
        Will update the details of a product
        :return: response
        """
        status = 400
        if not request.json:
            abort(403)

        client = request.json
        client_id = client.get('client_id')

        if client_id:
            pm = ClientModel()
            is_updated = pm.update_client(client_id, client)
            if is_updated:
                status = 200
                data = dict(message=f"UPDATE Client SUCCESS, ID: {client_id}")
            else:
                data = dict(message=f"UPDATE Client FAILURE, ID: {client_id}")
        else:
            data = dict(message='Invalid Client ID')

        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def patch(self):
        logger.info("Update client accounts")
        status = 400
        if not request.json:
            abort(403)

        client = request.json
        client_id = client.get('client_id')
        amount = client.get('amount')

        payload = json.dumps('Client account Update in progress')
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")




api.add_resource(ClientApi, "/")
