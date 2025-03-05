from flask import Blueprint, request, jsonify
from app.services.cart_service import CartService, PercentageDiscount, BuyOneGetOneDiscount, BulkDiscount

cart_routes = Blueprint('cart_routes', __name__)

# View cart
@cart_routes.route('/cart', methods=['GET'])
def view_cart():
    user_id = request.args.get('user_id')  # Get user_id from query parameter
    cart_items = CartService.get_cart_items(user_id)

    if not cart_items:
        return jsonify({"message": "⚠️ No items in the cart."}), 404

    # Calculate cart total
    cart_total = CartService.calculate_cart_total(user_id)

    return jsonify({
        "cart_items": cart_items,
        "cart_total": cart_total
    }), 200

# Add to cart
@cart_routes.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)  # Default to 1 if not specified

    result = CartService.add_to_cart(user_id, product_id, quantity)
    return jsonify({"message": result}), 201

# Update cart item quantity
@cart_routes.route('/cart/<int:product_id>', methods=['PUT'])
def update_cart(product_id):
    data = request.get_json()
    user_id = data.get('user_id')
    new_quantity = data.get('quantity')

    result = CartService.update_cart(user_id, product_id, new_quantity)
    return jsonify({"message": result}), 200

# Remove from cart
@cart_routes.route('/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    data = request.get_json()
    user_id = data.get('user_id')

    result = CartService.remove_from_cart(user_id, product_id)
    return jsonify({"message": result}), 200

# Clear cart
@cart_routes.route('/cart/clear', methods=['POST'])
def clear_cart():
    data = request.get_json()
    user_id = data.get('user_id')

    result = CartService.clear_cart(user_id)
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
