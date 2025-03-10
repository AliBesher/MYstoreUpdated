import unittest
from app.services.checkout_service import CheckoutService, OrderSubject
from unittest.mock import patch


class TestCheckoutService(unittest.TestCase):

    @patch('app.services.checkout_service.CartService.get_cart_items')
    @patch('app.services.checkout_service.Order.add_order')
    @patch('app.services.checkout_service.OrderItem.add_order_item')
    @patch('app.services.checkout_service.CartService.clear_cart')
    def test_checkout_success(self, mock_clear_cart, mock_add_order_item, mock_add_order, mock_get_cart_items):
        # 1️⃣ محاكاة بيانات السلة
        mock_get_cart_items.return_value = [
            {"ProductID": 1, "Quantity": 2, "Price": 100},
            {"ProductID": 2, "Quantity": 1, "Price": 200}
        ]

        # 2️⃣ محاكاة إنشاء الطلب
        mock_add_order.return_value = 1

        # 3️⃣ محاكاة إضافة عناصر الطلب
        mock_add_order_item.return_value = None

        # 4️⃣ محاكاة مسح السلة بعد الشراء
        mock_clear_cart.return_value = None

        # ✅ تنفيذ عملية الدفع والتحقق من النتيجة
        result = CheckoutService.checkout(user_id=1)
        self.assertEqual(result, "✅ Checkout completed successfully. Total amount: 400.")

    @patch('app.services.checkout_service.OrderSubject.notify')
    def test_notify_observers(self, mock_notify):
        # محاكاة إرسال الإشعارات
        mock_notify.return_value = None

        # تنفيذ إشعار الطلب
        OrderSubject.notify(order_id=1, user_id=1, total_amount=400, status="pending")

        # ✅ التحقق من أن الإشعار استُدعي بالقيم الصحيحة
        mock_notify.assert_called_once_with(order_id=1, user_id=1, total_amount=400, status="pending")

    @patch('app.services.checkout_service.execute_query')
    @patch('app.services.checkout_service.OrderSubject.notify')
    def test_process_payment(self, mock_notify, mock_execute_query):
        # 1️⃣ محاكاة نتائج الاستعلامات بالترتيب الصحيح - نحتاج إلى 3 استجابات:
        # الاستجابة الأولى للتحديث، الثانية للاستعلام، والثالثة للإشعار
        mock_execute_query.side_effect = [
            None,  # نتيجة استعلام UPDATE للطلب
            [{"OrderID": 1, "UserID": 1, "TotalAmount": 400, "Status": "paid"}]  # نتيجة استعلام SELECT للطلب
        ]

        # محاكاة الإشعار لتجنب استدعاء execute_query الثالث
        mock_notify.return_value = None

        # 2️⃣ تنفيذ عملية الدفع
        result = CheckoutService.process_payment(
            order_id=1,
            payment_method="credit_card",
            payment_details={"card_number": "1234"}
        )

        # 3️⃣ التحقق من النتيجة
        self.assertEqual(result, "✅ Payment processed successfully for order 1.")

        # التحقق من أن الإشعار تم استدعاؤه بالشكل الصحيح
        mock_notify.assert_called_once_with(1, 1, 400, "paid")


if __name__ == '__main__':
    unittest.main()
