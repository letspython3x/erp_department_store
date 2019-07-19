from datetime import datetime

from boto3.dynamodb.conditions import Key, Attr
from models.retail_model import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class CategoryModel(RetailModel):
    def __init__(self):
        super(CategoryModel, self).__init__()
        self.table = 'CATEGORY'

    def generate_new_category_id(self):
        """
        get the number of pk that starts with "category"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        print(_id)
        return _id

    def insert(self, category):
        category_id = self.generate_new_category_id()
        category_name = category.get('category_name')
        description = category.get('description')

        item = {
            "pk": f"{'categories'}#{category_id}",
            "sk": f"PRODUCT",
            "data": f"{category_name}#{description}",
            "category_id": category_id,
            "category_name": category_name,
            "description": description
        }
        already_existing_id = self.if_item_already_exists(item, sk='CATEGORY')
        if already_existing_id:
            return already_existing_id
        else:
            if self.save(item):
                return category_id

    def search_by_category_id(self, category_id):
        val = f"{'categories'}#{category_id}"
        logger.info(f"Searching the category ID: {category_id} ...")
        return self.get_by_partition_key(val)

    def search_by_name(self, category_name):
        # val = f"{category_name}"
        logger.info(f"Searching CATEGORY by Name: {category_name} ...")
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('CATEGORY'),
                                    FilterExpression=Attr('category_name').contains(category_name))
        data = response['Items']
        return data

    def get_all_categories(self, limit=None):
        if limit is None:
            response = self.model.query(
                IndexName='gsi_1',
                KeyConditionExpression=Key('sk').eq('CATEGORY'))
        else:
            print("Limiting the search to %s" % limit)
            response = self.model.query(
                IndexName='gsi_1',
                KeyConditionExpression=Key('sk').eq('CATEGORY'),
                Limit=limit)

        data = response['Items']
        data.sort(key=lambda item: int(item['pk'].split('#')[1]))
        return data

    def update_category(self, category_id, category):
        # TODO : Update the category
        print(self.get_by_partition_key(category_id))
        category_id = category.get('category_id')
        description = category.get('description')
        category_name = category.get('category_name')

        key = {'pk': f"{'categories'}#{category_id}", "sk": "CATEGORY"}
        print("KEY : ", key)
        attribute_updates = {'category_name': category_name, 'description': description}
        # print("attribute_updates ", attribute_updates)

        UpdateExpression = "SET "
        ExpressionAttributeValues = {}

        for k in attribute_updates.keys():
            UpdateExpression += "{}=:{}, ".format(k, k)
            ExpressionAttributeValues.update({
                ":{}".format(k): str(attribute_updates.get(k))
            })

        self.update(key, UpdateExpression[:-2], ExpressionAttributeValues)


# print(CategoryModel().get_all_categories(5))
# print(CategoryModel().search_by_name('Beverages'))
# print(CategoryModel().search_by_category_id(10))
