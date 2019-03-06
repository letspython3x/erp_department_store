from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key, And
from botocore.exceptions import ClientError

from erp_department_store.utils.generic_utils import get_logger, get_app_config

logger = get_logger(__name__)
local_dynamo_db = get_app_config()["local_dynamo_db"]

endpoint_url = r"http://localhost:8000"


class Db(object):
    """
    creates a DynamoDb object
    """

    def __enter__(self):
        logger.info("Creating Database resource...")
        # endpoint_url = self.endpoint_url
        self.dynamo = resource('dynamodb', endpoint_url=endpoint_url)
        return self.dynamo

    def __exit__(self, exc, typ, val):
        if exc:
            logger.error("Exception: %s \n %s \n %s" % (str(exc), str(typ), str(val)))

    @property
    def endpoint_url(self):
        """
        :return: endpoint_url for making DynamoDb connection
        """
        url = local_dynamo_db["endpoint_url"]
        return url

    @property
    def region(self):
        return ''


class DbOperations(object):
    def __init__(self, table_name):
        logger.info(f"Initializing DynamoDB Table: {table_name}")
        self.table_name = table_name

    @property
    def table(self):
        with Db() as db:
            tbl = db.Table(self.table_name)
            return tbl

    def get_total_records_count(self):
        c = self.table.item_count
        logger.info(f"Total Items in {self.table} is {c}")
        return c

    def get_table_last_record(self, pk_key):
        data = self.scan_table(pk_key)
        if data:
            logger.info(f"Returning Last Record")
            return data[-1]

    def save_records(self, records, pk_key=None):
        logger.info(f"Saving records in table: {self.table_name}")
        logger.info(f"Record Type: {type(records)} \nRecords: {records}")

        if isinstance(records, list) and len(records) >= 1:
            # more than one items to save in db
            for r in records:
                pk_val = r.get(pk_key, None)
                self.table.put_item(
                    Item=r,
                    ConditionExpression=Attr(pk_key).ne(pk_val) if pk_key else ''
                )
        else:
            pk_val = records.get(pk_key, None)
            self.table.put_item(
                Item=records,
                ConditionExpression=Attr(pk_key).ne(pk_val) if pk_key else ''
            )
        logger.info(f"Records Saved Successfully")

    def delete(self, pk_key, pk_val):
        """
        Delete the item from a table on the basis of its Primary Key
        :param pk_key: Primary Key of the table
        :param pk_val: Value of the Key to delete
        :return: True
        """
        self.table.delete_item(Key={pk_key: pk_val})
        return True

    def search_by_key(self, query_params):
        """
        Search a record on the basis of the Primary Key
        :param query_params: Key Params a dict
        :return: List of records that matched
        """
        logger.info(f"Query Params to Search by Key: {query_params}")
        if isinstance(query_params, dict):
            for pk_key, pk_value in query_params.items():
                key_exp = Key(pk_key).eq(pk_value)
        else:
            raise RuntimeError(f"Invalid Query Parameters provided {query_params}")
        try:
            response = self.table.query(
                KeyConditionExpression=key_exp
            )
        except ClientError as e:
            logger.error(f"Invalid Query Parameters provided {query_params}")
            logger.error(e.response['Error']['Message'])
            raise
        else:
            # Pick only the 1st element from the whole scan
            if response["Items"]:
                record = response["Items"]
                logger.info(f"Record Found: {record}")
                return record
            else:
                logger.info(f"{query_params} does not Match any record")

    def search_by_attributes(self, query_params):
        """

        :param query_params: accepts a list of dictionaries
        :return: filter Expression of `Attr` and `contains` for scan method
        """
        logger.info(f"Search by Attributes: {query_params}")
        filter_exp = self.get_filter_expression(query_params)
        try:
            response = self.table.scan(
                FilterExpression=filter_exp,
                Limit=100)

            while 'LastEvaluatedKey' in response:
                response = self.table.scan(
                    FilterExpression=filter_exp,
                    Limit=100,
                    ExclusiveStartKey=response['LastEvaluatedKey'])
            # //do something with each batch of 100 entries
        except ClientError as e:
            logger.error("Invalid Attributes provided {query_params}")
            logger.error(e.response['Error']['Message'])
            raise
        else:
            # Pick only the 1st element from the whole scan
            if response["Items"]:
                records = response["Items"]
                logger.info(f"Records Found on the basis of Attributes: {records}")
                return records
            else:
                logger.info(f"{query_params} does not Match any record")

    @staticmethod
    def get_filter_expression(query_params):
        """

        :param query_params: accepts a list of dictionaries
        :return: filter Expression of `Attr` and `contains` for scan method
        """
        logger.info(f"Generating Filter Expression from: {query_params}")
        filter_exp_list = []
        # if isinstance(list, query_params) and len(query_params) == 2:
        if isinstance(query_params, list) and len(query_params) >= 2:
            for query in query_params:
                for prop_name, prop_value in query.items():
                    filter_exp_list.append(Attr(prop_name).eq(prop_value))
            filter_exp = And(*filter_exp_list)

        elif isinstance(query_params, dict):
            for k, v in query_params.items():
                filter_exp = Attr(k).eq(str(v))
        return filter_exp

    def scan_table(self, sort_by=None):
        logger.info(f"Scanning all records of the table: {self.table_name}")
        logger.info(f"Schema: {self.table.key_schema}")

        # it is not possible to scan a table in a sorted manner
        response = self.table.scan()
        records = response['Items']

        # To Get all data > 1MB fom table
        while response.get('LastEvaluatedKey'):
            response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            records.extend(response['Items'])

        # try to implement some optimization here so as to fetch data in sorted order
        if sort_by:
            logger.info(f"Sorting the data on the basis of: {sort_by}")
            records.sort(key=lambda x: x[sort_by])
        return records
