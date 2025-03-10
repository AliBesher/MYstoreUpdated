from flask import Blueprint, request, jsonify
from app.services import UserService

user_routes = Blueprint('user_routes', __name__)

# Add a new user
@user_routes.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    # Check for required fields
    if not data:
        return jsonify({"message": "⚠️ No data provided"}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', "customer")  # Default to "customer"

    # Validate required fields
    if not name or not email or not password:
        return jsonify({"message": "⚠️ Name, email, and password are required"}), 400

    # Validate email format (basic check)
    if '@' not in email:
        return jsonify({"message": "⚠️ Invalid email format"}), 400

    # Validate password length
    if len(password) < 6:
        return jsonify({"message": "⚠️ Password must be at least 6 characters long"}), 400

    result = UserService.add_user(name, email, password, role)

    # Check if there was an error (indicated by ⚠️)
    if result and "⚠️" in result:
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 201

# Update user
@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Check if user exists
    existing_user = UserService.get_user_by_id(user_id)
    if not existing_user:
        return jsonify({"message": "⚠️ User not found"}), 404

    # Check for required fields
    if not data:
        return jsonify({"message": "⚠️ No data provided"}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Validate required fields
    if not name or not email:
        return jsonify({"message": "⚠️ Name and email are required"}), 400

    # Validate email format (basic check)
    if '@' not in email:
        return jsonify({"message": "⚠️ Invalid email format"}), 400

    # Validate password length if provided
    if password and len(password) < 6:
        return jsonify({"message": "⚠️ Password must be at least 6 characters long"}), 400

    result = UserService.update_user(user_id, name, email, password, role)

    # Check if there was an error
    if result and "⚠️" in result:
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 200

# Delete user
@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Check if user exists
    existing_user = UserService.get_user_by_id(user_id)
    if not existing_user:
        return jsonify({"message": "⚠️ User not found"}), 404

    result = UserService.delete_user(user_id)

    # Check if there was an error
    if result and "⚠️" in result:
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 200

# Get all users
@user_routes.route('/users', methods=['GET'])
def get_users():
    users = UserService.get_users()

    if not users:
        return jsonify({"users": []}), 200  # Return empty array instead of 404

    return jsonify({"users": users}), 200

# Get user by ID
@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = UserService.get_user_by_id(user_id)

    if not user:
        return jsonify({"message": "⚠️ User not found."}), 404

    return jsonify({"user": user}), 200

# User login
@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Check for required fields
    if not data:
        return jsonify({"message": "⚠️ No data provided"}), 400

    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if not email or not password:
        return jsonify({"message": "⚠️ Email and password are required"}), 400

    auth_result = UserService.authenticate_user(email, password)

    if auth_result:
        return jsonify(auth_result), 200

    return jsonify({"message": "⚠️ Invalid email or password."}), 401

# Reset user password
@user_routes.route('/users/<int:user_id>/reset-password', methods=['POST'])
def reset_password(user_id):
    data = request.get_json()

    # Check if user exists
    existing_user = UserService.get_user_by_id(user_id)
    if not existing_user:
        return jsonify({"message": "⚠️ User not found"}), 404

    # Check for required fields
    if not data or 'new_password' not in data:
        return jsonify({"message": "⚠️ New password is required"}), 400

    new_password = data.get('new_password')

    # Validate password length
    if len(new_password) < 6:
        return jsonify({"message": "⚠️ Password must be at least 6 characters long"}), 400

    result = UserService.reset_user_password(user_id, new_password)

    # Check if there was an error
    if result and "⚠️" in result:
        return jsonify({"message": result}), 400

    return jsonify({"message": result}), 200
