from flask import Flask
from app.routes import user_routes
from app.routes import product_routes
from app.routes import cart_routes
from app.routes import order_routes
from app.routes import checkout_routes

app = Flask(__name__)

# Register routes
app.register_blueprint(user_routes, url_prefix='/api')
app.register_blueprint(product_routes, url_prefix='/api')
app.register_blueprint(cart_routes, url_prefix='/api')
app.register_blueprint(order_routes, url_prefix='/api')
app.register_blueprint(checkout_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
