import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api

from api import bp_transaction, ValidateTransaction
from utils.generic_utils import get_logger
from models.transaction_model import TransactionModel

logger = get_logger(__name__)
api = Api(bp_transaction)


class TransactionApi(Resource):
    def get(self):
        status = 200
        transaction_id = request.args.get('transaction_id', '')
        name = request.args.get('payer_name', None)
        serial_no = request.args.get('serial_no', None)

        print(transaction_id)
        tm = TransactionModel()
        if transaction_id not in ['null', '']:
            data = tm.search_by_transaction_id(int(transaction_id))
        elif name not in ['null', None, '']:
            data = pm.search_by_name(name)
        elif serial_no not in ['null', None, '']:
            data = pm.search_by_serial_no(serial_no)
        else:
            data = pm.get_recent_transactions(limit=10)

        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def post(self):
        status = 201
        if not request.json:
            abort(status)
        transaction = request.json

        transaction_id = None
        vf = ValidateTransaction(transaction)
        if vf.validate():
            # single transaction
            p = TransactionModel()
            transaction_id = p.insert(transaction)
            message = "Transaction added Successfully"
        else:
            message = "Invalid transaction details"

        data = dict(transaction_id=transaction_id,
                    message=message)
        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def delete(self):
        transaction_id = request.args.get('transaction_id')
        print(transaction_id)
        status = 200
        if transaction_id:
            pm = TransactionModel()
            transaction = pm.delete_transaction(transaction_id)
            if transaction:
                data = dict(message=f"DELETE Transaction SUCCESS, ID: {transaction_id}")
            else:
                data = dict(message='Invalid Transaction ID')
        else:
            data = dict(message="Transaction ID can't be empty")
            status = 404

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def put(self):
        """
        Will update the details of a transaction
        :return: response
        """
        if not request.json:
            abort(403)
        status = 400

        transaction = request.json
        transaction_id = transaction.get('transaction_id')
        if transaction_id:
            pm = TransactionModel()
            is_updated = pm.update_transaction_item(transaction_id, transaction)
            if is_updated:
                status = 200
                data = dict(message=f"UPDATE Transaction SUCCESS, ID: {transaction_id}")
            else:
                data = dict(message=f"UPDATE Transaction FAILURE, ID: {transaction_id}")
        else:
            data = dict(message='Invalid Transaction ID')

        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def patch(self):
        if not request.json:
            abort(403)
        status = 400
        print(request)
        data = request.json

        transaction_id = data.get('transaction_id')
        quantity = data.get('quantity')
        print(quantity)
        if transaction_id and isinstance(quantity, int):
            pm = TransactionModel()
            units_in_stock = pm.update_quantity_in_stocks(transaction_id, quantity, increase=True)
            status = 200
            data = dict(
                transaction_id=transaction_id,
                message="New Stock Quantity: %d" % units_in_stock
            )
        payload = json.dumps(data)
        logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(TransactionApi, "/")
