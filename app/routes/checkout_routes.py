from flask import Blueprint, request, jsonify
from app.services import CheckoutService

checkout_routes = Blueprint('checkout_routes', __name__)

# Process checkout
@checkout_routes.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    user_id = data.get('user_id')

    # Initialize checkout service
    checkout_service = CheckoutService()
    
    # Process checkout
    result = checkout_service.checkout(user_id)
    if "⚠️" in result:  # If there's an error
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 200

# Process payment
@checkout_routes.route('/checkout/payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    order_id = data.get('order_id')
    payment_method = data.get('payment_method')
    payment_details = data.get('payment_details', {})

    # Initialize checkout service
    checkout_service = CheckoutService()
    
    # Process payment
    result = checkout_service.process_payment(order_id, payment_method, payment_details)
    if "⚠️" in result:  # If there's an error
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 200
