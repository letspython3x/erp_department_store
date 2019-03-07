from flask import Blueprint
from forms.validate_forms import ValidateUserForm

bp_user = Blueprint("user_view", __name__)
