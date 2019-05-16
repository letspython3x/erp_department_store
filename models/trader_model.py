from datetime import datetime

from models.base_model import BaseModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class TraderModel(BaseModel):
    def __init__(self, trader=None):
        logger.info("Initializing Customer...")
        super(TraderModel, self).__init__(table_name='Trader')
        if trader:
            print("Fetching Customer details...")
            self.name = trader.get('name')
            self.address = trader.get('address')
            self.country = trader.get('country')

        self.table_name = 'Trader'
        self.pk_key = 'trader_id'
        self.trader_id = 0

    def create(self):
        trader_id = self.db.get_total_records_count() + 1
        logger.info(f"Saving the New Trader, ID: %s" % trader_id)
        record = dict(
            trader_id=trader_id,
            name=self.name,
            address=self.address,
            country=self.country
        )
        is_added = self.db.add_new_records(record, pk_key=self.pk_key)
        if is_added:
            logger.info(f"New Trader Saved successfully; ID:{trader_id}")
            self.trader_id = trader_id

    def get_record_by_id(self, _id):
        record = self.search_by_id(pk_key=self.pk_key, pk_val=_id)
        if record:
            return record[0]

    def get_all_records(self):
        print("fetching all records")
        records = self.fetch_all(pk_key=self.pk_key)
        return records
