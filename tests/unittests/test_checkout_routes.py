import unittest
from app import create_app

class TestCheckoutRoutes(unittest.TestCase):

    def setUp(self):
        # إعداد التطبيق والعميل للاختبارات
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def test_checkout(self):
        # Step 1: Add items to the cart
        self.client.post('/api/cart', json={"user_id": 1, "product_id": 1, "quantity": 2})
        self.client.post('/api/cart', json={"user_id": 1, "product_id": 2, "quantity": 1})

        # Step 2: Send checkout request
        response = self.client.post('/api/checkout', json={"user_id": 1})

        # Debugging: طباعة حالة الاستجابة والبيانات المسترجعة
        print(f"Response Status: {response.status_code}")
        print(f"Response Data: {response.get_json()}")

        # Assertions: التحقق من أن الحالة هي 200 وأن الرسالة تحتوي على "Checkout completed successfully"
        self.assertEqual(response.status_code, 200)
        self.assertIn("Checkout completed successfully", response.get_json().get("message", ""))

    def test_process_payment(self):
        # إرسال بيانات الدفع
        data = {
            "order_id": 1,
            "payment_method": "credit_card",
            "payment_details": {"card_number": "1234"}
        }
        response = self.client.post('/api/checkout/payment', json=data)

        # التحقق من أن الطلب تم بنجاح
        self.assertEqual(response.status_code, 200)
        self.assertIn("Payment processed successfully", response.get_json().get("message", ""))

if __name__ == '__main__':
    unittest.main()
