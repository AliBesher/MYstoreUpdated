from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_routes = Blueprint('user_routes', __name__)

# Add a new user
@user_routes.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', "customer")  # Default to "customer"

    result = UserService.add_user(name, email, password, role)
    return jsonify({"message": result}), 201

# Update user
@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    result = UserService.update_user(user_id, name, email, password, role)
    return jsonify({"message": result}), 200

# Delete user
@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = UserService.delete_user(user_id)
    return jsonify({"message": result}), 200

# Get all users
@user_routes.route('/users', methods=['GET'])
def get_users():
    users = UserService.get_users()
    return jsonify({"users": users}), 200

# Get user by ID
@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify({"user": user}), 200
    return jsonify({"message": "⚠️ User not found."}), 404

# User login
@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    auth_result = UserService.authenticate_user(email, password)
    
    if auth_result:
        return jsonify(auth_result), 200
    
    return jsonify({"message": "⚠️ Invalid email or password."}), 401
