from datetime import datetime
from decimal import Decimal
from models.enums import ModelNameEnum
from boto3.dynamodb.conditions import Key, Attr

from models.retail_model import RetailModel
from models.store_model import StoreModel
from models.client_model import ClientModel
from models.product_model import ProductModel

from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class OrderModel(RetailModel):
    def __init__(self):
        super(OrderModel, self).__init__()
        logger.info("Initializing Order...")
        self.table = ModelNameEnum.ORDER.value

    def generate_new_order_id(self):
        """
        get the number of pk that starts with "orders"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        print(_id)
        return _id

    def search_by_order_id(self, order_id):
        val = f"{'orders'}#{order_id}"
        logger.info(f"Search order by ORDER ID: {order_id}...")
        order = self.get_by_partition_key(val)
        order = self.reformat(order)
        return order

    @staticmethod
    def reformat(order):
        logger.info(">>> Reformatting the output")
        metadata = order[0]
        store_id = metadata.get('store_id')
        client_id = metadata.get('client_id')
        store = StoreModel().search_by_store_id(store_id)[0]
        client = ClientModel().search_by_client_id(client_id)[0]

        new_order = dict(
            metadata=order[0],
            store=store,
            client=client,
            line_items=order[1:])

        return new_order

    def search_by_client_id(self, client_id):
        logger.info(f"Search all order by Client ID: {client_id}...")
        ke = Key('sk').eq('ORDER')
        fe = Attr('client_id').eq(client_id)
        pe = 'client_id, order_id, employee_id, store_id, order_type, payment_type, order_total, created_at'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        print(data)
        return data

    def search_by_employee_id(self, employee_id):
        logger.info(f"Search all order by Employee ID: {employee_id}...")
        ke = Key('sk').eq('ORDER')
        fe = Attr('employee_id').eq(employee_id)
        pe = 'client_id, order_id, employee_id, store_id, order_type, payment_type, order_total, created_at'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        return data

    def search_by_store_id(self, store_id):
        logger.info(f"Search all order by Store ID: {store_id}...")
        ke = Key('sk').eq('ORDER')
        fe = Attr('store_id').eq(store_id)
        pe = 'client_id, order_id, employee_id, store_id, order_type, payment_type, order_total, created_at'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        return data

    def search_between_dates(self, start_date, end_date):
        logger.info(f"Search all order between dates {start_date} & {end_date}...")
        ke = Key('sk').eq('ORDER')
        e = Attr('created_at').between(start_date, end_date)
        pe = 'client_id, order_id, employee_id, store_id, order_type, payment_type, order_total, created_at'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        return data

    def insert(self, order):
        """
        1. save order metadata
        2. save line_items

        If invoice: then just save it directly no changes to accounts or products
        If bill:
            Update (subtract) each products units_in_stock
            Update (accounts) if payment_type - Credit then ADD Receivables
            Update (accounts) if payment_type - Cash then ADD Income
        :param order:
        :return: order_id or order_id
        """
        order_type = order.get('order_type')
        logger.info("Saving Order TYPE: %s" % order_type)
        order_id = self.save_order_metadata(order)
        self.save_line_items(order_id, order)

        if order_type == 'Invoice':
            logger.info("Update Products Quantity & Accounts as its a BILL")
            self.update_products_quantity(order)
            self.update_accounts(order)
        return order_id

    def save_order_metadata(self, order):
        client_id = order.get('client_id')
        employee_id = order.get('employee_id', 1)
        order_type = order.get('order_type')
        payment_type = order.get('payment_type')
        discount_on_total = order.get('discount_on_total')
        total_tax = order.get('total_tax')
        discounted_sub_total = order.get('discounted_sub_total')
        order_total = order.get('order_total')
        store_id = order.get('store_id')
        order_date = datetime.utcnow().isoformat()
        order_id = self.generate_new_order_id()
        item = {
            "pk": f"{'orders'}#{order_id}",
            "sk": f"ORDER",
            "data": f"{order_date}#{employee_id}#{client_id}",
            "order_id": order_id,
            "client_id": client_id,
            "employee_id": employee_id,
            "store_id": store_id,
            "order_type": order_type,
            "payment_type": payment_type,
            "discount_on_total": Decimal(str(discount_on_total)),
            "discounted_sub_total": Decimal(str(discounted_sub_total)),
            "total_tax": Decimal(str(total_tax)),
            "order_total": Decimal(str(order_total)),
            "created_at": order_date,
        }
        self.save(item)
        logger.info("Order Metadata saved")
        return order_id

    def save_line_items(self, order_id, order):
        line_items = order.get('item_rows', [])  # POP line items so they are not added to the ORDER
        for line_item in line_items:
            print("Line Item: ", line_item)
            barcode_number = line_item.get('barcode_number', -999)
            product_name = line_item.get('product_name')
            category = line_item.get('category_name')
            quantity = line_item.get('quantity')
            quoted_price = Decimal(str(line_item.get('quoted_price')))
            item_discount = Decimal(str(line_item.get('item_discount')))
            tax = Decimal(str(line_item.get('tax')))
            line_item_total = Decimal(str(line_item.get('line_item_total')))
            item = {
                "pk": f"{'orders'}#{order_id}",
                "sk": f"{'product_name'}#{product_name}",
                "data": f"{line_item_total}#{quantity}#{tax}#{item_discount}",
                "barcode_number": barcode_number,
                "product_name": product_name,
                "category_name": category,
                "quoted_price": quoted_price,
                "quantity": quantity,
                "tax": tax,
                "item_discount": item_discount,
                "line_item_total": line_item_total,
            }
            # item.update(line_item)
            self.save(item)
        logger.info("Line items saved")

    @staticmethod
    def update_products_quantity(order):
        pm = ProductModel()
        line_items = order.get('item_rows', [])
        for line_item in line_items:
            barcode_number = line_item.get('barcode_number', -999)
            product_name = line_item.get('product_name')
            product = pm.search_by_barcode(barcode_number) or pm.search_by_name(product_name)
            product_id = product.get('product_id')
            quantity = line_item.get('quantity')
            ProductModel().update_quantity_in_stocks(product_id, quantity, increase=False)
        logger.info("Product quantities are updated")

    @staticmethod
    def update_accounts(order):
        pass
