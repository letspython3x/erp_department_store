from datetime import datetime

from boto3.dynamodb.conditions import Key, Attr

from models.enums import ModelNameEnum
from models.retail_model import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class ClientModel(RetailModel):
    def __init__(self):
        logger.info("Initializing Client...")
        super(ClientModel, self).__init__()
        self.table = ModelNameEnum.CLIENT.value

    def generate_new_client_id(self):
        """
        get the number of pk that starts with "clients"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        return _id

    def insert(self, client):
        client_id = self.generate_new_client_id()
        client['client_id'] = client_id

        primary_phone = client.get("primary_phone")
        email = client.get("email")
        country = client.get("country", '')
        state = client.get("state")
        first_name = client.get('first_name')
        middle_name = client.get('middle_name', "#")
        last_name = client.get('last_name')
        client_type = client.get("client_type")
        secondary_phone = client.get("secondary_phone")
        fax = client.get("fax")
        gender = client.get("gender")
        is_active = client.get("is_active")
        membership = client.get("membership")
        postal_code = client.get("postal_code")
        city = client.get("city")
        address = client.get("address")
        contact_title = client.get("contact_title")

        item = {
            "pk": f"clients#{client_id}",
            "sk": f"CLIENT",
            "data": f"{primary_phone}#{email}#{country}#{state}"
        }
        item.update(client)

        if self.model.save(item):
            return client_id

    def search_by_client_id(self, client_id):
        val = f"clients#{client_id}"
        logger.info(f"Searching the Client by ID: {client_id} ...")
        client = self.get_by_partition_key(val)
        return client

    def search_by_email(self, email):
        logger.info("Searching by phone number: %s" % email)
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('CLIENT'),
                                    FilterExpression=Attr('email').eq(email)
                                    )
        client = self.remove_db_col(response['Items'])
        return client

    def search_by_phone(self, phone):
        logger.info("Searching by phone number: %s" % phone)
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('CLIENT'),
                                    FilterExpression=Attr('primary_phone').eq(phone) or Attr('secondary_phone').eq(
                                        phone)
                                    )
        client = self.remove_db_col(response['Items'])
        return client

    def search_by_name(self, first_name, last_name, middle_name='NULL'):
        logger.info(f"Searching the Client by Name: {first_name} {last_name} ...")
        response = self.model.query(IndexName='gsi_1',
                                    KeyConditionExpression=Key('sk').eq('CLIENT'),
                                    FilterExpression=Attr('first_name').eq(first_name) and Attr('last_name').eq(
                                        last_name) and Attr('middle_name').eq(middle_name))
        client = self.remove_db_col(response['Items'])
        return client

    def get_recent_clients(self, limit):
        logger.info("Limiting Query Results to %s" % limit)
        response = self.model.query(
            IndexName='gsi_1',
            KeyConditionExpression=Key('sk').eq('CLIENT'),
            FilterExpression=Attr('is_active').eq(1),
            Limit=limit)
        clients = self.remove_db_col(response['Items'])
        return clients

    def delete_client(self, client_id):
        """
        Mark the client as in active by SET is_active=0
        :param client_id:
        :return:
        """
        key = {'pk': f"{'clients'}#{client_id}", "sk": "CLIENT"}
        UpdateExpression = "SET is_active=:is_active"
        ExpressionAttributeValues = {":is_active": 0}
        self.update(key, UpdateExpression, ExpressionAttributeValues)
        return client_id

    def update_client(self, client_id, client):
        return 0
