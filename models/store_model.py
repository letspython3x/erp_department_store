from datetime import datetime

from boto3.dynamodb.conditions import Key

from models import RetailModel
from models.enums import ModelNameEnum
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class StoreModel(RetailModel):
    def __init__(self):
        logger.info("Initializing Store...")
        super(StoreModel, self).__init__()
        self.table = ModelNameEnum.STORE.value

    def generate_new_store_id(self):
        """
        get the number of pk that starts with "store"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        print(_id)
        return _id

    def insert(self, store):
        store_id = self.generate_new_store_id()
        store_name = store.get('store_name')
        store_admin = store.get('store_admin')
        city = store.get('city')
        country = store.get('country')
        postal_code = store.get('postal_code')
        address = store.get('address')
        phone = store.get('phone')

        item = dict(
            pk=f"stores#{store_id}",
            sk="STORE",
            data=f"{store_name}#{store_admin}#{country}#{city}",
            store_id=store_id
        )
        item.update(store)
        already_existing_id = self.if_item_already_exists(item, sk='STORE')
        if already_existing_id:
            return already_existing_id
        else:
            if self.save(item):
                return store_id

    def search_by_store_id(self, store_id):
        val = f"{'stores'}#{store_id}"
        logger.info(f"Searching the Store by ID: {store_id}")
        return self.get_by_partition_key(val)

    def get_all_stores(self):
        response = self.model.query(
            IndexName='gsi_1',
            KeyConditionExpression=Key('sk').eq('STORE'))
        data = response['Items']
        data.sort(key=lambda item: item.get('store_name'))
        return data
