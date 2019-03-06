from datetime import datetime, date
from decimal import Decimal

from db import DbOperations
from werkzeug.utils import cached_property

from erp_department_store.utils.generic_utils import get_logger

logger = get_logger(__name__)


class BaseModel(object):
    """
    Base Class for all models to provide common operations
    """

    def __init__(self, table_name):
        logger.info("Initializing Base Model...")
        self.db = DbOperations(table_name)
        self.pk_key = None
        self.table = self.db.table

    @cached_property
    def last_record(self):
        """
        last_record will fetch the last entry on the basis of descending order sorted, Primary Key
        """
        logger.info(f"Fetching Last Record...")
        record = self.db.get_table_last_record(self.pk_key)
        # Dictionary Type data is returned
        return record

    def search_by_id(self, pk_key, pk_value):
        query = {
            pk_key: pk_value
        }
        # return 0 because it returns a list
        record = self.db.search_by_key(query)[0]
        if record:
            logger.info(f"Query: {query} \n Record Found: {record}")
        else:
            logger.info(f"Query: {query} \n Record Does Not Exist")
        return record


class Quotation(BaseModel):
    def __init__(self, quotation_set=None):
        super(Quotation, self).__init__(table_name='Quotation')
        logger.info("Initializing Quotation...")
        self.quotation_products, self.quotation_total = self.parse(quotation_set)
        self.table_name = 'Quotation'
        self.pk_key = 'quotation_id'
        self.create_time = str(datetime.now())


    @cached_property
    def quotation_id(self):
        """

        :return: The Last Quotation Saved in DB, to generate a new Quotation ID
        """
        id = 1
        if self.last_record:
            print(f"LAST RECORD Found: {self.last_record}")
            id = int(self.last_record[self.pk_key]) + 1
        return id

    def search_by_email(self, customer_email):
        logger.info(f"Searching Quotation via Customer Email {customer_email}...")
        query = {
            'customer_email': customer_email
        }
        record = self.db.search_by_attributes(query)
        return record

    def search_by_phone(self, customer_phone):
        logger.info(f"Searching Quotation via Customer Phone {customer_phone}...")
        query = {
            'customer_email': customer_phone
        }
        record = self.db.search_by_attributes(query)
        return record

    def save(self, customer_id):
        """
        saves the customer if it does not exist, after incrementing the last customer's id
        :return: None
        """
        print(f"Customer ID to be attached: {customer_id}")
        customer = Customer().search_by_id(pk_key='customer_id', pk_value=customer_id)
        print(f"Customer: {customer}")
        if customer_id and self.quotation_id:
            record = dict(
                customer_id=customer_id,
                quotation_id=self.quotation_id,
                quotation_total=Decimal(str(self.quotation_total)),
                customer_name=f"{customer.get('first_name')} {customer.get('last_name')}",
                customer_phone=customer.get('phone'),
                customer_email=customer.get('email'),
                create_time=str(date.today()),
                quotation_items=self.quotation_products,
            )
            self.db.save_records(record, pk_key=self.pk_key)

    @staticmethod
    def products_form_to_dict(product_form_set):
        """
        Convert the products form to a Dictionary
        :param products: Product Form Set
        :return: products a list of product dict
        """
        quotation_products = []
        for product in product_form_set:
            if product.cleaned_data.get('product_name'):
                temp = dict(
                    product_name=product.cleaned_data.get('product_name'),
                    category=product.cleaned_data.get('product_category'),
                    quoted_price=Decimal(str(product.cleaned_data.get('quoted_price'))),
                    quantity=Decimal(product.cleaned_data.get('quantity')),
                    serial_no=product.cleaned_data.get('serial_no')
                )
                quotation_products.append(temp)
        return quotation_products

    @staticmethod
    def parse(product_form_set):
        """
        Parse & Save the Quotation Form Set
        :param items: Product Form Set
        :return: list of dictionary of items
        """
        product_obj = Product()
        quotation_products = Quotation.products_form_to_dict(product_form_set)
        products_list = []
        quotation_total = 0
        for product in quotation_products:
            print(product)
            product_name = product.get('product_name')
            quoted_price = product['quoted_price']
            quantity = product['quantity']
            sub_total = float(quoted_price) * int(quantity)
            p = product_obj.search_by_name(product_name)
            if p:
                # If product/item Exist in Product Table
                product['product_id'] = p.product_id
            else:
                # If product/item does not exist then save in Product Table,
                # with the quoted_price value
                product['price'] = product['quoted_price']
                del product['quoted_price']
                _p = Product(product)
                _p.save()
                product['product_id'] = _p.product_id
            product['sub_total'] = Decimal(str(sub_total))
            product['quoted_price'] = product['price']
            del product['price']
            quotation_total += sub_total
            products_list.append(product)
        return products_list, quotation_total


