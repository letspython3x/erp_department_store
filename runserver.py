from flask import Flask

from api import bp_product, bp_customer, bp_quotation, bp_store, bp_trader

app = Flask(__name__)
app.config.from_object('settings')

app.register_blueprint(bp_quotation, url_prefix="/quotation")
app.register_blueprint(bp_product, url_prefix="/product")
app.register_blueprint(bp_customer, url_prefix="/customer")
app.register_blueprint(bp_store, url_prefix="/store")
app.register_blueprint(bp_trader, url_prefix="/trader")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
