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
