from flask import Blueprint, request, jsonify
from app.services import CartService, PercentageDiscount, BuyOneGetOneDiscount, BulkDiscount

cart_routes = Blueprint('cart_routes', __name__)

# View cart contents
@cart_routes.route('/cart', methods=['GET'])
def view_cart():
    user_id = request.args.get('user_id')

    # Check if user_id exists
    if not user_id:
        return jsonify({"message": "⚠️ User ID is required."}), 400

    # Call cart service
    cart_items = CartService.get_cart_items(user_id)

    if not cart_items:
        return jsonify({"message": "⚠️ No items in the cart."}), 404

    # Calculate total amount
    cart_total = CartService.calculate_cart_total(user_id)

    return jsonify({
        "cart_items": cart_items,
        "cart_total": cart_total
    }), 200

# Add item to cart
@cart_routes.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()

    # Validate data
    if not data or 'user_id' not in data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({"message": "⚠️ Invalid data. Missing required fields."}), 400

    # Call cart service
    try:
        result = CartService.add_to_cart(data['user_id'], data['product_id'], data['quantity'])
        return jsonify({"message": result}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

# Update item quantity in cart
@cart_routes.route('/cart/<int:product_id>', methods=['PUT'])
def update_cart(product_id):
    data = request.get_json()

    # Validate data
    if not data or 'user_id' not in data or 'quantity' not in data:
        return jsonify({"message": "⚠️ Invalid data. Missing required fields."}), 400

    # Validate quantity
    if data['quantity'] <= 0:
        return jsonify({"message": "⚠️ Quantity must be positive."}), 400

    # Call cart service
    try:
        result = CartService.update_cart(data['user_id'], product_id, data['quantity'])
        return jsonify({"message": result}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

# Remove item from cart
@cart_routes.route('/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    user_id = request.json.get('user_id')

    # Validate data
    if not user_id:
        return jsonify({"message": "⚠️ Invalid data. Missing user_id."}), 400

    # Call cart service
    try:
        result = CartService.remove_from_cart(user_id, product_id)
        return jsonify({"message": result}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404

# Clear cart
@cart_routes.route('/cart/clear', methods=['POST'])
def clear_cart():
    data = request.get_json()

    # Validate data
    if not data or 'user_id' not in data:
        return jsonify({"message": "⚠️ Invalid data. Missing required fields."}), 400

    # Call cart service
    result = CartService.clear_cart(data['user_id'])
    return jsonify({"message": result}), 200

# Apply discount
@cart_routes.route('/cart/discount', methods=['POST'])
def apply_discount():
    data = request.get_json()
    user_id = data.get('user_id')
    discount_type = data.get('discount_type')

    discount_strategy = None

    if discount_type == 'percentage':
        percentage = data.get('percentage', 10)
        discount_strategy = PercentageDiscount(percentage)
    elif discount_type == 'buy_one_get_one':
        eligible_categories = data.get('eligible_categories', [])
        discount_strategy = BuyOneGetOneDiscount(eligible_categories)
    elif discount_type == 'bulk':
        threshold = data.get('threshold', 5)
        percentage = data.get('percentage', 15)
        discount_strategy = BulkDiscount(threshold, percentage)
    else:
        return jsonify({"message": "⚠️ Invalid discount type."}), 400

    discount_amount = CartService.apply_discount(user_id, discount_strategy)

    return jsonify({
        "message": "Discount applied successfully.",
        "discount_amount": discount_amount
    }), 200
