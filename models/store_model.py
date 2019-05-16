from datetime import datetime

from models.base_model import BaseModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class StoreModel(BaseModel):
    def __init__(self, store=None):
        logger.info("Initializing Customer...")
        super(StoreModel, self).__init__(table_name='Store')
        if store:
            print("Fetching Customer details...")
            self.name = store.get('name')
            self.address = store.get('address')
            self.country = store.get('country')

        self.table_name = 'store'
        self.pk_key = 'store_id'
        self.store_id = 0

    def create(self):
        store_id = self.db.get_total_records_count() + 1
        logger.info(f"Saving the New Store, ID: %s" % store_id)
        record = dict(
            store_id=store_id,
            name=self.name,
            address=self.address,
            country=self.country
        )
        is_added = self.db.add_new_records(record, pk_key=self.pk_key)
        if is_added:
            logger.info(f"New Store Saved successfully; ID:{store_id}")
            self.store_id = store_id

    def get_record_by_id(self, _id):
        record = self.search_by_id(pk_key=self.pk_key, pk_val=_id)
        if record:
            return record[0]

    def get_all_records(self):
        print("fetching all records")
        records = self.fetch_all(pk_key=self.pk_key)
        return records
