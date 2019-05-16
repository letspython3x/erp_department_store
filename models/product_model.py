from datetime import datetime
from decimal import Decimal
from werkzeug.utils import cached_property

from models.base_model import BaseModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class ProductModel(BaseModel):
    def __init__(self, product=None):
        super(ProductModel, self).__init__(table_name='Product')
        logger.info("Initializing Product...")
        self.table_name = 'Product'
        self.pk_key = 'product_id'
        if product:
            logger.info("Initiating Product config...")
            self.product_name = product.get('name')
            self.serial_no = product.get('serial_no')
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

    def search_by_serial_no(self, serial_no=None):
        if serial_no or self.serial_no:
            query = {
                'serial_no': serial_no or serial_no
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
                serial_no=self.serial_no,
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

    # def fetch_all(self):
    #     records = self.db.scan_table(self.pk_key)
    #     return records
    def search_by_id(self, pk_val, pk_key=None):
        record = BaseModel.search_by_id(pk_val=pk_val, pk_key=self.pk_key)
        if record:
            return record[0]
