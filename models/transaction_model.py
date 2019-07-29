from datetime import datetime

from boto3.dynamodb.conditions import Key, Attr

from models import RetailModel
from models.enums import ModelNameEnum, TransactionTypeEnum, AccountTypeEnum
from utils.generic_utils import get_logger

TIMESTAMP = datetime.utcnow().isoformat()
logger = get_logger(__name__)


class TransactionModel(RetailModel):
    def __init__(self):
        super(TransactionModel, self).__init__()
        self.table = ModelNameEnum.TRANSACTION.value

    def generate_new_txn_id(self):
        """
        get the number of pk that starts with "transactions"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        return _id

    def insert(self, transaction):
        logger.info(">>> Inserting TRANSACTION")
        txn_id = self.generate_new_txn_id()
        order_id = 0
        account_id = 0
        store_id = 0
        amount = 0
        account_type = AccountTypeEnum.PURCHASE.value
        transaction_type = TransactionTypeEnum.CREDIT.value or TransactionTypeEnum.DEBIT.value

        item = {
            "pk": f"transaction#{txn_id}",
            "sk": self.table,
            "account_id": account_id,
            "order_id": order_id,
            "store_id": store_id,
            "transaction_id": txn_id,
            "transaction_type": transaction_type,
            "transaction_datetime": TIMESTAMP,
            "account_type": account_type,
            "amount": amount,
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

    def get_recent_transactions(self, limit=10):
        print(">>> Fetch %d Recent Transactions" % limit)
        response = self.model.query(
            IndexName='gsi_1',
            KeyConditionExpression=Key('sk').eq(self.table),
            # FilterExpression=Attr('is_active').eq(1),
            Limit=limit)

        transactions = self.remove_db_col(response['Items'])
        transactions.sort(key=lambda item: item.get('txn_id'), reverse=False)
        return transactions
