from datetime import datetime

from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
from models.retail_model import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class ReportModel(RetailModel):
    def __init__(self):
        super(ReportModel, self).__init__()
        # self.table = 'Report'

    def get_count_of_active_products(self):
        count = self.get_num_records(_type="PRODUCT")
        return count

    def get_count_of_current_month_orders(self):
        count = self.get_num_records(_type="ORDER")
        return count

    def get_count_of_customers(self):
        count = self.get_num_records(_type="CUSTOMER")
        return count

    def get_count_of_platinum_customers(self):
        count = self.get_num_records(_type="CUSTOMER")
        return count

    def get_count_of_gold_customers(self):
        count = self.get_num_records(_type="CUSTOMER")
        return count

    def get_count_of_silver_customers(self):
        count = self.get_num_records(_type="CUSTOMER")
        return count


    @staticmethod
    def get_revenue_generated_current_month():
        return 0
