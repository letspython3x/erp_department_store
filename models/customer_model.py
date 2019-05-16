from datetime import datetime
from decimal import Decimal
from werkzeug.utils import cached_property

from models.base_model import BaseModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class CustomerModel(BaseModel):
    def __init__(self, customer=None):
        logger.info("Initializing Customer...")
        super(CustomerModel, self).__init__(table_name='Customer')
        if customer:
            print("Fetching Customer details...")
            self.first_name = customer.get('first_name')
            self.middle_name = customer.get('middle_name')
            self.last_name = customer.get('last_name')
            self.email = customer.get("email")
            self.gender = customer.get("gender")
            self.category = customer.get("category")
            self.dob = customer.get("dob")
            self.membership = customer.get("membership")
            self.postcode = customer.get("postcode")
            self.state = customer.get("state")
            self.city = customer.get("city")
            self.country = customer.get("country")
            self.phone = customer.get("phone")
            # self.phone = self.get_phone(customer)
            self.address = self.get_address(customer)

        self.table_name = 'Customer'
        self.pk_key = 'customer_id'

    @cached_property
    def customer_id(self):
        """
        If Customer exists, returns his customer_id
        elif customer does not exist, return the last customer ID recorded.
        :return: Customer ID
        """
        customer = self.search_by_phone() or self.search_by_email() or self.search_by_name()
        if customer:
            customer_id = customer[0][self.pk_key]
            return customer_id

    def search_by_phone(self, phone=None):
        logger.info(f"Searching the Customer by Phone: {phone}...")
        if phone or self.phone:
            query = {
                'phone': phone or self.phone
            }
            record = self.db.search_by_attributes(query)
            return record

    def search_by_email(self, email=None):
        logger.info(f"Searching the Customer by Email: {email}...")
        if email or self.email:
            query = {
                'email': email or self.email
            }
            record = self.db.search_by_attributes(query)
            return record

    def search_by_name(self, first_name=None, last_name=None):
        logger.info(f"Searching the Customer by Name: {first_name} {last_name}...")
        if (first_name and last_name) or (self.first_name and self.last_name):
            query = {
                'first_name': first_name or self.first_name,
                'last_name': last_name or self.last_name
            }
            record = self.db.search_by_attributes(query)
            return record

    # @staticmethod
    # def get_phone(customer):
    #     if customer.get('phone_1') and customer.get('phone_2'):
    #         phone = [customer.get('phone_1'), customer.get('phone_2')]
    #     else:
    #         phone = customer.get('phone_1') or customer.get('phone_2')
    #     return phone

    @staticmethod
    def get_address(customer):
        if customer.get('address_1') and customer.get('address_2'):
            address = [customer.get('address_1'), customer.get('address_2')]
        else:
            address = customer.get('address_1') or customer.get('address_2')
        return address

    def create(self):
        """
        saves the customer if it does not exist, after incrementing the last customer's id
        :return: None
        """
        customer_id = self.customer_id
        if not customer_id:
            logger.info(f"Saving the New Customer...")
            customer_id = int(self.last_record[self.pk_key]) + 1  # if self.last_record else 1
            logger.info(f"New Customer ID: {customer_id}")
            record = dict(
                customer_id=customer_id,
                first_name=self.first_name,
                middle_name=self.middle_name,
                last_name=self.last_name,
                gender=self.gender,
                phone=self.phone,
                email=self.email,
                category=self.category,
                dob=self.dob,
                membership=self.membership,
                address=self.address,
                city=self.city or '(null)',
                state=self.state or '(null)',
                country=self.country or '(null)',
                postcode=self.postcode or '(null)',
            )
            is_added = self.db.add_new_records(record, pk_key=self.pk_key)
            logger.info(f"New Customer Saved successfully; ID:{customer_id}")
        else:
            # Verify all the fields are matching
            logger.info(f"Customer already present, Customer ID: {customer_id}")
        return customer_id

    def search_by_id(self, pk_val, pk_key=None):
        record = BaseModel.search_by_id(pk_key=self.pk_key, pk_val=pk_val)
        if record:
            return record[0]
