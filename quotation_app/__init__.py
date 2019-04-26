from flask import Blueprint

bp_user = Blueprint("user_view", __name__)
bp_product = Blueprint("product_view", __name__)
bp_quotation = Blueprint("quotation_view", __name__)

from forms.validate_forms import ValidateCustomer, ValidateProduct, ValidateQuotation, ValidateUser
from quotation_app.blueprints import user, product, quotation
