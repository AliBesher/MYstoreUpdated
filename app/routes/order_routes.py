from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService

order_routes = Blueprint('order_routes', __name__)

# Create new order
@order_routes.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('user_id')

    result = OrderService.create_order(user_id)
    if "⚠️" in result:  # If there's an error
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 201

# Update order status
@order_routes.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    status = data.get('status')  # New order status (e.g., "processing", "completed")

    result = OrderService.update_order_status(order_id, status)
    return jsonify({"message": result}), 200

# Delete order
@order_routes.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    result = OrderService.delete_order(order_id)
    return jsonify({"message": result}), 200

# Get user's orders
@order_routes.route('/orders', methods=['GET'])
def view_orders():
    user_id = request.args.get('user_id')  # Get user_id from query parameter
    orders = OrderService.get_order_by_user(user_id)

    if not orders:
        return jsonify({"message": "⚠️ No orders found for this user."}), 404

    return jsonify({"orders": orders}), 200

# Get order details
@order_routes.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = OrderService.get_order_by_id(order_id)
    
    if not order:
        return jsonify({"message": "⚠️ Order not found."}), 404
    
    # Get order items
    from app.models.order import Order
    order_items = Order.get_order_items(order_id)
    
    return jsonify({
        "order": order,
        "items": order_items
    }), 200
