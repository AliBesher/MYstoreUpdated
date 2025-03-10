import unittest
from unittest.mock import patch, MagicMock
from app.models.cart import Cart

class TestCartModel(unittest.TestCase):

    @patch('app.models.cart.execute_query')
    def test_add_to_cart_new_item(self, mock_execute_query):
        # محاكاة عدم وجود العنصر في السلة
        mock_execute_query.side_effect = [
            None,  # نتيجة استدعاء get_cart_item
            None   # نتيجة استدعاء insert
        ]

        # إنشاء كائن السلة وإضافة عنصر جديد
        cart = Cart(1)
        cart.add_to_cart(101, 2)

        # التحقق من أن execute_query تم استدعاؤها مرتين
        self.assertEqual(mock_execute_query.call_count, 2)

        # التحقق من الاستدعاء الثاني (إدراج عنصر جديد)
        second_call_args = mock_execute_query.call_args_list[1][0]
        self.assertIn("INSERT INTO Cart", second_call_args[0])
        self.assertEqual(second_call_args[1][0], 1)  # معرف المستخدم
        self.assertEqual(second_call_args[1][1], 101)  # معرف المنتج
        self.assertEqual(second_call_args[1][2], 2)  # الكمية

    @patch('app.models.cart.Cart.get_cart_item')
    @patch('app.models.cart.Cart.update_cart')
    def test_add_to_cart_existing_item(self, mock_update_cart, mock_get_cart_item):
        # محاكاة وجود العنصر في السلة
        mock_get_cart_item.return_value = {
            "CartID": 1,
            "UserID": 1,
            "ProductID": 101,
            "Quantity": 3
        }

        # محاكاة تحديث السلة
        mock_update_cart.return_value = None

        # إنشاء كائن السلة وإضافة عنصر موجود
        cart = Cart(1)
        cart.add_to_cart(101, 2)

        # التحقق من استدعاء get_cart_item
        mock_get_cart_item.assert_called_once_with(101)

        # التحقق من استدعاء update_cart بالكمية الجديدة
        mock_update_cart.assert_called_once_with(101, 5)  # 3 (الكمية الحالية) + 2 (الكمية المضافة)

    def test_add_to_cart_invalid_quantity(self):
        # إنشاء كائن السلة
        cart = Cart(1)

        # محاولة إضافة عنصر بكمية غير صالحة (0 أو سالبة)
        with self.assertRaises(ValueError) as context:
            cart.add_to_cart(101, 0)

        self.assertIn("Quantity must be greater than 0", str(context.exception))

        with self.assertRaises(ValueError) as context:
            cart.add_to_cart(101, -1)

        self.assertIn("Quantity must be greater than 0", str(context.exception))

    @patch('app.models.cart.execute_query')
    def test_update_cart_success(self, mock_execute_query):
        # محاكاة النتائج المتسلسلة: get_cart_item ثم update
        mock_execute_query.side_effect = [
            [{"CartID": 1, "ProductID": 101, "Quantity": 2}],  # نتيجة get_cart_item
            None  # نتيجة update
        ]

        # إنشاء كائن السلة وتحديث كمية العنصر
        cart = Cart(1)
        cart.update_cart(101, 5)

        # التحقق من استدعاء execute_query مرتين
        self.assertEqual(mock_execute_query.call_count, 2)

        # التحقق من الاستدعاء الثاني (تحديث الكمية)
        second_call_args = mock_execute_query.call_args_list[1][0]
        self.assertIn("UPDATE Cart", second_call_args[0])
        self.assertEqual(second_call_args[1][0], 5)  # الكمية الجديدة
        self.assertEqual(second_call_args[1][1], 1)  # معرف المستخدم
        self.assertEqual(second_call_args[1][2], 101)  # معرف المنتج

    def test_update_cart_invalid_quantity(self):
        # إنشاء كائن السلة
        cart = Cart(1)

        # محاولة تحديث عنصر بكمية غير صالحة (0 أو سالبة)
        with self.assertRaises(ValueError) as context:
            cart.update_cart(101, 0)

        self.assertIn("Quantity must be greater than 0", str(context.exception))

        with self.assertRaises(ValueError) as context:
            cart.update_cart(101, -1)

        self.assertIn("Quantity must be greater than 0", str(context.exception))

    @patch('app.models.cart.Cart.get_cart_item')
    def test_update_cart_item_not_found(self, mock_get_cart_item):
        # محاكاة عدم وجود العنصر في السلة
        mock_get_cart_item.return_value = None

        # إنشاء كائن السلة
        cart = Cart(1)

        # محاولة تحديث عنصر غير موجود
        with self.assertRaises(ValueError) as context:
            cart.update_cart(101, 5)

        self.assertIn("Product not found in cart", str(context.exception))
        mock_get_cart_item.assert_called_once_with(101)

    @patch('app.models.cart.execute_query')
    def test_remove_from_cart_success(self, mock_execute_query):
        # محاكاة النتائج المتسلسلة: get_cart_item ثم delete
        mock_execute_query.side_effect = [
            [{"CartID": 1, "ProductID": 101, "Quantity": 2}],  # نتيجة get_cart_item
            None  # نتيجة delete
        ]

        # إنشاء كائن السلة وإزالة عنصر
        cart = Cart(1)
        cart.remove_from_cart(101)

        # التحقق من استدعاء execute_query مرتين
        self.assertEqual(mock_execute_query.call_count, 2)

        # التحقق من الاستدعاء الثاني (حذف العنصر)
        second_call_args = mock_execute_query.call_args_list[1][0]
        self.assertIn("DELETE FROM Cart", second_call_args[0])
        self.assertEqual(second_call_args[1][0], 1)  # معرف المستخدم
        self.assertEqual(second_call_args[1][1], 101)  # معرف المنتج

    @patch('app.models.cart.Cart.get_cart_item')
    def test_remove_from_cart_item_not_found(self, mock_get_cart_item):
        # محاكاة عدم وجود العنصر في السلة
        mock_get_cart_item.return_value = None

        # إنشاء كائن السلة
        cart = Cart(1)

        # محاولة إزالة عنصر غير موجود
        with self.assertRaises(ValueError) as context:
            cart.remove_from_cart(101)

        self.assertIn("Product not found in cart", str(context.exception))
        mock_get_cart_item.assert_called_once_with(101)

    @patch('app.models.cart.execute_query')
    def test_clear_cart(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن السلة وتفريغها
        cart = Cart(1)
        cart.clear_cart()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لحذف جميع عناصر السلة
        self.assertIn("DELETE FROM Cart WHERE UserID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

    @patch('app.models.cart.execute_query')
    def test_get_cart_item(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [{
            "CartID": 1,
            "UserID": 1,
            "ProductID": 101,
            "Quantity": 2
        }]

        # إنشاء كائن السلة والحصول على عنصر
        cart = Cart(1)
        item = cart.get_cart_item(101)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للبحث عن عنصر في السلة
        self.assertIn("SELECT * FROM Cart WHERE UserID = ? AND ProductID = ?", call_args[0])
        self.assertEqual(call_args[1], (1, 101))

        # التحقق من النتيجة
        self.assertEqual(item["ProductID"], 101)
        self.assertEqual(item["Quantity"], 2)

    @patch('app.models.cart.execute_query')
    def test_get_cart_item_not_found(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام لعنصر غير موجود
        mock_execute_query.return_value = []

        # إنشاء كائن السلة والحصول على عنصر غير موجود
        cart = Cart(1)
        item = cart.get_cart_item(999)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()

        # التحقق من النتيجة
        self.assertIsNone(item)

    @patch('app.models.cart.execute_query')
    def test_get_cart_items(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [
            {
                "CartID": 1,
                "UserID": 1,
                "ProductID": 101,
                "Quantity": 2,
                "Name": "Chair",
                "Price": 100,
                "ImageURL": "/images/chair.jpg",
                "FurnitureType": "Chair",
                "CategoryID": 1
            },
            {
                "CartID": 2,
                "UserID": 1,
                "ProductID": 102,
                "Quantity": 1,
                "Name": "Table",
                "Price": 300,
                "ImageURL": "/images/table.jpg",
                "FurnitureType": "Table",
                "CategoryID": 2
            }
        ]

        # إنشاء كائن السلة والحصول على جميع العناصر
        cart = Cart(1)
        items = cart.get_cart_items()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للحصول على جميع عناصر السلة مع تفاصيل المنتج
        self.assertIn("SELECT c.*, p.Name, p.Price, p.ImageURL, p.FurnitureType, p.CategoryID", call_args[0])
        self.assertEqual(call_args[1], (1,))

        # التحقق من النتيجة
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["ProductID"], 101)
        self.assertEqual(items[1]["ProductID"], 102)
        self.assertEqual(items[0]["Name"], "Chair")
        self.assertEqual(items[1]["Name"], "Table")
        self.assertEqual(items[0]["Quantity"], 2)
        self.assertEqual(items[1]["Quantity"], 1)

    @patch('app.models.cart.execute_query')
    def test_get_cart_items_empty(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام لسلة فارغة
        mock_execute_query.return_value = []

        # إنشاء كائن السلة والحصول على جميع العناصر
        cart = Cart(1)
        items = cart.get_cart_items()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()

        # التحقق من النتيجة
        self.assertEqual(items, [])

    @patch('app.models.cart.Cart.get_cart_items')
    def test_calculate_total(self, mock_get_cart_items):
        # محاكاة نتيجة الحصول على عناصر السلة
        mock_get_cart_items.return_value = [
            {"Price": 100, "Quantity": 2},
            {"Price": 300, "Quantity": 1}
        ]

        # إنشاء كائن السلة وحساب المبلغ الإجمالي
        cart = Cart(1)
        total = cart.calculate_total()

        # التحقق من استدعاء get_cart_items
        mock_get_cart_items.assert_called_once()

        # التحقق من النتيجة (2*100 + 1*300 = 500)
        self.assertEqual(total, 500)

    @patch('app.models.cart.Cart.get_cart_items')
    def test_calculate_total_empty_cart(self, mock_get_cart_items):
        # محاكاة نتيجة الحصول على عناصر السلة الفارغة
        mock_get_cart_items.return_value = []

        # إنشاء كائن السلة وحساب المبلغ الإجمالي
        cart = Cart(1)
        total = cart.calculate_total()

        # التحقق من استدعاء get_cart_items
        mock_get_cart_items.assert_called_once()

        # التحقق من النتيجة
        self.assertEqual(total, 0)

if __name__ == '__main__':
    unittest.main()
