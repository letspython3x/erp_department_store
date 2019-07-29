# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html#GettingStarted.Python.03.03
from datetime import datetime

import simplejson as json
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from utils.generic_utils import get_logger, get_app_config

TIMESTAMP = datetime.now
logger = get_logger(__name__)
local_dynamo_db = get_app_config()["local_dynamo_db"]

endpoint_url = r"http://localhost:8000"


class RetailModel:
    def __init__(self):
        logger.info("Initializing Retail Table...")
        self.table_name = 'Retail'

    @property
    def model(self):
        dynamo = resource('dynamodb', endpoint_url=endpoint_url)
        return dynamo.Table(self.table_name)

    def get_by_partition_key(self, pk):
        try:
            # response = self.model.get_item(Key={'pk': 'categories#1'})
            response = self.model.query(
                KeyConditionExpression=Key('pk').eq(pk),
            )
            # items = self.remove_db_col(response['Items'])
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
        else:
            logger.info("%s GetItem succeeded:" % self.get_by_partition_key.__name__)
            items = self.remove_db_col(response['Items'])
            # logger.info(json.dumps(items, indent=4))
            return items

    def get_records_begins_with_pk(self, _str):
        try:
            response = self.model.query(
                KeyConditionExpression=Key('pk').begins_with(_str),
            )
        except ClientError as e:
            logger.error(e)
            logger.error(e.response['Error']['Message'])
        else:
            logger.info("%s GetItem succeeded:" % self.get_records_begins_with_pk.__name__)
            items = self.remove_db_col(response['Items'])
            # logger.info(json.dumps(item, indent=4))
            return items

    def get_by_sort_key(self, sk):
        try:
            response = self.model.query(
                IndexName='gsi_1',
                KeyConditionExpression=Key('sk').eq(sk),
            )
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
            logger.info(e.response['Error']['Message'])
        else:
            logger.info("%s GetItem succeeded:" % self.get_by_sort_key.__name__)
            items = self.remove_db_col(response['Items'])
            return items

    def get_num_records(self, _type):
        response = self.model.query(
            IndexName='gsi_1',
            KeyConditionExpression=Key('sk').eq(_type)
        )
        return len(response['Items'])

    def if_item_already_exists(self, item, sk):
        data = item["data"]
        response = self.model.query(
            IndexName='gsi_1',
            KeyConditionExpression=Key('sk').eq(sk) & Key('data').eq(data))

        # logger.info(response["Items"])

        return None if len(response["Items"]) == 0 else response["Items"][0].get('pk')

    def save(self, item):
        """
        To be implemented in the child classes
        :param item: item to save in model
        :return: bool
        """
        # TODO: Check if the item is already existing with same ID
        try:
            self.model.put_item(Item=item)
            logger.info(f"Records Saved Successfully")
            return True
        except Exception as e:
            logger.error(f"Records did not save !!!")
            logger.error(f"{e}")

    def teardown(self):
        self.model.delete()

    def delete(self, pk_val, sk):
        """
        Delete the item from a table on the basis of its Primary Key
        :param pk_val: Value of the Key to delete
        :return: Boolean True
        """
        logger.info(f"Deleting the record, pk: {pk_val}")
        # self.model.delete_item(Key={'pk': pk_val})
        self.model.delete_item(Key={'pk': pk_val, 'sk': sk})
        return True

    def update(self, key, UpdateExpression, ExpressionAttributeValues, ReturnValues="UPDATED_NEW"):
        # logger.info(key)
        response = self.model.update_item(
            Key=key,
            UpdateExpression=UpdateExpression,
            ExpressionAttributeValues=ExpressionAttributeValues,
            ReturnValues=ReturnValues
        )
        # response = self.model.update_item(
        #     Key={
        #         'year': year,
        #         'title': title
        #     },
        #     UpdateExpression="set info.rating = :r, info.plot=:p, info.actors=:a",
        #     ExpressionAttributeValues={
        #         ':r': decimal.Decimal(5.5),
        #         ':p': "Everything happens all at once.",
        #         ':a': ["Larry", "Moe", "Curly"]
        #     },
        #     ReturnValues=ReturnValues
        # )
        logger.info("UpdateItem succeeded:")
        data = response["Attributes"]
        # logger.info(json.dumps(response, indent=4))
        # logger.info(data)
        return data

    def query_records(self, index_name, ke, fe, pe):
        # index_name = "NULL"  # None #'gsi_1'
        # ke = Key('sk').eq('products#2')
        # fe = Attr('productName').eq('Chang')
        # pe = 'unitsInStock, quantityPerUnit'

        if index_name:
            response = self.model.query(
                IndexName=index_name,
                KeyConditionExpression=ke,
                FilterExpression=fe,
                ProjectionExpression=pe,
            )
        else:
            response = self.model.query(
                KeyConditionExpression=ke,
                FilterExpression=fe,
                ProjectionExpression=pe,
            )

        items = self.remove_db_col(response['Items'])
        logger.info(items)
        return items

    def scan_all_records(self, fe, pe, ean):

        # fe = Key('pk').eq('products#2')
        # pe = "#desc, Title, BicycleType"
        # # Expression Attribute Names for Projection Expression only.
        # ean = {"#desc": "Description", }
        # esk = None

        response = self.model.scan(
            FilterExpression=fe,
            ProjectionExpression=pe,
            ExpressionAttributeNames=ean
        )

        for i in response['Items']:
            logger.info(json.dumps(i))

        while 'LastEvaluatedKey' in response:
            response = self.model.scan(
                ProjectionExpression=pe,
                FilterExpression=fe,
                ExpressionAttributeNames=ean,
                ExclusiveStartKey=response['LastEvaluatedKey']
            )

            # for i in response['Items']:
            #     logger.info(json.dumps(i))

        items = self.remove_db_col(response['Items'])
        logger.info(items)
        return items

    @staticmethod
    def remove_db_col(db_items):
        logger.info(">>> Removing DB Columns")
        if isinstance(db_items, list):
            for p in db_items:
                p.pop("pk", None)
                p.pop("sk", None)
                p.pop("data", None)
        elif isinstance(db_items, dict):
            db_items.pop("pk", None)
            db_items.pop("sk", None)
            db_items.pop("data", None)
        else:
            return db_items
        return db_items
