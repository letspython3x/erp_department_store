from datetime import datetime

from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
from models.retail_model import RetailModel
from models.account_model import AccountModel
from utils.generic_utils import get_logger
from models.enums import ModelNameEnum, TransactionTypeEnum, OrderTypeEnum, OrderSubTypeEnum

TIMESTAMP = datetime.now
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
        transaction_id = self.generate_new_txn_id()
        payee_account_name = transaction.get('payee_account_name')
        payer_account_name = transaction.get('payer_account_name')
        transaction_amount = transaction.get('transaction_amount')

        if transaction.get('order_type').upper() == OrderTypeEnum.INVOICE.value:
            order_type = OrderTypeEnum.INVOICE.value

        if transaction.get('order_sub_type').upper() == OrderSubTypeEnum.PURCHASE.value:
            order_sub_type = OrderSubTypeEnum.PURCHASE.value
        elif transaction.get('order_sub_type').upper() == OrderSubTypeEnum.SALE.value:
            order_sub_type = OrderSubTypeEnum.SALE.value

        if transaction.get('transaction_type').upper() == TransactionTypeEnum.CASH.value:
            transaction_type = TransactionTypeEnum.CASH.value
        elif transaction.get('transaction_type').upper() == TransactionTypeEnum.CREDIT.value:
            transaction_type = TransactionTypeEnum.CREDIT.value

        item = {
            "pk": f"transactions#{transaction_id}",
            "sk": self.table,
            "transaction_id": transaction_id,
            "payee_account_name": payee_account_name,
            "payer_account_name": payer_account_name,
            "transaction_amount": Decimal(str(transaction_amount)),
            "transaction_date": datetime.utcnow().isoformat(),
            "order_type": order_type,
            "order_sub_type": order_sub_type,
            "transaction_type": transaction_type
        }
        self.save(item)
        AccountModel().update_account(item)
        return transaction_id

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
