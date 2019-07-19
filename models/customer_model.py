from datetime import datetime

from boto3.dynamodb.conditions import Key, Attr

from models.retail_model import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class CustomerModel(RetailModel):
    def __init__(self):
        logger.info("Initializing Customer...")
        super(CustomerModel, self).__init__()
        self.table = "CUSTOMER"

    def generate_new_customer_id(self):
        """
        get the number of pk that starts with "customers"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        return _id

    def insert(self, customer):
        customer_id = self.generate_new_customer_id()
        customer['customer_id'] = customer_id

        primary_phone = customer.get("primary_phone")
        email = customer.get("email")
        country = customer.get("country", '')
        state = customer.get("state")

        item = {
            "pk": f"customers#{customer_id}",
            "sk": f"CUSTOMER",
            "data": f"{primary_phone}#{email}#{country}#{state}"
        }
        item.update(customer)

        if self.model.save(item):
            return customer_id

    def search_by_customer_id(self, customer_id):
        val = f"customers#{customer_id}"
        logger.info(f"Searching the Customer by ID: {customer_id} ...")
        customer = self.get_by_partition_key(val)
        return customer


    def search_by_email(self, email):
        logger.info("Searching by phone number: %s" % email)
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('CUSTOMER'),
                                    FilterExpression=Attr('email').eq(email)
                                    )
        customer = self.remove_db_col(response['Items'])
        return customer

    def search_by_phone(self, phone):
        logger.info("Searching by phone number: %s" % phone)
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('CUSTOMER'),
                                    FilterExpression=Attr('primary_phone').eq(phone) or Attr('secondary_phone').eq(
                                        phone)
                                    )
        customer = self.remove_db_col(response['Items'])
        return customer

    def search_by_name(self, first_name, last_name, middle_name='NULL'):
        logger.info(f"Searching the Customer by Name: {first_name} {last_name} ...")
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('CUSTOMER'),
                                    FilterExpression=Attr('first_name').eq(first_name) and Attr('last_name').eq(
                                        last_name) and Attr('middle_name').eq(middle_name))
        customer = self.remove_db_col(response['Items'])
        return customer

    def get_recent_customers(self, limit):
        logger.info("Limiting Query Results to %s" % limit)
        response = self.model.query(
            IndexName='gsi_1',
            KeyConditionExpression=Key('sk').eq('CUSTOMER'),
            FilterExpression=Attr('is_active').eq(1),
            Limit=limit)
        customers = self.remove_db_col(response['Items'])
        return customers

    def delete_customer(self, customer_id):
        """
        Mark the customer as in active by SET is_active=0
        :param customer_id:
        :return:
        """
        key = {'pk': f"{'customers'}#{customer_id}", "sk": "CUSTOMER"}
        UpdateExpression = "SET is_active=:is_active"
        ExpressionAttributeValues = {":is_active": 0}
        self.update(key, UpdateExpression, ExpressionAttributeValues)
        return customer_id

    def update_customer(self, customer_id, customer):
        return 0