class Product(BaseModel):
    def __init__(self, product=None):
        super(Product, self).__init__(table_name='Product')
        logger.info("Initializing Product...")
        if product:
            print("Initiating Product config...")
            self.name = product.get('product_name')
            self.category = product.get('category')
            self.price = product.get('price')
            self.serial_no = product.get("serial_no") or "-9999"
            # self.validate()

        self.table_name = 'Product'
        self.pk_key = 'product_id'

    def validate(self):
        assert isinstance(self.name, str)
        assert isinstance(self.category, str)
        assert isinstance(self.price, Decimal)
        print(self.serial_no)
        print(type(self.serial_no))
        assert isinstance(self.serial_no, str)

    @cached_property
    def product_id(self):
        product = self.search_by_name()
        if product:
            product_id = product[0][self.pk_key]
            return product_id

    def search_by_name(self, product_name=None):
        if product_name or self.name:
            query = {
                'product_name': product_name or self.name
            }
            record = self.db.search_by_attributes(query)
            return record

    def save(self):
        """
        saves the customer if it does not exist, after incrementing the last customer's id
        :return: None
        """
        product_id = self.product_id
        if not product_id:
            logger.info(f"Saving the New Product...")
            product_id = int(self.last_record[self.pk_key]) + 1
            logger.info(f"New Product ID: {product_id}")
            record = dict(
                product_id=product_id,
                name=self.name,
                category=self.category,
                price=Decimal(str(self.price)),
                serial_no=self.serial_no
            )
            self.db.save_records(record, pk_key=self.pk_key)
            logger.info(f"New Product Saved Successfully; ID: {self.product_id}")
        else:
            # Verify all the fields are matching
            print(f"Product present, Product ID: {self.product_id}")
        return product_id


class Customer(BaseModel):
    def __init__(self, customer=None):
        logger.info("Initializing Customer...")
        super(Customer, self).__init__(table_name='Customer')
        if customer:
            print("Initiating Customer config...")
            self.first_name = customer.get('first_name').lower()
            self.last_name = customer.get('last_name').lower()
            self.phone = str(customer.get('phone')).lower()
            self.email = customer.get('email').lower()
            self.street = customer.get('street').lower()
            self.state = customer.get('state').lower()
            self.country = customer.get('country').lower()
            self.postal_code = customer.get('postal_code').lower()
            self.validate()

        self.table_name = 'Customer'
        self.pk_key = 'customer_id'

    def validate(self):
        assert isinstance(self.first_name, str)
        assert isinstance(self.last_name, str)
        assert isinstance(self.phone, str)
        assert isinstance(self.email, str)
        assert isinstance(self.street, str)
        assert isinstance(self.state, str)
        assert isinstance(self.country, str)
        assert isinstance(self.postal_code, str)

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

    def save(self):
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
                last_name=self.last_name,
                phone=self.phone,
                email=self.email,
                street=self.street or '(null)',
                state=self.state or '(null)',
                country=self.country or '(null)',
                postal_code=self.postal_code or '(null)'
            )
            self.db.save_records(record, pk_key=self.pk_key)
            logger.info(f"New Customer Saved successfully; ID:{customer_id}")
        else:
            # Verify all the fields are matching
            logger.info(f"Customer already present, Customer ID: {customer_id}")
        return customer_id
