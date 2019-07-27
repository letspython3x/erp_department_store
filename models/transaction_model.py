from datetime import datetime

from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
from models.retail_model import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class AccountModel(RetailModel):
    def __init__(self):
        super(AccountModel, self).__init__()
        self.table = 'ACCOUNTS'

    def generate_new_txn_id(self):
        """
        get the number of pk that starts with "customers"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        return _id

    def insert(self):
        txn_id = self.generate_new_txn_id()
        self.update_receivables(txn_id)
        self.update_payables(txn_id)
        self.update_income(txn_id)
        self.update_expenses(txn_id)

        item = {
            "pk": f"transactions#{txn_id}",
            "sk": f"TRANSACTIONS",
            "payee": "",
            "payer": "",
            "txn_amount": "",
            "txn_date": datetime.utcnow().isoformat(),
        }

    def update_receivables(self, txn_id):
        """
        Accounts Recievables

        - Customer Open Items
        - Customer cleared items.

        :param txn_id:
        :return:
        """
        pass

    def update_payables(self, txn_id):
        """
         - Vendor Open Items
         - Vendor cleared items.
        :param txn_id:
        :return:
        """
        pass

    def update_income(self, txn_id):
        pass

    def update_expenses(self, txn_id):
        pass
