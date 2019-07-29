from datetime import datetime

from models.enums import ModelNameEnum, TransactionTypeEnum, AccountTypeEnum
from models import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.utcnow().isoformat()
logger = get_logger(__name__)


class DuesModel(RetailModel):
    def __init__(self):
        super(DuesModel, self).__init__()
        self.table = ModelNameEnum.DUES.value

    def generate_new_dues_id(self):
        """
        get the number of pk that starts with "dues"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        return _id

    def insert(self, dues):
        logger.info(">>> Inserting DUES")
        dues_id = self.generate_new_dues_id()
        order_id = 0
        account_id = 0
        store_id = 0
        amount = 0
        account_type = AccountTypeEnum.PURCHASE.value
        transaction_type = TransactionTypeEnum.CREDIT.value or TransactionTypeEnum.DEBIT.value

        item = {
            "pk": f"dues#{dues_id}",
            "sk": self.table,
            "account_id": account_id,
            "order_id": order_id,
            "store_id": store_id,
            "dues_id": dues_id,
            "transaction_type": transaction_type,
            "transaction_datetime": TIMESTAMP,
            "account_type": account_type,
            "amount": amount,
        }
        self.save(item)
        return dues_id
