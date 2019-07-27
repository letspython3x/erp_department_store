from datetime import datetime

from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
from models.retail_model import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class TransactionModel(RetailModel):
    def __init__(self):
        super(TransactionModel, self).__init__()
        self.table = 'TRANSACTIONS'

    def generate_new_txn_id(self):
        """
        get the number of pk that starts with "transactions"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        return _id

    def insert(self, transaction):
        txn_id = self.generate_new_txn_id()
        payee = transaction.get('payee')
        payer = transaction.get('payer')
        txn_amount = transaction.get('txn_amount')

        item = {
            "pk": f"transactions#{txn_id}",
            "sk": f"TRANSACTIONS",
            "txn_id": txn_id,
            "payee": payee,
            "payer": payer,
            "txn_amount": Decimal(str(txn_amount)),
            "txn_date": datetime.utcnow().isoformat(),
        }

        self.save(item)
        return txn_id

    def get_all_txn_by_client(self, client_id):
        logger.info(f"Search all TRANSACTIONS by Client ID: {client_id}...")
        ke = Key('sk').eq('TRANSACTIONS')
        fe = Attr('payer').eq(client_id)
        pe = 'txn_id, payee, payer, txn_amount, txn_date'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        print(data)
        return data

    def get_all_txn_on_date(self, txn_date):
        logger.info(f"Search all TRANSACTIONS on date: {txn_date}...")
        ke = Key('sk').eq('TRANSACTIONS')
        fe = Attr('txn_date').eq(txn_date)
        pe = 'txn_id, payee, payer, txn_amount, txn_date'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        print(data)
        return data

    def get_all_txn_bw_dates(self, start_date, end_date):
        logger.info(f"Search all TRANSACTIONS between {start_date}-{end_date} ...")
        ke = Key('sk').eq('TRANSACTIONS')
        fe = Attr('txn_date').between(start_date, end_date)
        pe = 'txn_id, payee, payer, txn_amount, txn_date'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        print(data)
        return data
