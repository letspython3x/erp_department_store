import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api

from api import bp_account, ValidateAccount
from utils.generic_utils import get_logger
from models.account_model import AccountModel

logger = get_logger(__name__)
api = Api(bp_account)


class AccountApi(Resource):
    def get(self):
        status = 200
        account_id = request.args.get('account_id', '')
        name = request.args.get('name', None)
        serial_no = request.args.get('serial_no', None)

        print(account_id)
        pm = AccountModel()
        if account_id not in ['null', '']:
            data = pm.search_by_account_id(int(account_id))
        elif name not in ['null', None, '']:
            data = pm.search_by_name(name)
        elif serial_no not in ['null', None, '']:
            data = pm.search_by_serial_no(serial_no)
        else:
            data = pm.get_recent_accounts(limit=10)

        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def post(self):
        status = 201
        if not request.json:
            abort(status)
        account = request.json

        account_id = None
        vf = ValidateAccount(account)
        if vf.validate():
            # single account
            p = AccountModel()
            account_id = p.insert(account)
            message = "Account added Successfully"
        else:
            message = "Invalid account details"

        data = dict(account_id=account_id,
                    message=message)
        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def delete(self):
        account_id = request.args.get('account_id')
        print(account_id)
        status = 200
        if account_id:
            pm = AccountModel()
            account = pm.delete_account(account_id)
            if account:
                data = dict(message=f"DELETE Account SUCCESS, ID: {account_id}")
            else:
                data = dict(message='Invalid Account ID')
        else:
            data = dict(message="Account ID can't be empty")
            status = 404

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def put(self):
        """
        Will update the details of a account
        :return: response
        """
        if not request.json:
            abort(403)
        status = 400

        account = request.json
        account_id = account.get('account_id')
        if account_id:
            pm = AccountModel()
            is_updated = pm.update_account_item(account_id, account)
            if is_updated:
                status = 200
                data = dict(message=f"UPDATE Account SUCCESS, ID: {account_id}")
            else:
                data = dict(message=f"UPDATE Account FAILURE, ID: {account_id}")
        else:
            data = dict(message='Invalid Account ID')

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def patch(self):
        if not request.json:
            abort(403)
        status = 400
        print(request)
        data = request.json

        account_id = data.get('account_id')
        quantity = data.get('quantity')
        print(quantity)
        if account_id and isinstance(quantity, int):
            pm = AccountModel()
            units_in_stock = pm.update_quantity_in_stocks(account_id, quantity, increase=True)
            status = 200
            data = dict(
                account_id=account_id,
                message="New Stock Quantity: %d" % units_in_stock
            )
        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(AccountApi, "/")
