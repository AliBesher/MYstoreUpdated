import unittest
from unittest.mock import patch, MagicMock
from app.services.user_service import UserService
from app.models import User

class TestUserService(unittest.TestCase):

    @patch('app.services.user_service.User.get_user_by_email')
    @patch('app.services.user_service.User.add_user')
    def test_add_user_success(self, mock_add_user, mock_get_user_by_email):
        # Mock the get_user_by_email method to return None (email not in use)
        mock_get_user_by_email.return_value = None

        # Mock the add_user method
        mock_add_user.return_value = None

        # Test adding a user
        result = UserService.add_user(
            name="Test User",
            email="test@example.com",
            password="password123"
        )

        # Verify results
        self.assertEqual(result, "User 'Test User' added successfully.")
        mock_get_user_by_email.assert_called_once_with("test@example.com")
        mock_add_user.assert_called_once()

    @patch('app.services.user_service.User.get_user_by_email')
    def test_add_user_email_exists(self, mock_get_user_by_email):
        # Mock the get_user_by_email method to return a user (email in use)
        mock_get_user_by_email.return_value = {"UserID": 1, "Email": "test@example.com"}

        # Test adding a user with an existing email
        result = UserService.add_user(
            name="Test User",
            email="test@example.com",
            password="password123"
        )

        # Verify results
        self.assertEqual(result, "⚠️ Email already in use.")
        mock_get_user_by_email.assert_called_once_with("test@example.com")

    def test_add_user_missing_fields(self):
        # Test with missing name
        result = UserService.add_user(
            name="",
            email="test@example.com",
            password="password123"
        )
        self.assertEqual(result, "⚠️ Name, email, and password are required.")

        # Test with missing email
        result = UserService.add_user(
            name="Test User",
            email="",
            password="password123"
        )
        self.assertEqual(result, "⚠️ Name, email, and password are required.")

        # Test with missing password
        result = UserService.add_user(
            name="Test User",
            email="test@example.com",
            password=""
        )
        self.assertEqual(result, "⚠️ Name, email, and password are required.")

    def test_add_user_invalid_email(self):
        # Test with invalid email format
        result = UserService.add_user(
            name="Test User",
            email="invalid-email",
            password="password123"
        )
        self.assertEqual(result, "⚠️ Invalid email format.")

    def test_add_user_short_password(self):
        # Test with short password
        result = UserService.add_user(
            name="Test User",
            email="test@example.com",
            password="short"
        )
        self.assertEqual(result, "⚠️ Password must be at least 6 characters long.")

    def test_add_user_invalid_role(self):
        # Test with invalid role
        result = UserService.add_user(
            name="Test User",
            email="test@example.com",
            password="password123",
            role="invalid_role"
        )
        self.assertTrue("⚠️ Invalid role" in result)

    @patch('app.services.user_service.User.get_user_by_id')
    @patch('app.services.user_service.User.get_user_by_email')
    @patch('app.services.user_service.User.update_user')
    def test_update_user_success(self, mock_update_user, mock_get_user_by_email, mock_get_user_by_id):
        # Mock the get_user_by_id method to return a user
        mock_get_user_by_id.return_value = {
            "UserID": 1,
            "Name": "Old Name",
            "Email": "old@example.com"
        }

        # Mock the get_user_by_email method to return None (new email not in use)
        mock_get_user_by_email.return_value = None

        # Mock the update_user method
        mock_update_user.return_value = None

        # Test updating a user
        result = UserService.update_user(
            user_id=1,
            name="New Name",
            email="new@example.com",
            password="newpassword123",
            role="admin"
        )

        # Verify results
        self.assertEqual(result, "User 'New Name' updated successfully.")
        mock_get_user_by_id.assert_called_once_with(1)
        mock_get_user_by_email.assert_called_once_with("new@example.com")
        mock_update_user.assert_called_once()

    @patch('app.services.user_service.User.get_user_by_id')
    def test_update_user_not_found(self, mock_get_user_by_id):
        # Mock the get_user_by_id method to return None (user not found)
        mock_get_user_by_id.return_value = None

        # Test updating a non-existent user
        result = UserService.update_user(
            user_id=999,
            name="New Name",
            email="new@example.com",
            password="newpassword123",
            role="customer"
        )

        # Verify results
        self.assertEqual(result, "⚠️ User not found.")
        mock_get_user_by_id.assert_called_once_with(999)

    @patch('app.services.user_service.User.get_user_by_id')
    @patch('app.services.user_service.User.get_user_by_email')
    def test_update_user_email_in_use(self, mock_get_user_by_email, mock_get_user_by_id):
        # Mock the get_user_by_id method to return a user
        mock_get_user_by_id.return_value = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com"
        }

        # Mock the get_user_by_email method to return another user (email in use)
        mock_get_user_by_email.return_value = {
            "UserID": 2,
            "Email": "new@example.com"
        }

        # Test updating a user with an email in use by another user
        result = UserService.update_user(
            user_id=1,
            name="Test User",
            email="new@example.com",
            password="password123",
            role="customer"
        )

        # Verify results
        self.assertEqual(result, "⚠️ Email already in use by another user.")
        mock_get_user_by_id.assert_called_once_with(1)
        mock_get_user_by_email.assert_called_once_with("new@example.com")

    def test_update_user_invalid_data(self):
        # Mock user exists
        with patch('app.services.user_service.User.get_user_by_id') as mock_get_user_by_id:
            mock_get_user_by_id.return_value = {"UserID": 1, "Name": "Test User"}

            # Test with missing name
            result = UserService.update_user(1, "", "test@example.com", "password123", "customer")
            self.assertEqual(result, "⚠️ Name and email are required.")

            # Test with missing email
            result = UserService.update_user(1, "Test User", "", "password123", "customer")
            self.assertEqual(result, "⚠️ Name and email are required.")

            # Test with invalid email
            result = UserService.update_user(1, "Test User", "invalid-email", "password123", "customer")
            self.assertEqual(result, "⚠️ Invalid email format.")

            # Test with short password
            result = UserService.update_user(1, "Test User", "test@example.com", "short", "customer")
            self.assertEqual(result, "⚠️ Password must be at least 6 characters long.")

            # Test with invalid role
            result = UserService.update_user(1, "Test User", "test@example.com", "password123", "invalid_role")
            self.assertTrue("⚠️ Invalid role" in result)

    @patch('app.services.user_service.User.get_user_by_id')
    @patch('app.services.user_service.User.delete_user')
    def test_delete_user_success(self, mock_delete_user, mock_get_user_by_id):
        # Mock the get_user_by_id method to return a user
        mock_get_user_by_id.return_value = {"UserID": 1, "Name": "Test User"}

        # Mock the delete_user method
        mock_delete_user.return_value = None

        # Test deleting a user
        result = UserService.delete_user(user_id=1)

        # Verify results
        self.assertEqual(result, "User deleted successfully.")
        mock_get_user_by_id.assert_called_once_with(1)
        mock_delete_user.assert_called_once_with(1)

    @patch('app.services.user_service.User.get_user_by_id')
    def test_delete_user_not_found(self, mock_get_user_by_id):
        # Mock the get_user_by_id method to return None (user not found)
        mock_get_user_by_id.return_value = None

        # Test deleting a non-existent user
        result = UserService.delete_user(user_id=999)

        # Verify results
        self.assertEqual(result, "⚠️ User not found.")
        mock_get_user_by_id.assert_called_once_with(999)

    @patch('app.services.user_service.execute_query')
    def test_get_users(self, mock_execute_query):
        # Mock the execute_query method to return a list of users
        mock_users = [
            {"UserID": 1, "Name": "User 1", "Email": "user1@example.com", "Role": "admin"},
            {"UserID": 2, "Name": "User 2", "Email": "user2@example.com", "Role": "customer"}
        ]
        mock_execute_query.return_value = mock_users

        # Test getting all users
        result = UserService.get_users()

        # Verify results
        self.assertEqual(result, mock_users)
        self.assertEqual(len(result), 2)
        mock_execute_query.assert_called_once()

    @patch('app.services.user_service.execute_query')
    def test_get_users_empty(self, mock_execute_query):
        # Mock the execute_query method to return an empty list
        mock_execute_query.return_value = []

        # Test getting all users when none exist
        result = UserService.get_users()

        # Verify results
        self.assertEqual(result, [])
        mock_execute_query.assert_called_once()

    @patch('app.services.user_service.User.get_user_by_id')
    def test_get_user_by_id_success(self, mock_get_user_by_id):
        # Mock user data
        mock_user = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Role": "customer"
        }
        mock_get_user_by_id.return_value = mock_user

        # Test getting a user by ID
        result = UserService.get_user_by_id(1)

        # Verify results
        self.assertEqual(result, mock_user)
        mock_get_user_by_id.assert_called_once_with(1)

    @patch('app.services.user_service.User.get_user_by_id')
    def test_get_user_by_id_not_found(self, mock_get_user_by_id):
        # Mock user not found
        mock_get_user_by_id.return_value = None

        # Test getting a non-existent user
        result = UserService.get_user_by_id(999)

        # Verify results
        self.assertIsNone(result)
        mock_get_user_by_id.assert_called_once_with(999)

    def test_get_user_by_id_invalid(self):
        # Test with invalid ID (0 or negative)
        result = UserService.get_user_by_id(0)
        self.assertIsNone(result)

        result = UserService.get_user_by_id(-1)
        self.assertIsNone(result)

    @patch('app.services.user_service.User.get_user_by_email')
    @patch('app.services.user_service.User.verify_password')
    @patch('app.services.user_service.User.generate_auth_token')
    def test_authenticate_user_success(self, mock_generate_token, mock_verify_password, mock_get_user_by_email):
        # Mock user data
        mock_user = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Password": "hashed_password",
            "Salt": "salt123",
            "Role": "customer"
        }
        mock_get_user_by_email.return_value = mock_user

        # Mock password verification success
        mock_verify_password.return_value = True

        # Mock token generation
        mock_generate_token.return_value = "fake_token_12345"

        # Test successful authentication
        result = UserService.authenticate_user("test@example.com", "password123")

        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result["user"]["id"], 1)
        self.assertEqual(result["user"]["name"], "Test User")
        self.assertEqual(result["user"]["email"], "test@example.com")
        self.assertEqual(result["user"]["role"], "customer")
        self.assertEqual(result["token"], "fake_token_12345")

        mock_get_user_by_email.assert_called_once_with("test@example.com")
        mock_verify_password.assert_called_once_with("password123", "hashed_password", "salt123")
        mock_generate_token.assert_called_once_with(1)

    @patch('app.services.user_service.User.get_user_by_email')
    def test_authenticate_user_not_found(self, mock_get_user_by_email):
        # Mock user not found
        mock_get_user_by_email.return_value = None

        # Test authentication with non-existent email
        result = UserService.authenticate_user("nonexistent@example.com", "password123")

        # Verify results
        self.assertIsNone(result)
        mock_get_user_by_email.assert_called_once_with("nonexistent@example.com")

    @patch('app.services.user_service.User.get_user_by_email')
    @patch('app.services.user_service.User.verify_password')
    def test_authenticate_user_wrong_password(self, mock_verify_password, mock_get_user_by_email):
        # Mock user data
        mock_user = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Password": "hashed_password",
            "Salt": "salt123",
            "Role": "customer"
        }
        mock_get_user_by_email.return_value = mock_user

        # Mock password verification failure
        mock_verify_password.return_value = False

        # Test authentication with wrong password
        result = UserService.authenticate_user("test@example.com", "wrong_password")

        # Verify results
        self.assertIsNone(result)
        mock_get_user_by_email.assert_called_once_with("test@example.com")
        mock_verify_password.assert_called_once_with("wrong_password", "hashed_password", "salt123")

    @patch('app.services.user_service.User.get_user_by_id')
    @patch('app.services.user_service.User.reset_password')
    def test_reset_user_password_success(self, mock_reset_password, mock_get_user_by_id):
        # Mock user data
        mock_user = {"UserID": 1, "Name": "Test User"}
        mock_get_user_by_id.return_value = mock_user

        # Mock password reset success
        mock_reset_password.return_value = True

        # Test successful password reset
        result = UserService.reset_user_password(1, "newpassword123")

        # Verify results
        self.assertEqual(result, "✅ Password reset successfully.")
        mock_get_user_by_id.assert_called_once_with(1)
        mock_reset_password.assert_called_once_with(1, "newpassword123")

    @patch('app.services.user_service.User.get_user_by_id')
    def test_reset_user_password_user_not_found(self, mock_get_user_by_id):
        # Mock user not found
        mock_get_user_by_id.return_value = None

        # Test password reset for non-existent user
        result = UserService.reset_user_password(999, "newpassword123")

        # Verify results
        self.assertEqual(result, "⚠️ User not found.")
        mock_get_user_by_id.assert_called_once_with(999)

    @patch('app.services.user_service.User.get_user_by_id')
    @patch('app.services.user_service.User.reset_password')
    def test_reset_user_password_failure(self, mock_reset_password, mock_get_user_by_id):
        # Mock user data
        mock_user = {"UserID": 1, "Name": "Test User"}
        mock_get_user_by_id.return_value = mock_user

        # Mock password reset failure
        mock_reset_password.return_value = False

        # Test failed password reset
        result = UserService.reset_user_password(1, "newpassword123")

        # Verify results
        self.assertEqual(result, "⚠️ Failed to reset password.")
        mock_get_user_by_id.assert_called_once_with(1)
        mock_reset_password.assert_called_once_with(1, "newpassword123")

    def test_reset_user_password_invalid_password(self):
        # Test with short password
        with patch('app.services.user_service.User.get_user_by_id') as mock_get_user_by_id:
            mock_get_user_by_id.return_value = {"UserID": 1, "Name": "Test User"}

            result = UserService.reset_user_password(1, "short")
            self.assertEqual(result, "⚠️ Password must be at least 6 characters long.")

if __name__ == '__main__':
    unittest.main()
