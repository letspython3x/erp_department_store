from datetime import datetime

from boto3.dynamodb.conditions import Key

from models import RetailModel
from models.enums import ModelNameEnum
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class TraderModel(RetailModel):
    def __init__(self):
        logger.info("Initializing Trader...")
        super(TraderModel, self).__init__()
        self.table = ModelNameEnum.TRADER.value

    def generate_new_trader_id(self):
        """
        get the number of pk that starts with "store"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        print(_id)
        return _id

    def insert(self, trader):
        trader_id = self.generate_new_trader_id()
        primary_phone = trader.get("primary_phone")
        email = trader.get("email")
        city = trader.get('city')
        country = trader.get("country")
        company_name = trader.get('company_name')
        contact_name = trader.get("contact_name")
        address = trader.get('address')
        phone = trader.get('phone')
        postal_code = trader.get('postal_code')
        secondary_phone = trader.get("secondary_phone")
        fax = trader.get("fax")

        item = dict(
            pk=f"traders#{trader_id}",
            sk=self.table,
            data=f"{primary_phone}#{email}#{country}#{city}",
            trader_id=trader_id,
            entity_type=self.table)

        item.update(trader)
        already_existing_id = self.if_item_already_exists(item, sk='TRADER')
        if already_existing_id:
            return already_existing_id
        else:
            if self.save(item):
                return trader_id

    def search_by_trader_id(self, trader_id):
        val = f"{'traders'}#{trader_id}"
        logger.info(f"Searching the TRADER by ID: {trader_id}")
        return self.get_by_partition_key(val)

    def get_all_traders(self):
        response = self.model.query(
            IndexName='gsi_1',
            KeyConditionExpression=Key('sk').eq('TRADER'))
        data = response['Items']
        data.sort(key=lambda item: item.get('trader_id'))
        return data
