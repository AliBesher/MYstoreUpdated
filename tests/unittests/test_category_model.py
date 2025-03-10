import unittest
from unittest.mock import patch, MagicMock
from app.models.category import Category

class TestCategoryModel(unittest.TestCase):

    @patch('app.models.category.execute_query')
    def test_add_category(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن الفئة وإضافته
        category = Category("Test Category", "Test Description")
        category.add_category()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لإدراج فئة جديدة
        self.assertIn("INSERT INTO Categories", call_args[0])

        # التحقق من أن معلمات الاستعلام تحتوي على بيانات الفئة
        params = call_args[1]
        self.assertEqual(params[0], "Test Category")
        self.assertEqual(params[1], "Test Description")

    @patch('app.models.category.execute_query')
    def test_update_category(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن الفئة وتحديثه
        category = Category("Updated Category", "Updated Description")
        category.update_category(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لتحديث فئة
        self.assertIn("UPDATE Categories", call_args[0])

        # التحقق من أن معلمات الاستعلام تحتوي على بيانات الفئة المحدثة
        params = call_args[1]
        self.assertEqual(params[0], "Updated Category")
        self.assertEqual(params[1], "Updated Description")
        self.assertEqual(params[2], 1)  # معرف الفئة

    @patch('app.models.category.execute_query')
    def test_delete_category(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن الفئة وحذفه
        category = Category("Test Category", "Test Description")
        category.delete_category(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لحذف فئة
        self.assertIn("DELETE FROM Categories WHERE CategoryID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

    @patch('app.models.category.execute_query')
    def test_get_category_by_id(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [{
            "CategoryID": 1,
            "Name": "Test Category",
            "Description": "Test Description"
        }]

        # استدعاء دالة الحصول على الفئة بواسطة المعرف
        category = Category.get_category_by_id(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للبحث عن فئة
        self.assertIn("SELECT * FROM Categories WHERE CategoryID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

        # التحقق من النتيجة
        self.assertEqual(category["CategoryID"], 1)
        self.assertEqual(category["Name"], "Test Category")
        self.assertEqual(category["Description"], "Test Description")

    @patch('app.models.category.execute_query')
    def test_get_category_by_id_not_found(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام لفئة غير موجودة
        mock_execute_query.return_value = []

        # استدعاء دالة الحصول على الفئة بواسطة المعرف
        category = Category.get_category_by_id(999)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()

        # التحقق من النتيجة
        self.assertIsNone(category)

    @patch('app.models.category.execute_query')
    def test_get_all_categories(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [
            {
                "CategoryID": 1,
                "Name": "Category 1",
                "Description": "Description 1"
            },
            {
                "CategoryID": 2,
                "Name": "Category 2",
                "Description": "Description 2"
            }
        ]

        # استدعاء دالة الحصول على جميع الفئات
        categories = Category.get_all_categories()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للحصول على جميع الفئات
        self.assertIn("SELECT * FROM Categories ORDER BY Name", call_args[0])

        # التحقق من النتيجة
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0]["Name"], "Category 1")
        self.assertEqual(categories[1]["Name"], "Category 2")

    @patch('app.models.category.execute_query')
    def test_get_all_categories_empty(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام لقائمة فئات فارغة
        mock_execute_query.return_value = []

        # استدعاء دالة الحصول على جميع الفئات
        categories = Category.get_all_categories()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()

        # التحقق من النتيجة
        self.assertEqual(categories, [])

if __name__ == '__main__':
    unittest.main()
