from app.models import User
from app.db import execute_query

class UserService:
    @staticmethod
    def add_user(name, email, password, role="customer"):
        """
        Add a new user.
        """
        # Check if email already exists
        existing_user = User.get_user_by_email(email)
        
        if existing_user:
            return "⚠️ Email already in use."

        # Create and add user
        user = User(name, email, password, role)
        user.add_user()
        return f"User '{name}' added successfully."

    @staticmethod
    def update_user(user_id, name, email, password, role):
        """
        Update user information.
        """
        # Check if email is used by another user
        existing_user = User.get_user_by_email(email)
        
        if existing_user and existing_user['UserID'] != user_id:
            return "⚠️ Email already in use by another user."

        # Create and update user
        user = User(name, email, password, role)
        user.update_user(user_id)
        return f"User '{name}' updated successfully."

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user.
        """
        user = User("", "", "", "")  # Empty user object
        user.delete_user(user_id)
        return "User deleted successfully."

    @staticmethod
    def get_users():
        """
        Get all users.
        """
        query = "SELECT UserID, Name, Email, Role, CreatedAt FROM Users"
        return execute_query(query, fetch=True)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID.
        """
        return User.get_user_by_id(user_id)
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate a user by email and password.
        """
        user = User.authenticate(email, password)
        
        if user:
            # Generate authentication token
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
            
        return None
