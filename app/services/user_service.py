from app.models import User
from app.db import execute_query
import hashlib
import re

class UserService:
    @staticmethod
    def add_user(name, email, password, role="customer"):
        """
        Add a new user.
        """
        # Validate inputs
        if not name or not email or not password:
            return "⚠️ Name, email, and password are required."

        # Validate email format with regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return "⚠️ Invalid email format."

        # Validate password length
        if len(password) < 6:
            return "⚠️ Password must be at least 6 characters long."

        # Validate role
        valid_roles = ["admin", "customer", "manager"]
        if role not in valid_roles:
            return f"⚠️ Invalid role. Must be one of: {', '.join(valid_roles)}"

        # Check if email already exists
        existing_user = User.get_user_by_email(email)
        if existing_user:
            return "⚠️ Email already in use."

        try:
            # Create and add user
            user = User(name, email, password, role)
            user.add_user()
            return f"User '{name}' added successfully."
        except Exception as e:
            return f"⚠️ Error adding user: {str(e)}"

    @staticmethod
    def update_user(user_id, name, email, password, role):
        """
        Update user information.
        """
        # Validate inputs
        if not name or not email:
            return "⚠️ Name and email are required."

        # Validate email format with regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return "⚠️ Invalid email format."

        # Validate password length if provided
        if password and len(password) < 6:
            return "⚠️ Password must be at least 6 characters long."

        # Validate role if provided
        if role:
            valid_roles = ["admin", "customer", "manager"]
            if role not in valid_roles:
                return f"⚠️ Invalid role. Must be one of: {', '.join(valid_roles)}"

        # Check if user exists
        user = User.get_user_by_id(user_id)
        if not user:
            return "⚠️ User not found."

        # Check if email is used by another user
        existing_user = User.get_user_by_email(email)
        if existing_user and existing_user['UserID'] != user_id:
            return "⚠️ Email already in use by another user."

        try:
            # Create and update user
            user_obj = User(name, email, password, role)
            user_obj.update_user(user_id)
            return f"User '{name}' updated successfully."
        except Exception as e:
            return f"⚠️ Error updating user: {str(e)}"

    @staticmethod
    def reset_user_password(user_id, new_password):
        """
        Reset user password.
        """
        # Validate password
        if not new_password or len(new_password) < 6:
            return "⚠️ Password must be at least 6 characters long."

        # Check if user exists
        user = User.get_user_by_id(user_id)
        if not user:
            return "⚠️ User not found."

        try:
            # Reset password
            success = User.reset_password(user_id, new_password)
            if success:
                return "✅ Password reset successfully."
            else:
                return "⚠️ Failed to reset password."
        except Exception as e:
            return f"⚠️ Error resetting password: {str(e)}"

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user.
        """
        # Check if user exists
        user = User.get_user_by_id(user_id)
        if not user:
            return "⚠️ User not found."

        try:
            user_obj = User("", "", "", "")  # Empty user object
            user_obj.delete_user(user_id)
            return "User deleted successfully."
        except Exception as e:
            return f"⚠️ Error deleting user: {str(e)}"

    @staticmethod
    def get_users():
        """
        Get all users.
        """
        try:
            query = "SELECT UserID, Name, Email, Role, CreatedAt FROM Users"
            result = execute_query(query, fetch=True)
            return result if result else []
        except Exception as e:
            print(f"Error fetching users: {str(e)}")
            return []

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID.
        """
        if not user_id or user_id <= 0:
            return None

        try:
            return User.get_user_by_id(user_id)
        except Exception as e:
            print(f"Error fetching user by ID: {str(e)}")
            return None

    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate user and return user info with token.
        """
        if not email or not password:
            return None

        try:
            print(f"Attempting login: {email}")

            user = User.get_user_by_email(email)

            if not user:
                print("User not found")
                return None

            salted_password = password.encode('utf-8') + user['Salt'].encode('utf-8')
            calculated_hash = hashlib.sha256(salted_password).hexdigest()

            print(f"Input Password: {password}")
            print(f"Salt: {user['Salt']}")
            print(f"Calculated Hash: {calculated_hash}")
            print(f"Stored Password: {user['Password']}")

            if User.verify_password(password, user['Password'], user['Salt']):
                token = User.generate_auth_token(user['UserID'])

                return {
                    "user": {
                        "id": user['UserID'],
                        "name": user['Name'],
                        "email": user['Email'],
                        "role": user['Role']
                    },
                    "token": token
                }
            print("Password verification failed")
            return None
        except Exception as e:
            print(f"Error during authentication: {str(e)}")
            return None
