from datetime import datetime
from decimal import Decimal

from boto3.dynamodb.conditions import Key, Attr

from models.enums import ModelNameEnum
from models.retail_model import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class ProductModel(RetailModel):
    def __init__(self):
        super(ProductModel, self).__init__()
        self.table = ModelNameEnum.PRODUCT.value

    def delete_product(self, product_id):
        """
        Mark the product as in active by SET is_active=0
        :param product_id:
        :return:
        """
        key = {'pk': f"{'products'}#{product_id}", "sk": "PRODUCT"}
        UpdateExpression = "SET is_active=:is_active"
        ExpressionAttributeValues = {":is_active": 0}
        self.update(key, UpdateExpression, ExpressionAttributeValues)
        return product_id

    def generate_new_product_id(self):
        """
        get the number of pk that starts with "product"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        print(_id)
        return _id

    def get_changed_elements(self, product_id, new_product):
        ori_product = self.search_by_product_id(product_id)[0]
        changes = {}
        for key in new_product.keys():
            if ori_product.get(key) and new_product.get(key) == ori_product.get(key):
                changes[key] = ori_product.get(key)
            else:
                changes[key] = new_product.get(key)
        # print("Changed : ", changes)
        return changes

    def get_recent_products(self, limit):
        print(limit)
        response = self.model.query(
            IndexName='gsi_1',
            KeyConditionExpression=Key('sk').eq('PRODUCT'),
            FilterExpression=Attr('is_active').eq(1),
            Limit=limit)

        products = self.remove_db_col(response['Items'])
        products.sort(key=lambda item: item.get('product_name'), reverse=False)
        return products

    def insert(self, product):
        product_id = self.generate_new_product_id()
        product['product_id'] = product_id
        category_id = product.get('category_id')
        description = product.get('description')
        is_active = product.get("is_active", 1)
        product_name = product.get('product_name')
        sell_price = Decimal(product.get('sell_price'))
        serial_no = product.get('serial_no')
        supplier_id = product.get('supplier_id')
        units_in_stock = int(product.get('units_in_stock', 0))
        unit_price = Decimal(product.get('unit_price'))

        item = {
            "pk": f"{'products'}#{product_id}",
            "sk": f"PRODUCT",
            "data": f"{product_name}#{category_id}#{serial_no}#{is_active}"
        }

        item.update(product)
        already_existing_id = self.if_item_already_exists(item, sk='PRODUCT')
        if already_existing_id:
            return already_existing_id
        else:
            if self.save(item):
                return product_id

    def search_by_product_id(self, product_id):
        val = f"{'products'}#{product_id}"
        logger.info(f"Searching the product ID: {product_id} ...")
        product = self.get_by_partition_key(val)
        return product

    def search_by_name(self, product_name):
        # val = f"{product_name}"
        logger.info(f"Searching the PRODUCT by Name: {product_name} ...")
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('PRODUCT') & Key('data').begins_with(
                                        product_name))
        data = response['Items']
        return data

    def search_by_barcode(self, barcode_number):
        logger.info("Searching by Barcode Number: %s" % barcode_number)
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('PRODUCT'),
                                    FilterExpression=Attr('barcode_number').eq(barcode_number))
        return (response['Items'])

    def search_by_serial_no(self, serial_no):
        logger.info("Searching by Serial Number: %s" % serial_no)
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('PRODUCT'),
                                    FilterExpression=Attr('serial_no').eq(serial_no))
        return response['Items']

    def update_product_item(self, product_id, product):
        print(self.get_by_partition_key(product_id))
        product.pop('product_id')
        product.pop('description')
        product.pop('sell_price')
        product.pop('unit_price')
        key = {'pk': f"{'products'}#{product_id}", "sk": "PRODUCT"}
        print("KEY : ", key)
        attribute_updates = self.get_changed_elements(product_id, product)
        # print("attribute_updates ", attribute_updates)

        UpdateExpression = "SET "
        ExpressionAttributeValues = {}

        for k in attribute_updates.keys():
            UpdateExpression += "{}=:{}, ".format(k, k)
            ExpressionAttributeValues.update({
                ":{}".format(k): str(attribute_updates.get(k))
            })

        self.update(key, UpdateExpression[:-2], ExpressionAttributeValues)

    def update_quantity_in_stocks(self, product_id, quantity, increase=False):
        key = {'pk': f"{'products'}#{product_id}", "sk": "PRODUCT"}
        self.search_by_product_id(product_id)
        UpdateExpression = "ADD units_in_stock :units_in_stock"
        ExpressionAttributeValues = {
            ":units_in_stock": quantity if increase else int('-' + str(quantity))
        }
        updated_data = self.update(key, UpdateExpression, ExpressionAttributeValues)
        quantity = updated_data["units_in_stock"]
        logger.info(f"Quantity of Product : {product_id} is " + "increased" if increase else "decreased")
        return quantity
