from flask import Flask
from flask_cors import CORS

from api import bp_product, bp_client, bp_order, bp_store, bp_trader, bp_report, bp_category

app = Flask(__name__)
app.config.from_object('settings')

app.register_blueprint(bp_order, url_prefix="/order")
app.register_blueprint(bp_product, url_prefix="/product")
app.register_blueprint(bp_client, url_prefix="/client")
app.register_blueprint(bp_store, url_prefix="/store")
app.register_blueprint(bp_trader, url_prefix="/trader")
app.register_blueprint(bp_report, url_prefix="/report")
app.register_blueprint(bp_category, url_prefix="/category")


CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
