from flask import Flask
from flask_cors import CORS, cross_origin

from quotation_app import bp_product, bp_user, bp_quotation

app = Flask(__name__)
app.config.from_object('settings')

app.register_blueprint(bp_quotation, url_prefix="/quotation")
app.register_blueprint(bp_product, url_prefix="/product")
app.register_blueprint(bp_user, url_prefix="/user")

CORS(app)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)