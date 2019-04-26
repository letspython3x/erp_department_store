from datetime import datetime, date
from decimal import Decimal

from werkzeug.utils import cached_property

from models.db import DbOperations
from utils.generic_utils import get_logger
from datetime import datetime

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class BaseModel(object):
    """
    Base Class for all models to provide common operations
    """

    def __init__(self, table_name):
        logger.info("Initializing Base Model...")
        self.db = DbOperations(table_name)
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

    def search_by_id(self, pk_key, pk_val):
        logger.info(f"Query: Searching by ID...")
        query = {
            pk_key: pk_val
        }
        # return 0 because it returns a list
        record = self.db.search_by_key(query)
        if record:
            logger.info(f"Query: {query} \n Record Found: {record}")
            return record[0]
        else:
            logger.info(f"Query: {query} \n Record Does Not Exist")


class QuotationModel(BaseModel):
    def __init__(self, quotation=None):
        super(QuotationModel, self).__init__(table_name='Quotation')
        logger.info("Initializing Quotation...")
        # self.quotation_products, self.quotation_total = self.parse(quotation) if quotation else ('', '')
        self.quotation = quotation
        self.table_name = 'Quotation'
        self.pk_key = 'quotation_id'
        self.create_at = str(datetime.now())

    @cached_property
    def quotation_id(self):
        """

        :return: The Last Quotation Saved in DB, to generate a new Quotation ID
        """
        last_id = self.get_last_quotation_id()
        new_id = last_id + 1 if last_id else 1
        return new_id

    def get_last_quotation_id(self):
        last_id = int(self.last_record[self.pk_key])
        if isinstance(last_id, int):
            return last_id
        else:
            return 0

    def generate_new_quotation_id(self):
        return self.quotation_id

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

    @staticmethod
    def fetch_customer_details(quotation):
        c = dict(customer_phone=quotation.get("customer_phone"),
                 customer_email=quotation.get("customer_email"),
                 customer_name=quotation.get("customer_name"))
        return c

    def fetch_quotation_metadata(self, quotation):
        md = dict(store_id=quotation.get("store_id"),
                  user_id=quotation.get("user_id"),
                  total=quotation.get("total"),
                  created_at=TIMESTAMP().strftime("%d-%m-%Y %H:%M:%S")
                  )
        customer = self.fetch_customer_details(quotation)
        md.update(customer)
        return md

    @staticmethod
    def fetch_quoted_products(quotation):
        products = quotation.get("products")
        qp = []  # quoted products

        for product in products:
            if product is not None:
                temp = dict(
                    name=product.get("name"),
                    category=product.get("category"),
                    quoted_price=Decimal(str(product.get("quoted_price"))),
                    quantity=Decimal(product.get("quantity")),
                    sub_total=Decimal(product.get("sub_total"))
                )
                qp.append(temp)
        return qp

    def create(self):
        """
        save the quotation details after fetching customer details and
        products list details, with a new dynamically generated quotation_id.
        :return: None
        """
        new_quotation_id = self.generate_new_quotation_id()
        md = self.fetch_quotation_metadata(self.quotation)
        products = self.fetch_quoted_products(self.quotation)

        record = dict(quotation_id=new_quotation_id)
        record.update(dict(products=products))
        record.update(md)
        is_added = self.db.add_new_records(record, pk_key=self.pk_key)
        return is_added

    # def create(self, customer_id):
    #     """
    #     saves the customer if it does not exist, after incrementing the last customer's id
    #     :return: None
    #     """
    #     print(f"Customer ID to be attached: {customer_id}")
    #     customer = CustomerModel().search_by_id(pk_key='customer_id', pk_val=customer_id)
    #     print(f"Customer: {customer}")
    #     if customer_id and self.quotation_id:
    #         record = dict(
    #             customer_id=customer_id,
    #             quotation_id=self.quotation_id,
    #             quotation_total=Decimal(str(self.quotation_total)),
    #             customer_name=f"{customer.get('first_name')} {customer.get('last_name')}",
    #             customer_phone=customer.get('phone'),
    #             customer_email=customer.get('email'),
    #             create_time=str(date.today()),
    #             quotation_items=self.quotation_products,
    #         )
    #         self.db.add_new_records(record, pk_key=self.pk_key)

    @staticmethod
    def products_form_to_dict(product_form_set):
        """
        Convert the products form to a Dictionary
        :param products: Product Form Set
        :return: products a list of product dict
        """
        quotation_products = []
        for product in product_form_set:
            print(product)
            if product.get('product_name'):
                temp = dict(
                    product_name=product.get('product_name'),
                    category=product.get('product_category'),
                    quoted_price=Decimal(str(product.get('quoted_price'))),
                    quantity=Decimal(product.get('quantity')),
                    serial_no=product.get('serial_no')
                )
                quotation_products.append(temp)
        return quotation_products

    @staticmethod
    def parse(product_form_set):
        """
        Parse & Save the Quotation Form Set
        :param product_form_set: Product Form Set
        :return: list of dictionary of items
        """
        product_obj = ProductModel()
        quotation_products = product_form_set["products"]
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
                _p = ProductModel(product)
                _p.save()
                product['product_id'] = _p.product_id
            product['sub_total'] = Decimal(str(sub_total))
            product['quoted_price'] = product['price']
            del product['price']
            quotation_total += sub_total
            products_list.append(product)
        return products_list, quotation_total


