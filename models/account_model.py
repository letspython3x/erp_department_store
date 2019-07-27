from datetime import datetime

from models.retail_model import RetailModel
from models.transaction_model import TransactionModel
from utils.generic_utils import get_logger
from models.enums import ModelNameEnum, TransactionTypeEnum

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class AccountModel(RetailModel):
    def __init__(self):
        super(AccountModel, self).__init__()
        self.table = ModelNameEnum.ACCOUNT.value

    def update_accounts(self, transaction):
        txn_type = transaction.get("txn_type")
        if txn_type == TransactionTypeEnum.SELL_CASH.value:
            self.update_income(transaction)
        elif txn_type in [TransactionTypeEnum.REFUND.value, TransactionTypeEnum.REVERSAL.value]:
            transaction['txn_amount'] = int('-' + str(transaction['txn_amount']))
            self.update_receivables(transaction)
        elif txn_type == TransactionTypeEnum.SELL_CREDIT.value:
            self.update_receivables(transaction)
        elif txn_type == TransactionTypeEnum.BUY_CREDIT.value:
            self.update_payables(transaction)
        elif txn_type == TransactionTypeEnum.BUY_CASH.value:
            self.update_expenses(transaction)

    def update_receivables(self, transaction):
        """
        Accounts Recievables

        - Client Open Items
        - Client cleared items.

        :param txn_id:
        :return:
        """
        txn_id = TransactionModel().insert(transaction)

    def update_payables(self, transaction):
        """
         - Vendor Open Items
         - Vendor cleared items.
        :param txn_id:
        :return:
        """
        txn_id = TransactionModel().insert(transaction)

    def update_income(self, transaction):
        txn_id = TransactionModel().insert(transaction)

    def update_expenses(self, transaction):
        txn_id = TransactionModel().insert(transaction)
