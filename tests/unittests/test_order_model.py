import unittest
from unittest.mock import patch, MagicMock
from app.models.order import Order

class TestOrderModel(unittest.TestCase):

    @patch('app.models.order.execute_query')
    def test_add_order_success(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام مع معرف الطلب المدرج
        mock_execute_query.return_value = [(1,)]

        # إنشاء كائن الطلب وإضافته
        order = Order(1, 500, "pending")
        order_id = order.add_order()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لإدراج طلب جديد
        self.assertIn("INSERT INTO Orders", call_args[0])

        # التحقق من أن معلمات الاستعلام تحتوي على بيانات الطلب
        params = call_args[1]
        self.assertEqual(params[0], 1)  # معرف المستخدم
        self.assertEqual(params[1], 500)  # المبلغ الإجمالي
        self.assertEqual(params[2], "pending")  # الحالة

        # التحقق من النتيجة
        self.assertEqual(order_id, 1)

    @patch('app.models.order.execute_query')
    def test_add_order_no_result(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام بدون أي نتائج
        mock_execute_query.return_value = []

        # إنشاء كائن الطلب وإضافته
        order = Order(1, 500, "pending")
        order_id = order.add_order()

        # التحقق من استدعاء execute_query
        mock_execute_query.assert_called_once()

        # التحقق من النتيجة
        self.assertIsNone(order_id)

    @patch('app.models.order.execute_query')
    def test_update_order(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن الطلب وتحديثه
        order = Order(1, 600, "shipped")
        order.update_order(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لتحديث طلب
        self.assertIn("UPDATE Orders", call_args[0])

        # التحقق من أن معلمات الاستعلام تحتوي على بيانات الطلب المحدثة
        params = call_args[1]
        self.assertEqual(params[0], "shipped")  # الحالة
        self.assertEqual(params[1], 600)  # المبلغ الإجمالي
        self.assertEqual(params[2], 1)  # معرف الطلب

    @patch('app.models.order.execute_query')
    def test_delete_order(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن الطلب وحذفه
        order = Order(1, 500, "pending")
        order.delete_order(1)

        # التحقق من أن execute_query تم استدعاؤها مرتين (مرة لحذف العناصر ومرة لحذف الطلب)
        self.assertEqual(mock_execute_query.call_count, 2)

        # التحقق من الاستدعاء الأول (حذف عناصر الطلب)
        first_call_args = mock_execute_query.call_args_list[0][0]
        self.assertIn("DELETE FROM OrderItems WHERE OrderID = ?", first_call_args[0])
        self.assertEqual(first_call_args[1], (1,))

        # التحقق من الاستدعاء الثاني (حذف الطلب)
        second_call_args = mock_execute_query.call_args_list[1][0]
        self.assertIn("DELETE FROM Orders WHERE OrderID = ?", second_call_args[0])
        self.assertEqual(second_call_args[1], (1,))

    @patch('app.models.order.execute_query')
    def test_get_order_by_id(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [{
            "OrderID": 1,
            "UserID": 1,
            "TotalAmount": 500,
            "Status": "pending",
            "UserName": "Test User",
            "UserEmail": "test@example.com"
        }]

        # استدعاء دالة الحصول على الطلب بواسطة المعرف
        order = Order.get_order_by_id(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للبحث عن طلب
        self.assertIn("SELECT o.*, u.Name as UserName, u.Email as UserEmail", call_args[0])
        self.assertEqual(call_args[1], (1,))

        # التحقق من النتيجة
        self.assertEqual(order["OrderID"], 1)
        self.assertEqual(order["TotalAmount"], 500)
        self.assertEqual(order["Status"], "pending")
        self.assertEqual(order["UserName"], "Test User")

    @patch('app.models.order.execute_query')
    def test_get_order_by_id_not_found(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام لطلب غير موجود
        mock_execute_query.return_value = []

        # استدعاء دالة الحصول على الطلب بواسطة المعرف
        order = Order.get_order_by_id(999)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()

        # التحقق من النتيجة
        self.assertIsNone(order)

    @patch('app.models.order.execute_query')
    def test_get_order_items(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [
            {
                "OrderItemID": 1,
                "OrderID": 1,
                "ProductID": 101,
                "Quantity": 2,
                "Price": 100,
                "ProductName": "Chair",
                "ProductImage": "/images/chair.jpg",
                "FurnitureType": "Chair"
            },
            {
                "OrderItemID": 2,
                "OrderID": 1,
                "ProductID": 102,
                "Quantity": 1,
                "Price": 300,
                "ProductName": "Table",
                "ProductImage": "/images/table.jpg",
                "FurnitureType": "Table"
            }
        ]

        # استدعاء دالة الحصول على عناصر الطلب
        items = Order.get_order_items(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للحصول على عناصر الطلب
        self.assertIn("SELECT oi.*, p.Name as ProductName, p.ImageURL as ProductImage", call_args[0])
        self.assertEqual(call_args[1], (1,))

        # التحقق من النتيجة
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["ProductName"], "Chair")
        self.assertEqual(items[1]["ProductName"], "Table")
        self.assertEqual(items[0]["Quantity"], 2)
        self.assertEqual(items[1]["Quantity"], 1)

    @patch('app.models.order.execute_query')
    def test_get_orders_by_user(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [
            {
                "OrderID": 1,
                "UserID": 1,
                "TotalAmount": 500,
                "Status": "pending",
                "ItemCount": 3
            },
            {
                "OrderID": 2,
                "UserID": 1,
                "TotalAmount": 300,
                "Status": "shipped",
                "ItemCount": 2
            }
        ]

        # استدعاء دالة الحصول على طلبات المستخدم
        orders = Order.get_orders_by_user(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للحصول على طلبات المستخدم
        self.assertIn("SELECT o.*, COUNT(oi.OrderItemID) as ItemCount", call_args[0])
        self.assertEqual(call_args[1], (1,))

        # التحقق من النتيجة
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]["OrderID"], 1)
        self.assertEqual(orders[1]["OrderID"], 2)
        self.assertEqual(orders[0]["TotalAmount"], 500)
        self.assertEqual(orders[1]["TotalAmount"], 300)
        self.assertEqual(orders[0]["ItemCount"], 3)
        self.assertEqual(orders[1]["ItemCount"], 2)

    @patch('app.models.order.execute_query')
    def test_get_orders_by_status(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [
            {
                "OrderID": 1,
                "UserID": 1,
                "TotalAmount": 500,
                "Status": "pending",
                "UserName": "User 1"
            },
            {
                "OrderID": 3,
                "UserID": 2,
                "TotalAmount": 700,
                "Status": "pending",
                "UserName": "User 2"
            }
        ]

        # استدعاء دالة الحصول على الطلبات حسب الحالة
        orders = Order.get_orders_by_status("pending")

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو للحصول على الطلبات حسب الحالة
        self.assertIn("SELECT o.*, u.Name as UserName", call_args[0])
        self.assertEqual(call_args[1], ("pending",))

        # التحقق من النتيجة
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]["OrderID"], 1)
        self.assertEqual(orders[1]["OrderID"], 3)
        self.assertEqual(orders[0]["Status"], "pending")
        self.assertEqual(orders[1]["Status"], "pending")
        self.assertEqual(orders[0]["UserName"], "User 1")
        self.assertEqual(orders[1]["UserName"], "User 2")

    @patch('app.models.order.execute_query')
    def test_update_order_status(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلامات المتعددة
        mock_execute_query.side_effect = [
            None,  # نتيجة استعلام UPDATE
            [{"OrderID": 1, "UserID": 1, "TotalAmount": 400}]  # نتيجة استعلام SELECT
        ]

        # استدعاء دالة تحديث حالة الطلب
        Order.update_order_status(1, "shipped")

        # التحقق من أن execute_query تم استدعاؤه مرتين
        self.assertEqual(mock_execute_query.call_count, 2)

        # التحقق من الاستدعاء الأول (تحديث حالة الطلب)
        first_call_args = mock_execute_query.call_args_list[0][0]
        self.assertIn("UPDATE Orders", first_call_args[0])
        self.assertEqual(first_call_args[1], ("shipped", 1))

if __name__ == '__main__':
    unittest.main()
