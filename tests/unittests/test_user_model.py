import unittest
from unittest.mock import patch, MagicMock
from app.models.user import User

class TestUserModel(unittest.TestCase):

    @patch('app.models.user.execute_query')
    @patch('app.models.user.os.urandom')
    def test_add_user(self, mock_urandom, mock_execute_query):
        
        mock_urandom.return_value = b'test_salt'

       
        mock_execute_query.return_value = None

        
        user = User("Test User", "test@example.com", "password123", "customer")
        user.add_user()

        # Verify that execute_query is called with the correct parameters.
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("INSERT INTO Users", call_args[0])

        
        params = call_args[1]
        self.assertEqual(params[0], "Test User")
        self.assertEqual(params[1], "test@example.com")
       
        self.assertEqual(params[4], "customer")  

    @patch('app.models.user.execute_query')
    def test_update_user_with_new_password(self, mock_execute_query):
        
        mock_execute_query.return_value = None

        
        with patch('app.models.user.User.get_user_by_id') as mock_get_user:
            mock_get_user.return_value = {
                "UserID": 1,
                "Name": "Old Name",
                "Email": "old@example.com",
                "Password": "old_hash",
                "Salt": "old_salt"
            }

            # os.urandom emulation to control the new Salt
            with patch('app.models.user.os.urandom') as mock_urandom:
                mock_urandom.return_value = b'new_salt'

                # Create a user object and update it with a new password.
                user = User("New Name", "new@example.com", "newpassword123", "admin")
                user.update_user(1)

               
                mock_execute_query.assert_called_once()
                call_args = mock_execute_query.call_args[0]

               
                self.assertIn("UPDATE Users", call_args[0])

                
                params = call_args[1]
                self.assertEqual(params[0], "New Name")  
                self.assertEqual(params[1], "new@example.com")  
                self.assertEqual(params[-1], 1)  

    @patch('app.models.user.execute_query')
    def test_update_user_without_password(self, mock_execute_query):
       
        mock_execute_query.return_value = None

        
        with patch('app.models.user.User.get_user_by_id') as mock_get_user:
            mock_get_user.return_value = {
                "UserID": 1,
                "Name": "Old Name",
                "Email": "old@example.com"
            }

            # Create and update user object without new password (empty password)
            user = User("New Name", "new@example.com", "", "admin")
            user.update_user(1)

            
            mock_execute_query.assert_called_once()
            call_args = mock_execute_query.call_args[0]

           
            self.assertIn("UPDATE Users", call_args[0])
            self.assertIn("Name = ?, Email = ?, Role = ?", call_args[0])

    @patch('app.models.user.execute_query')
    def test_delete_user(self, mock_execute_query):
   
        mock_execute_query.return_value = None

        
        user = User("", "", "", "")  
        user.delete_user(1)

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

   
        self.assertIn("DELETE FROM Users", call_args[0])
        self.assertEqual(call_args[1], (1,))

    def test_hash_password(self):
     
        password = "password123"
        salt = "test_salt"

        
        hashed_password = User._hash_password(password, salt)

       
        self.assertNotEqual(hashed_password, password)

        # Verify that the hash is consistent (gives the same result for the same input)
        hashed_password2 = User._hash_password(password, salt)
        self.assertEqual(hashed_password, hashed_password2)

        
        hashed_password3 = User._hash_password("differentpassword", salt)
        self.assertNotEqual(hashed_password, hashed_password3)

    def test_verify_password(self):
     
        password = "password123"
        salt = "test_salt"

       
        hashed_password = User._hash_password(password, salt)

        
        self.assertTrue(User.verify_password(password, hashed_password, salt))

        
        self.assertFalse(User.verify_password("wrongpassword", hashed_password, salt))

    @patch('app.models.user.execute_query')
    def test_get_user_by_id(self, mock_execute_query):
       
        mock_execute_query.return_value = [{
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Role": "customer"
        }]

        
        user = User.get_user_by_id(1)

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

      
        self.assertIn("SELECT * FROM Users WHERE UserID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

       
        self.assertEqual(user["UserID"], 1)
        self.assertEqual(user["Name"], "Test User")

    @patch('app.models.user.execute_query')
    def test_get_user_by_id_not_found(self, mock_execute_query):
        
        mock_execute_query.return_value = []

       
        user = User.get_user_by_id(999)

       
        mock_execute_query.assert_called_once()

     
        self.assertIsNone(user)

    @patch('app.models.user.execute_query')
    def test_get_user_by_email(self, mock_execute_query):
        
        mock_execute_query.return_value = [{
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Role": "customer"
        }]

        # Call the function get user by email
        user = User.get_user_by_email("test@example.com")

     
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("SELECT * FROM Users WHERE Email = ?", call_args[0])
        self.assertEqual(call_args[1], ("test@example.com",))

        self.assertEqual(user["Email"], "test@example.com")

    @patch('app.models.user.User.get_user_by_email')
    @patch('app.models.user.User.verify_password')
    def test_authenticate(self, mock_verify_password, mock_get_user_by_email):
        # User simulation
        mock_user = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Password": "hashed_password",
            "Salt": "test_salt"
        }
        mock_get_user_by_email.return_value = mock_user

    
        mock_verify_password.return_value = True

        
        authenticated_user = User.authenticate("test@example.com", "password123")

        # Verify that get_user_by_email is called with the correct parameters.
        mock_get_user_by_email.assert_called_once_with("test@example.com")

        
        mock_verify_password.assert_called_once_with("password123", "hashed_password", "test_salt")

        
        self.assertEqual(authenticated_user, mock_user)

    @patch('app.models.user.User.get_user_by_email')
    def test_authenticate_user_not_found(self, mock_get_user_by_email):
       
        mock_get_user_by_email.return_value = None

        authenticated_user = User.authenticate("nonexistent@example.com", "password123")

        # Verify that get_user_by_email is called with the correct parameters.
        mock_get_user_by_email.assert_called_once_with("nonexistent@example.com")

        
        self.assertIsNone(authenticated_user)

    @patch('app.models.user.User.get_user_by_email')
    @patch('app.models.user.User.verify_password')
    def test_authenticate_wrong_password(self, mock_verify_password, mock_get_user_by_email):
        
        mock_user = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Password": "hashed_password",
            "Salt": "test_salt"
        }
        mock_get_user_by_email.return_value = mock_user

    
        mock_verify_password.return_value = False

        authenticated_user = User.authenticate("test@example.com", "wrongpassword")

        
        mock_get_user_by_email.assert_called_once_with("test@example.com")

        # Verify that verify_password is called with the correct parameters.
        mock_verify_password.assert_called_once_with("wrongpassword", "hashed_password", "test_salt")

  
        self.assertIsNone(authenticated_user)

    @patch('app.models.user.execute_query')
    @patch('app.models.user.uuid.uuid4')
    def test_generate_auth_token(self, mock_uuid4, mock_execute_query):
      
        mock_uuid4.return_value = "fake-uuid-token"

     
        mock_execute_query.return_value = None

      
        token = User.generate_auth_token(1)

        mock_uuid4.assert_called_once()

      
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("INSERT INTO AuthTokens", call_args[0])

        
        self.assertEqual(token, "fake-uuid-token")

    @patch('app.models.user.execute_query')
    def test_validate_auth_token_valid(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام لرمز صالح
        mock_execute_query.return_value = [{
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Role": "customer"
        }]

        # استدعاء دالة التحقق من رمز المصادقة
        user = User.validate_auth_token("valid-token")

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL يحتوي على الأجزاء الأساسية
        self.assertIn("SELECT u.*", call_args[0])
        self.assertIn("FROM AuthTokens t", call_args[0])
        self.assertIn("JOIN Users u ON t.UserID = u.UserID", call_args[0])
        self.assertEqual(call_args[1], ("valid-token",))

        # التحقق من النتيجة
        self.assertEqual(user["UserID"], 1)
        self.assertEqual(user["Email"], "test@example.com")


    @patch('app.models.user.execute_query')
    def test_validate_auth_token_invalid(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام لرمز غير صالح
        mock_execute_query.return_value = []

        # استدعاء دالة التحقق من رمز المصادقة
        user = User.validate_auth_token("invalid-token")

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()

        self.assertIsNone(user)

    @patch('app.models.user.execute_query')
    @patch('app.models.user.User.get_user_by_id')
    @patch('app.models.user.os.urandom')
    def test_reset_password(self, mock_urandom, mock_get_user_by_id, mock_execute_query):
        
        mock_user = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com"
        }
        mock_get_user_by_id.return_value = mock_user

        mock_urandom.return_value = b'new_salt'

        mock_execute_query.return_value = None

        
        result = User.reset_password(1, "newpassword123")

       
        mock_get_user_by_id.assert_called_once_with(1)

      
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

       
        self.assertIn("UPDATE Users", call_args[0])
        self.assertIn("Password = ?, Salt = ?", call_args[0])

     
        self.assertTrue(result)

    @patch('app.models.user.User.get_user_by_id')
    def test_reset_password_user_not_found(self, mock_get_user_by_id):
        
        mock_get_user_by_id.return_value = None

        
        result = User.reset_password(999, "newpassword123")

        
        mock_get_user_by_id.assert_called_once_with(999)

      
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
