from flask import Flask

from flask_blueprints.customer import bp_customer
from flask_blueprints.product import bp_product
from flask_blueprints.quotation import bp_quotation
from flask_blueprints.user import bp_user

app = Flask(__name__)
app.register_blueprint(bp_customer, url_prefix="/customer")
app.register_blueprint(bp_quotation, url_prefix="/quotation")
app.register_blueprint(bp_product, url_prefix="/product")
app.register_blueprint(bp_user, url_prefix="/user")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
