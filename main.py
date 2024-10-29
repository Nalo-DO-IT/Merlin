from flask import Flask
from endpoint import sort_products_endpoint

app = Flask(__name__)
app.register_blueprint(sort_products_endpoint)

if __name__ == '__main__':
    app.run(debug=True)