class ProductModel(BaseModel):
    def __init__(self, product=None):
        super(ProductModel, self).__init__(table_name='Product')
        logger.info("Initializing Product...")
        self.table_name = 'Product'
        self.pk_key = 'product_id'
        if product:
            logger.info("Initiating Product config...")
            self.product_name = product.get('name')
            self.category = product.get('category')
            self.cost_price = product.get('cost_price')
            self.sell_price = product.get('sell_price')
            self.quantity = product.get('quantity')
            self.distributor = product.get('distributor')
            self.description = product.get('description')
            self.is_active = product.get("is_active", 1)
            self.quantity = product.get("quantity", 0)

    @cached_property
    def product_id(self):
        product = self.search_by_name()
        if product:
            product_id = product[0][self.pk_key]
            return product_id

    def search_by_name(self, product_name=None):
        if product_name or self.product_name:
            query = {
                'name': product_name or self.product_name
            }
            record = self.db.search_by_attributes(query)
            return record

    def create(self):
        """
        saves the product if it does not exist, after incrementing the last product's id
        :return: None
        """
        product_id = self.product_id
        if not product_id:
            logger.info(f"Saving the New Product...")
            product_id = int(self.last_record[self.pk_key]) + 1

            logger.info(f"New Product ID: {product_id}")
            print(f"{product_id} {self.product_name} {self.category} {self.cost_price}")
            record = dict(
                product_id=Decimal(str(product_id)),
                name=self.product_name,
                category=self.category,
                description=self.description,
                distributor=self.distributor,
                cost_price=Decimal(str(self.cost_price)),
                sell_price=Decimal(str(self.sell_price)),
                is_active=Decimal(str(int(self.is_active))),
                quantity=self.quantity
            )
            # self.db.save_records(record, pk_key=self.pk_key)
            self.db.add_new_records(record, pk_key='name')
            logger.info(f"New Product Saved Successfully; ID: {product_id}")
        else:
            # Verify all the fields are matching
            logger.info(f"Product already present, Product ID: {self.product_id}")
            logger.info(f"Updating the old Product...")
            self.update(product_id, self.product_name, self.category, self.cost_price, self.sell_price, self.is_active,
                        self.quantity, self.description, self.distributor)
        return product_id

    def update(self, product_id, product_name=None, category=None, cost_price=None, sell_price=None,
               is_active=None, quantity=None, description=None, distributor=None):
        """
        update the corresponding values of the product,
        by saving the old with new values.
        :return: True
        """
        # product = self.search_by_id(pk_key='product_id', pk_val=product_id)
        record = dict(
            product_id=product_id,
            name=product_name,
            category=category,
            description=description,
            distributor=distributor,
            cost_price=Decimal(str(cost_price)),
            sell_price=Decimal(str(sell_price)),
            is_active=is_active,
            quantity=quantity
        )
        is_updated = self.db.update_record(record)
        if is_updated:
            logger.info(f"UPDATE Product SUCCESS: ID: {product_id}")
            return is_updated
        logger.info(f"UPDATE Product FAILURE: ID: {product_id}")

    def update_details(self, product_id, new_data):
        existing_record = self.search_by_id(pk_key='product_id', pk_val=product_id)

        product_name = new_data.get('name') or existing_record.get('name')
        category = new_data.get('category') or existing_record.get('category')
        distributor = new_data.get('distributor') or existing_record.get('distributor')
        description = new_data.get('description') or existing_record.get('description')
        cost_price = new_data.get('cost_price') or existing_record.get('cost_price')
        sell_price = new_data.get('sell_price') or existing_record.get('sell_price')
        is_active = new_data.get('is_active') or existing_record.get('is_active')
        quantity = new_data.get('quantity') or existing_record.get('quantity')

        self.update(product_id, product_name, category, cost_price, sell_price, is_active, quantity, description,
                    distributor)

    def deactivate(self, product):
        """
        Delete will only mark a product as in active,
        by putting is_active=0
        :param id:
        :return:
        """
        # self.db.delete(self.pk_key, int(id))
        return self.switch_active_flag(product, is_active=0)

    def activate(self, product):
        return self.switch_active_flag(product, is_active=1)

    def switch_active_flag(self, product, is_active):
        product_id = product.get('product_id')
        product_name = product.get('name')
        category = product.get('category')
        cost_price = product.get('cost_price')
        sell_price = product.get('sell_price')
        quantity = product.get('quantity')
        distributor = product.get('distributor')
        description = product.get('description')
        is_active = is_active
        print(f"{product_id}, {product_name}, {category}, {cost_price}, {is_active}, {quantity}, {distributor}")
        is_updated = self.update(product_id, product_name, category, cost_price, sell_price, is_active, quantity,
                                 description, distributor)

        return is_updated

    def fetch_all_products(self):
        records = self.db.scan_table(self.pk_key)
        return records


class CustomerModel(BaseModel):
    def __init__(self, customer=None):
        logger.info("Initializing Customer...")
        super(CustomerModel, self).__init__(table_name='Customer')
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
            self.db.add_new_records(record, pk_key=self.pk_key)
            logger.info(f"New Customer Saved successfully; ID:{customer_id}")
        else:
            # Verify all the fields are matching
            logger.info(f"Customer already present, Customer ID: {customer_id}")
        return customer_id
