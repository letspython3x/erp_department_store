from datetime import datetime

from models import RetailModel
from models.enums import ModelNameEnum, AccountTypeEnum, OrderPaymentTypeEnum
from utils.generic_utils import get_logger

TIMESTAMP = datetime.utcnow().isoformat()
logger = get_logger(__name__)


class PurchaseModel(RetailModel):
    def __init__(self):
        """
        A Purchase model to store all the purchases made
        """
        super(PurchaseModel, self).__init__()
        self.table = ModelNameEnum.PURCHASE.value

    def generate_new_purchase_id(self):
        """
        get the number of pk that starts with "transactions"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        return _id

    def insert(self, purchase):
        logger.info(">>> Inserting PURCHASE")
        purchase_id = self.generate_new_purchase_id()
        order_id = 0
        account_id = 0
        store_id = 0
        amount = 0
        account_type = AccountTypeEnum.PURCHASE.value
        order_payment_type = OrderPaymentTypeEnum.CASH.value or OrderPaymentTypeEnum.ON_CREDIT.value

        item = {
            "pk": f"purchase#{purchase_id}",
            "sk": self.table,
            "account_id": account_id,
            "order_id": order_id,
            "store_id": store_id,
            "purchase_id": purchase_id,
            "order_payment_type": order_payment_type,
            "sale_datetime": TIMESTAMP,
            "account_type": account_type,
            "amount": amount,
        }
        self.save(item)
        return purchase_id
