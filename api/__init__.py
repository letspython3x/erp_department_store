from flask import Blueprint

bp_client = Blueprint("client_view", __name__)
bp_product = Blueprint("product_view", __name__)
bp_order = Blueprint("order_view", __name__)
bp_store = Blueprint("store_view", __name__)
bp_trader = Blueprint("trader_view", __name__)
bp_report = Blueprint("report_view", __name__)
bp_category = Blueprint("category_view", __name__)

from forms.validate_forms import ValidateProduct, ValidateOrder, ValidateUser, ValidateStore, ValidateTrader, \
    ValidateCategory, ValidateAccount
from api.blueprints import client, product, order, store, trader, report, category
