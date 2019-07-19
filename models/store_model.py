from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from models.retail_model import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class StoreModel(RetailModel):
    def __init__(self):
        logger.info("Initializing Customer...")
        super(StoreModel, self).__init__()
        self.table = 'STORE'

    def generate_new_store_id(self):
        """
        get the number of pk that starts with "STORE"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        print(_id)
        return _id

    def insert(self, store):
        store_id = self.generate_new_store_id()
        store['store_id'] = store_id
        store_name = store.get('store_name')
        store_admin = store.get('store_admin')
        address = store.get('address')
        phone = store.get('phone')
        city = store.get('city')
        country = store.get('country')
        postal_code = store.get('postal_code')

        item = dict(
            pk=f"stores#{store_id}",
            sk="STORE",
            data="store_name#category_id#store_admin"
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
            KeyConditionExpression=Key('sk').eq('STORE') )
        data = response['Items']
        data.sort(key=lambda item: int(item['pk'].split('#')[1]))
        return data


    @staticmethod
    def reformat(store):
        if isinstance(store, list):
            for p in store:
                p.pop("pk")
                p.pop("sk")
                p.pop("data")
        elif isinstance(store, dict):
            store.pop("pk")
            store.pop("sk")
            store.pop("data")
        else:
            return store
        return store
