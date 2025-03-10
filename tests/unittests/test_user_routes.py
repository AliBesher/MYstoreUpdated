import unittest
from unittest.mock import patch
from app import create_app
from app.services.user_service import UserService

class TestUserRoutes(unittest.TestCase):

    def setUp(self):
        # Create Flask app in test mode
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    # --------------------------
    # Test adding a user
    # --------------------------
    @patch('app.services.user_service.UserService.add_user')
    def test_add_user_success(self, mock_add_user):
        # Mock successful user addition
        mock_add_user.return_value = "User 'Test User' added successfully."

        # Test data
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "role": "customer"
        }

        # Send POST request
        response = self.client.post('/api/users', json=data)

        # Verify results
        self.assertEqual(response.status_code, 201)
        self.assertIn("added successfully", response.json["message"])
        mock_add_user.assert_called_once_with(
            "Test User", "test@example.com", "password123", "customer")

    @patch('app.services.user_service.UserService.add_user')
    def test_add_user_email_exists(self, mock_add_user):
        # Mock email already exists error
        mock_add_user.return_value = "⚠️ Email already in use."

        # Test data
        data = {
            "name": "Test User",
            "email": "existing@example.com",
            "password": "password123"
        }

        # Send POST request
        response = self.client.post('/api/users', json=data)

        # Verify results
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already in use", response.json["message"])

    # --------------------------
    # Test updating a user
    # --------------------------
    @patch('app.services.user_service.UserService.update_user')
    def test_update_user_success(self, mock_update_user):
        # Mock successful user update
        mock_update_user.return_value = "User 'Updated User' updated successfully."

        # Test data
        data = {
            "name": "Updated User",
            "email": "updated@example.com",
            "password": "newpassword123",
            "role": "admin"
        }

        # Send PUT request
        response = self.client.put('/api/users/1', json=data)

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertIn("updated successfully", response.json["message"])
        mock_update_user.assert_called_once_with(
            1, "Updated User", "updated@example.com", "newpassword123", "admin")

    @patch('app.services.user_service.UserService.update_user')
    def test_update_user_email_exists(self, mock_update_user):
        # Mock email already in use by another user error
        mock_update_user.return_value = "⚠️ Email already in use by another user."

        # Test data
        data = {
            "name": "Updated User",
            "email": "existing@example.com",
            "password": "newpassword123",
            "role": "customer"
        }

        # Send PUT request
        response = self.client.put('/api/users/1', json=data)

        # Verify results
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already in use", response.json["message"])

    # --------------------------
    # Test deleting a user
    # --------------------------
    @patch('app.services.user_service.UserService.delete_user')
    def test_delete_user_success(self, mock_delete_user):
        # Mock successful user deletion
        mock_delete_user.return_value = "User deleted successfully."

        # Send DELETE request
        response = self.client.delete('/api/users/1')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.json["message"])
        mock_delete_user.assert_called_once_with(1)

    # --------------------------
    # Test getting all users
    # --------------------------
    @patch('app.services.user_service.UserService.get_users')
    def test_get_users(self, mock_get_users):
        # Mock user list
        mock_get_users.return_value = [
            {"UserID": 1, "Name": "User 1", "Email": "user1@example.com", "Role": "admin"},
            {"UserID": 2, "Name": "User 2", "Email": "user2@example.com", "Role": "customer"}
        ]

        # Send GET request
        response = self.client.get('/api/users')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["users"]), 2)
        self.assertEqual(response.json["users"][0]["Name"], "User 1")
        mock_get_users.assert_called_once()

    # --------------------------
    # Test getting a specific user
    # --------------------------
    @patch('app.services.user_service.UserService.get_user_by_id')
    def test_get_user_by_id_success(self, mock_get_user):
        # Mock user data
        mock_get_user.return_value = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Role": "customer"
        }

        # Send GET request
        response = self.client.get('/api/users/1')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["user"]["UserID"], 1)
        self.assertEqual(response.json["user"]["Name"], "Test User")
        mock_get_user.assert_called_once_with(1)

    @patch('app.services.user_service.UserService.get_user_by_id')
    def test_get_user_by_id_not_found(self, mock_get_user):
        # Mock user not found
        mock_get_user.return_value = None

        # Send GET request
        response = self.client.get('/api/users/999')

        # Verify results
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json["message"])
        mock_get_user.assert_called_once_with(999)

    # --------------------------
    # Test user login
    # --------------------------
    @patch('app.services.user_service.UserService.authenticate_user')
    def test_login_success(self, mock_authenticate):
        # Mock successful authentication
        mock_authenticate.return_value = {
            "user": {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com",
                "role": "customer"
            },
            "token": "fake_token_12345"
        }

        # Login data
        data = {
            "email": "test@example.com",
            "password": "password123"
        }

        # Send POST request to login
        response = self.client.post('/api/login', json=data)

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["user"]["name"], "Test User")
        self.assertEqual(response.json["token"], "fake_token_12345")
        mock_authenticate.assert_called_once_with("test@example.com", "password123")

    @patch('app.services.user_service.UserService.authenticate_user')
    def test_login_failed(self, mock_authenticate):
        # Mock failed authentication
        mock_authenticate.return_value = None

        # Login data
        data = {
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }

        # Send POST request to login
        response = self.client.post('/api/login', json=data)

        # Verify results
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid email or password", response.json["message"])
        mock_authenticate.assert_called_once_with("wrong@example.com", "wrongpassword")

if __name__ == '__main__':
    unittest.main()
