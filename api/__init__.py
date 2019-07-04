from flask import Blueprint

bp_customer = Blueprint("customer_view", __name__)
bp_product = Blueprint("product_view", __name__)
bp_quotation = Blueprint("quotation_view", __name__)
bp_store = Blueprint("store_view", __name__)
bp_trader = Blueprint("trader_view", __name__)
bp_report = Blueprint("report_view", __name__)

from forms.validate_forms import ValidateCustomer, ValidateProduct, ValidateQuotation, ValidateUser, ValidateStore, ValidateTrader
from api.blueprints import customer, product, quotation, store, trader, report
