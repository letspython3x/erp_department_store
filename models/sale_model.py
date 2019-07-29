from datetime import datetime

from models import RetailModel
from models.enums import ModelNameEnum, OrderPaymentTypeEnum, AccountTypeEnum
from utils.generic_utils import get_logger

TIMESTAMP = datetime.utcnow().isoformat()
logger = get_logger(__name__)


class SaleModel(RetailModel):
    def __init__(self):
        """
        A Sales model to store all the sales made
        """
        super(SaleModel, self).__init__()
        self.table = ModelNameEnum.SALE.value

    def generate_new_sale_id(self):
        """
        get the number of pk that starts with "sales"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        return _id

    def insert(self, sale):
        logger.info(">>> Inserting SALE")
        sale_id = self.generate_new_sale_id()
        order_id = 0
        account_id = 0
        store_id = 0
        amount = 0
        account_type = AccountTypeEnum.SALE.value
        order_payment_type = OrderPaymentTypeEnum.CASH.value or OrderPaymentTypeEnum.ON_CREDIT.value

        item = {
            "pk": f"sale#{sale_id}",
            "sk": self.table,
            "account_id": account_id,
            "order_id": order_id,
            "store_id": store_id,
            "sale_id": sale_id,
            "order_payment_type": order_payment_type,
            "sale_datetime": TIMESTAMP,
            "account_type": account_type,
            "amount": amount,
        }
        self.save(item)
        return sale_id
