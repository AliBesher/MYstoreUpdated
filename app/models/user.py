from app.db.execute_query import execute_query
import hashlib
import os
import uuid


class User:
    """User class with enhanced security features."""
    
    def __init__(self, name, email, password, role="customer"):
        self.name = name
        self.email = email
        self.password = password  # Plain text password (temporary)
        self.role = role
        
    def add_user(self):
        """Add a new user with hashed password."""
        # Generate a random salt
        salt = os.urandom(32).hex()
        
        # Hash the password with the salt
        hashed_password = self._hash_password(self.password, salt)
        
        query = """
        INSERT INTO Users (Name, Email, Password, Salt, Role, CreatedAt)
        VALUES (?, ?, ?, ?, ?, GETDATE())
        """
        execute_query(query, (self.name, self.email, hashed_password, salt, self.role))
        print(f"User '{self.name}' added successfully.")
        
    def update_user(self, user_id):
        """Update user information."""
        # Check if password has changed
        current_user = User.get_user_by_id(user_id)
        
        if current_user and self.password:
            # Password is being updated, generate new salt and hash
            salt = os.urandom(32).hex()
            hashed_password = self._hash_password(self.password, salt)
            
            query = """
            UPDATE Users
            SET Name = ?, Email = ?, Password = ?, Salt = ?, Role = ?
            WHERE UserID = ?
            """
            execute_query(query, (self.name, self.email, hashed_password, salt, self.role, user_id))
        else:
            # Password not changing, update other fields only
            query = """
            UPDATE Users
            SET Name = ?, Email = ?, Role = ?
            WHERE UserID = ?
            """
            execute_query(query, (self.name, self.email, self.role, user_id))
            
        print(f"User '{self.name}' updated successfully.")
        
    def delete_user(self, user_id):
        """Delete a user."""
        query = "DELETE FROM Users WHERE UserID = ?"
        execute_query(query, (user_id,))
        print(f"User deleted successfully.")
        
    @staticmethod
    def _hash_password(password, salt):
        """Hash a password with the given salt using SHA-256."""
        # Combine password and salt, then hash
        salted_password = password.encode('utf-8') + bytes.fromhex(salt)
        hashed = hashlib.sha256(salted_password).hexdigest()
        return hashed
        
    @staticmethod
    def verify_password(password, hashed_password, salt):
        """Verify a password against a hash."""
        # Hash the input password with the same salt
        calculated_hash = User._hash_password(password, salt)
        # Compare the calculated hash with the stored hash
        return calculated_hash == hashed_password
        
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID."""
        query = "SELECT * FROM Users WHERE UserID = ?"
        result = execute_query(query, (user_id,), fetch=True)
        if result:
            return result[0]
        return None
        
    @staticmethod
    def get_user_by_email(email):
        """Get user by email."""
        query = "SELECT * FROM Users WHERE Email = ?"
        result = execute_query(query, (email,), fetch=True)
        if result:
            return result[0]
        return None
        
    @staticmethod
    def authenticate(email, password):
        """Authenticate a user by email and password."""
        user = User.get_user_by_email(email)
        
        if not user:
            return None
            
        if User.verify_password(password, user['Password'], user['Salt']):
            return user
            
        return None
        
    @staticmethod
    def generate_auth_token(user_id):
        """Generate authentication token for user."""
        token = str(uuid.uuid4())
        expiry = "DATEADD(hour, 24, GETDATE())"  # Token expires in 24 hours
        
        query = """
        INSERT INTO AuthTokens (UserID, Token, ExpiresAt, CreatedAt)
        VALUES (?, ?, {}, GETDATE())
        """.format(expiry)
        
        execute_query(query, (user_id, token))
        return token
        
    @staticmethod
    def validate_auth_token(token):
        """Validate an authentication token."""
        query = """
        SELECT u.* 
        FROM AuthTokens t
        JOIN Users u ON t.UserID = u.UserID
        WHERE t.Token = ? AND t.ExpiresAt > GETDATE()
        """
        
        result = execute_query(query, (token,), fetch=True)
        if result:
            return result[0]
        return None


def view_users():
    """View all users."""
    query = "SELECT UserID, Name, Email, Role, CreatedAt FROM Users"
    users = execute_query(query, fetch=True)  # Get all users without password hash

    if not users:
        print("⚠️ No users found in the database.")
        return

    print("🧑‍💻 User list:")
    for user in users:
        print(user)
