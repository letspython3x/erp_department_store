from datetime import datetime
from decimal import Decimal

from boto3.dynamodb.conditions import Key, Attr

from models.retail_model import RetailModel
from utils.generic_utils import get_logger

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class QuotationModel(RetailModel):
    def __init__(self):
        super(QuotationModel, self).__init__()
        logger.info("Initializing Quotation...")
        self.table = 'ORDER'

    def generate_new_order_id(self):
        """
        get the number of pk that starts with "product"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        print(_id)
        return _id

    def search_by_order_id(self, order_id):
        val = f"{'orders'}#{order_id}"
        logger.info(f"Search QUOTATION by ORDER ID: {order_id}...")
        return self.get_by_partition_key(val)

    def search_by_customer_id(self, customer_id):
        logger.info(f"Search all QUOTATION by Customer ID: {customer_id}...")
        ke = Key('sk').eq('ORDER')
        fe = Attr('customer_id').eq(customer_id)
        pe = 'customer_id, order_id, employee_id, quotation_type, payment_type, quotation_total, created_at'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        print(data)
        return data

    def search_by_employee_id(self, employee_id):
        logger.info(f"Search all QUOTATION by Employee ID: {employee_id}...")
        ke = Key('sk').eq('ORDER')
        fe = Attr('employee_id').eq(employee_id)
        pe = 'customer_id, order_id, employee_id, quotation_type, payment_type, quotation_total, created_at'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        return data

    def insert(self, quotation):
        customer_id = quotation.get('customer_id')
        employee_id = quotation.get('employee_id', 1)
        quotation_type = quotation.get('quotation_type')
        payment_type = quotation.get('payment_type')
        discount_on_total = quotation.get('discount_on_total')
        total_tax = quotation.get('total_tax')
        discounted_sub_total = quotation.get('discounted_sub_total')
        quotation_total = quotation.get('quotation_total')
        store_id = quotation.get('store_id')

        line_items = quotation.pop('item_rows', [])  # POP line items so they are not added to the ORDER
        order_date = datetime.utcnow().isoformat()
        order_id = self.generate_new_order_id()
        item = {
            "pk": f"{'orders'}#{order_id}",
            "sk": f"ORDER",
            "data": f"{order_date}#{employee_id}#{customer_id}",
            "order_id": order_id,
            "customer_id": customer_id,
            "employee_id": employee_id,
            "store_id": store_id,
            "quotation_type": quotation_type,
            "payment_type": payment_type,
            "discount_on_total": Decimal(str(discount_on_total)),
            "discounted_sub_total": Decimal(str(discounted_sub_total)),
            "total_tax": Decimal(str(total_tax)),
            "quotation_total": Decimal(str(quotation_total)),
            "created_at": order_date,
        }

        # item.update(quotation)
        # print(item)
        self.save(item)

        for line_item in line_items:
            self.save_line_item(order_id, line_item)
        return order_id

    def save_line_item(self, order_id, line_item):
        print("Line Item: ", line_item)
        quantity = line_item.get('quantity')
        item_discount = Decimal(str(line_item.get('item_discount')))
        tax = Decimal(str(line_item.get('tax')))
        line_item_total = Decimal(str(line_item.get('line_item_total')))
        quoted_price = Decimal(str(line_item.get('quoted_price')))
        category = line_item.get('category_name')
        product_name = line_item.get('product_name')

        # product_id = ProductModel().search_by_name(product_name).get('product_id', -999)

        item = {
            "pk": f"{'orders'}#{order_id}",
            "sk": f"{'product_name'}#{product_name}",
            "data": f"{line_item_total}#{quantity}#{tax}#{item_discount}",
            "product_name": product_name,
            "line_item_total": line_item_total,
            "tax": tax,
            "item_discount": item_discount,
            "quoted_price": quoted_price,
            "category_name": category,
            "quantity": quantity,
        }
        # item.update(line_item)
        self.save(item)
        print(item)
