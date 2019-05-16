from datetime import datetime
from decimal import Decimal

from werkzeug.utils import cached_property

from models.base_model import BaseModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class QuotationModel(BaseModel):
    def __init__(self, quotation=None):
        super(QuotationModel, self).__init__(table_name='Quotation')
        logger.info("Initializing Quotation...")
        # self.quotation_products, self.quotation_total = self.parse(quotation) if quotation else ('', '')
        self.quotation = quotation
        self.table_name = 'Quotation'
        self.pk_key = 'quotation_id'

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
        c = dict(customer_id=quotation.get("customer_id"))
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
        new_quotation_id = self.db.get_total_records_count() + 1  # self.generate_new_quotation_id()
        md = self.fetch_quotation_metadata(self.quotation)
        products = self.fetch_quoted_products(self.quotation)

        record = dict(quotation_id=new_quotation_id)
        record.update(dict(products=products))
        record.update(md)
        is_added = self.db.add_new_records(record, pk_key=self.pk_key)
        return is_added

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

    def search_by_id(self, pk_val, pk_key=None):
        record = BaseModel.search_by_id(pk_val=pk_val, pk_key=self.pk_key)
        if record:
            return record[0]
