from flask import Flask

from auth_app import bp_user
from quotation_app import bp_product, bp_customer, bp_quotation

app = Flask(__name__)
app.register_blueprint(bp_customer, url_prefix="/customer")
app.register_blueprint(bp_quotation, url_prefix="/quotation")
app.register_blueprint(bp_product, url_prefix="/product")
app.register_blueprint(bp_user, url_prefix="/user")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
