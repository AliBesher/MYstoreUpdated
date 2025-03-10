import unittest
from unittest.mock import patch, MagicMock
from app.models.user import User

class TestUserModel(unittest.TestCase):

    @patch('app.models.user.execute_query')
    @patch('app.models.user.os.urandom')
    def test_add_user(self, mock_urandom, mock_execute_query):
        # محاكاة توليد الملح العشوائي
        mock_urandom.return_value = b'test_salt'

        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن المستخدم وإضافته
        user = User("Test User", "test@example.com", "password123", "customer")
        user.add_user()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لإدراج مستخدم جديد
        self.assertIn("INSERT INTO Users", call_args[0])

        # التحقق من أن معلمات الاستعلام تحتوي على بيانات المستخدم
        params = call_args[1]
        self.assertEqual(params[0], "Test User")
        self.assertEqual(params[1], "test@example.com")
        # لا نتحقق من الـ Salt مباشرة لأنه يتم تحويله إلى تمثيل هيكس
        self.assertEqual(params[4], "customer")  # فحص الدور

    @patch('app.models.user.execute_query')
    def test_update_user_with_new_password(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # محاكاة المستخدم الحالي
        with patch('app.models.user.User.get_user_by_id') as mock_get_user:
            mock_get_user.return_value = {
                "UserID": 1,
                "Name": "Old Name",
                "Email": "old@example.com",
                "Password": "old_hash",
                "Salt": "old_salt"
            }

            # محاكاة os.urandom للتحكم في Salt الجديد
            with patch('app.models.user.os.urandom') as mock_urandom:
                mock_urandom.return_value = b'new_salt'

                # إنشاء كائن المستخدم وتحديثه مع كلمة مرور جديدة
                user = User("New Name", "new@example.com", "newpassword123", "admin")
                user.update_user(1)

                # التحقق من استدعاء execute_query بالمعلمات الصحيحة
                mock_execute_query.assert_called_once()
                call_args = mock_execute_query.call_args[0]

                # التحقق من أن الاستعلام SQL هو لتحديث المستخدم
                self.assertIn("UPDATE Users", call_args[0])

                # التحقق من أن معلمات الاستعلام تحتوي على البيانات المحدثة
                params = call_args[1]
                self.assertEqual(params[0], "New Name")  # الاسم
                self.assertEqual(params[1], "new@example.com")  # البريد
                self.assertEqual(params[-1], 1)  # معرف المستخدم (آخر معلمة)

    @patch('app.models.user.execute_query')
    def test_update_user_without_password(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # محاكاة المستخدم الحالي
        with patch('app.models.user.User.get_user_by_id') as mock_get_user:
            mock_get_user.return_value = {
                "UserID": 1,
                "Name": "Old Name",
                "Email": "old@example.com"
            }

            # إنشاء كائن المستخدم وتحديثه بدون كلمة مرور جديدة (كلمة مرور فارغة)
            user = User("New Name", "new@example.com", "", "admin")
            user.update_user(1)

            # التحقق من استدعاء execute_query بالمعلمات الصحيحة
            mock_execute_query.assert_called_once()
            call_args = mock_execute_query.call_args[0]

            # التحقق من أن الاستعلام SQL هو لتحديث المستخدم بدون كلمة المرور
            self.assertIn("UPDATE Users", call_args[0])
            self.assertIn("Name = ?, Email = ?, Role = ?", call_args[0])

    @patch('app.models.user.execute_query')
    def test_delete_user(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن المستخدم وحذفه
        user = User("", "", "", "")  # كائن فارغ للحذف
        user.delete_user(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لحذف المستخدم
        self.assertIn("DELETE FROM Users", call_args[0])
        self.assertEqual(call_args[1], (1,))

    def test_hash_password(self):
        # اختبار هاش كلمة المرور
        password = "password123"
        salt = "test_salt"

        # حساب الهاش
        hashed_password = User._hash_password(password, salt)

        # التحقق من أن الهاش ليس كلمة المرور الأصلية
        self.assertNotEqual(hashed_password, password)

        # التحقق من أن الهاش متناسق (يعطي نفس النتيجة لنفس المدخلات)
        hashed_password2 = User._hash_password(password, salt)
        self.assertEqual(hashed_password, hashed_password2)

        # التحقق من أن الهاش مختلف لكلمات مرور مختلفة
        hashed_password3 = User._hash_password("differentpassword", salt)
        self.assertNotEqual(hashed_password, hashed_password3)

    def test_verify_password(self):
        # اختبار التحقق من كلمة المرور
        password = "password123"
        salt = "test_salt"

        # حساب الهاش
        hashed_password = User._hash_password(password, salt)

        # التحقق من أن كلمة المرور الصحيحة تجتاز عملية التحقق
        self.assertTrue(User.verify_password(password, hashed_password, salt))

        # التحقق من أن كلمة المرور الخاطئة لا تجتاز عملية التحقق
        self.assertFalse(User.verify_password("wrongpassword", hashed_password, salt))

    @patch('app.models.user.execute_query')
    def test_get_user_by_id(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [{
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Role": "customer"
        }]

        # استدعاء دالة الحصول على المستخدم بواسطة المعرف
        user = User.get_user_by_id(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للبحث عن مستخدم
        self.assertIn("SELECT * FROM Users WHERE UserID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

        # التحقق من النتيجة
        self.assertEqual(user["UserID"], 1)
        self.assertEqual(user["Name"], "Test User")

    @patch('app.models.user.execute_query')
    def test_get_user_by_id_not_found(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام لمستخدم غير موجود
        mock_execute_query.return_value = []

        # استدعاء دالة الحصول على المستخدم بواسطة المعرف
        user = User.get_user_by_id(999)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()

        # التحقق من النتيجة
        self.assertIsNone(user)

    @patch('app.models.user.execute_query')
    def test_get_user_by_email(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [{
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Role": "customer"
        }]

        # استدعاء دالة الحصول على المستخدم بواسطة البريد الإلكتروني
        user = User.get_user_by_email("test@example.com")

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للبحث عن مستخدم
        self.assertIn("SELECT * FROM Users WHERE Email = ?", call_args[0])
        self.assertEqual(call_args[1], ("test@example.com",))

        # التحقق من النتيجة
        self.assertEqual(user["Email"], "test@example.com")

    @patch('app.models.user.User.get_user_by_email')
    @patch('app.models.user.User.verify_password')
    def test_authenticate(self, mock_verify_password, mock_get_user_by_email):
        # محاكاة المستخدم
        mock_user = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Password": "hashed_password",
            "Salt": "test_salt"
        }
        mock_get_user_by_email.return_value = mock_user

        # محاكاة التحقق من كلمة المرور
        mock_verify_password.return_value = True

        # استدعاء دالة المصادقة
        authenticated_user = User.authenticate("test@example.com", "password123")

        # التحقق من استدعاء get_user_by_email بالمعلمات الصحيحة
        mock_get_user_by_email.assert_called_once_with("test@example.com")

        # التحقق من استدعاء verify_password بالمعلمات الصحيحة
        mock_verify_password.assert_called_once_with("password123", "hashed_password", "test_salt")

        # التحقق من النتيجة
        self.assertEqual(authenticated_user, mock_user)

    @patch('app.models.user.User.get_user_by_email')
    def test_authenticate_user_not_found(self, mock_get_user_by_email):
        # محاكاة مستخدم غير موجود
        mock_get_user_by_email.return_value = None

        # استدعاء دالة المصادقة
        authenticated_user = User.authenticate("nonexistent@example.com", "password123")

        # التحقق من استدعاء get_user_by_email بالمعلمات الصحيحة
        mock_get_user_by_email.assert_called_once_with("nonexistent@example.com")

        # التحقق من النتيجة
        self.assertIsNone(authenticated_user)

    @patch('app.models.user.User.get_user_by_email')
    @patch('app.models.user.User.verify_password')
    def test_authenticate_wrong_password(self, mock_verify_password, mock_get_user_by_email):
        # محاكاة المستخدم
        mock_user = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Password": "hashed_password",
            "Salt": "test_salt"
        }
        mock_get_user_by_email.return_value = mock_user

        # محاكاة فشل التحقق من كلمة المرور
        mock_verify_password.return_value = False

        # استدعاء دالة المصادقة
        authenticated_user = User.authenticate("test@example.com", "wrongpassword")

        # التحقق من استدعاء get_user_by_email بالمعلمات الصحيحة
        mock_get_user_by_email.assert_called_once_with("test@example.com")

        # التحقق من استدعاء verify_password بالمعلمات الصحيحة
        mock_verify_password.assert_called_once_with("wrongpassword", "hashed_password", "test_salt")

        # التحقق من النتيجة
        self.assertIsNone(authenticated_user)

    @patch('app.models.user.execute_query')
    @patch('app.models.user.uuid.uuid4')
    def test_generate_auth_token(self, mock_uuid4, mock_execute_query):
        # محاكاة توليد UUID
        mock_uuid4.return_value = "fake-uuid-token"

        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # استدعاء دالة توليد رمز المصادقة
        token = User.generate_auth_token(1)

        # التحقق من استدعاء uuid4
        mock_uuid4.assert_called_once()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لإدراج رمز المصادقة
        self.assertIn("INSERT INTO AuthTokens", call_args[0])

        # التحقق من النتيجة
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

        # التحقق من النتيجة
        self.assertIsNone(user)

    @patch('app.models.user.execute_query')
    @patch('app.models.user.User.get_user_by_id')
    @patch('app.models.user.os.urandom')
    def test_reset_password(self, mock_urandom, mock_get_user_by_id, mock_execute_query):
        # محاكاة المستخدم
        mock_user = {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com"
        }
        mock_get_user_by_id.return_value = mock_user

        # محاكاة توليد الملح العشوائي
        mock_urandom.return_value = b'new_salt'

        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # استدعاء دالة إعادة تعيين كلمة المرور
        result = User.reset_password(1, "newpassword123")

        # التحقق من استدعاء get_user_by_id بالمعلمات الصحيحة
        mock_get_user_by_id.assert_called_once_with(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لتحديث كلمة المرور
        self.assertIn("UPDATE Users", call_args[0])
        self.assertIn("Password = ?, Salt = ?", call_args[0])

        # التحقق من النتيجة
        self.assertTrue(result)

    @patch('app.models.user.User.get_user_by_id')
    def test_reset_password_user_not_found(self, mock_get_user_by_id):
        # محاكاة مستخدم غير موجود
        mock_get_user_by_id.return_value = None

        # استدعاء دالة إعادة تعيين كلمة المرور
        result = User.reset_password(999, "newpassword123")

        # التحقق من استدعاء get_user_by_id بالمعلمات الصحيحة
        mock_get_user_by_id.assert_called_once_with(999)

        # التحقق من النتيجة
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
