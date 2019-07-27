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
