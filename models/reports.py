from datetime import datetime

from models import AccountModel, CategoryModel, ClientModel, DuesModel, OrderModel, ProductModel, SaleModel, StoreModel, \
    TraderModel, TransactionModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class Reports():
    def __init__(self):
        pass

    def get_count_of_active_products(self):
        count = self.get_num_records(_type="PRODUCT")
        return count

    def get_count_of_current_month_orders(self):
        count = self.get_num_records(_type="ORDER")
        return count

    def get_count_of_clients(self):
        count = self.get_num_records(_type="CLIENT")
        return count

    def get_count_of_platinum_clients(self):
        count = self.get_num_records(_type="CLIENT")
        return count

    def get_count_of_gold_clients(self):
        count = self.get_num_records(_type="CLIENT")
        return count

    def get_count_of_silver_clients(self):
        count = self.get_num_records(_type="CLIENT")
        return count

    @staticmethod
    def get_revenue_generated_current_month():
        return 0
