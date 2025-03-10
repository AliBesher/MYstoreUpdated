from flask import Blueprint, request, jsonify
from app.services import ProductService

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    # Check for required fields
    required_fields = ['name', 'description', 'price', 'dimensions', 'stock_quantity',
                       'category_id', 'image_url', 'furniture_type']

    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"⚠️ Missing required field: {field}"}), 400

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    dimensions = data.get('dimensions')
    stock_quantity = data.get('stock_quantity')
    category_id = data.get('category_id')
    image_url = data.get('image_url')
    furniture_type = data.get('furniture_type')

    # Validate price and stock quantity
    if price <= 0:
        return jsonify({"message": "⚠️ Price must be greater than 0"}), 400

    if stock_quantity < 0:
        return jsonify({"message": "⚠️ Stock quantity must be greater than or equal to 0"}), 400

    # Get additional attributes based on furniture type
    additional_attrs = {}

    if furniture_type == "Chair":
        additional_attrs = {
            'max_weight_capacity': data.get('max_weight_capacity', 100),
            'has_armrests': data.get('has_armrests', True),
            'is_adjustable': data.get('is_adjustable', False)
        }
    elif furniture_type == "Table":
        additional_attrs = {
            'shape': data.get('shape', "Rectangle"),
            'max_weight_capacity': data.get('max_weight_capacity', 200),
            'is_extendable': data.get('is_extendable', False)
        }
    elif furniture_type == "Sofa":
        additional_attrs = {
            'seats': data.get('seats', 3),
            'is_convertible': data.get('is_convertible', False),
            'has_storage': data.get('has_storage', False)
        }
    elif furniture_type == "Bed":
        additional_attrs = {
            'bed_size': data.get('bed_size', "Queen"),
            'has_storage': data.get('has_storage', False),
            'material_type': data.get('material_type', "Wood")
        }
    elif furniture_type == "Cabinet":
        additional_attrs = {
            'num_drawers': data.get('num_drawers', 0),
            'num_shelves': data.get('num_shelves', 0),
            'has_lock': data.get('has_lock', False)
        }

    result = ProductService.add_product(
        name, description, price, dimensions, stock_quantity,
        category_id, image_url, furniture_type, **additional_attrs
    )

    # Check for errors
    if result and "⚠️" in result:
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 201

@product_routes.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()

    # Check if product exists
    product = ProductService.get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "⚠️ Product not found."}), 404

    # Extract and validate data
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    dimensions = data.get('dimensions')
    stock_quantity = data.get('stock_quantity')
    category_id = data.get('category_id')
    image_url = data.get('image_url')
    furniture_type = data.get('furniture_type')

    # Validate price and stock quantity
    if price <= 0:
        return jsonify({"message": "⚠️ Price must be greater than 0"}), 400

    if stock_quantity < 0:
        return jsonify({"message": "⚠️ Stock quantity must be greater than or equal to 0"}), 400

    # Get additional attributes based on furniture type
    additional_attrs = {}

    if furniture_type == "Chair":
        additional_attrs = {
            'max_weight_capacity': data.get('max_weight_capacity', 100),
            'has_armrests': data.get('has_armrests', True),
            'is_adjustable': data.get('is_adjustable', False)
        }
    elif furniture_type == "Table":
        additional_attrs = {
            'shape': data.get('shape', "Rectangle"),
            'max_weight_capacity': data.get('max_weight_capacity', 200),
            'is_extendable': data.get('is_extendable', False)
        }
    elif furniture_type == "Sofa":
        additional_attrs = {
            'seats': data.get('seats', 3),
            'is_convertible': data.get('is_convertible', False),
            'has_storage': data.get('has_storage', False)
        }
    elif furniture_type == "Bed":
        additional_attrs = {
            'bed_size': data.get('bed_size', "Queen"),
            'has_storage': data.get('has_storage', False),
            'material_type': data.get('material_type', "Wood")
        }
    elif furniture_type == "Cabinet":
        additional_attrs = {
            'num_drawers': data.get('num_drawers', 0),
            'num_shelves': data.get('num_shelves', 0),
            'has_lock': data.get('has_lock', False)
        }

    result = ProductService.update_product(
        product_id, name, description, price, dimensions, stock_quantity,
        category_id, image_url, furniture_type, **additional_attrs
    )

    # Check for errors
    if result and "⚠️" in result:
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 200

@product_routes.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Check if product exists
    product = ProductService.get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "⚠️ Product not found."}), 404

    result = ProductService.delete_product(product_id)

    # Check for errors
    if result and "⚠️" in result:
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 200

@product_routes.route('/products', methods=['GET'])
def get_products():
    # Check if category filter is provided
    category_id = request.args.get('category_id')
    furniture_type = request.args.get('furniture_type')
    search_term = request.args.get('search')

    if category_id:
        products = ProductService.get_products_by_category(category_id)
    elif furniture_type:
        products = ProductService.get_products_by_furniture_type(furniture_type)
    elif search_term:
        products = ProductService.search_products(search_term)
    else:
        products = ProductService.get_all_products()

    return jsonify({"products": products}), 200

@product_routes.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)

    if not product:
        return jsonify({"message": "⚠️ Product not found."}), 404

    return jsonify({"product": product.to_dict()}), 200
