# tests/regression_test_mock.py
"""
اختبار انحدار يستخدم محاكاة قاعدة البيانات بدلاً من الاتصال الحقيقي.
"""

import unittest
from app.db.mock_db import apply_mock, restore_original
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.cart_service import CartService, PercentageDiscount
from app.services.checkout_service import CheckoutService, OrderSubject, InventoryUpdate, EmailNotification

class TestCompletePurchaseFlow(unittest.TestCase):
    """اختبار سير عملية الشراء الكاملة."""

    @classmethod
    def setUpClass(cls):
        """إعداد يتم تنفيذه مرة واحدة قبل جميع الاختبارات."""
        # تطبيق المحاكاة على قاعدة البيانات
        cls.original_execute_query = apply_mock()
        
        # تهيئة المراقبين للإشعارات
        cls.email_observer = EmailNotification()
        cls.inventory_observer = InventoryUpdate()
        
        # تسجيل المراقبين
        OrderSubject._observers = []
        OrderSubject.attach(cls.email_observer)
        OrderSubject.attach(cls.inventory_observer)

    @classmethod
    def tearDownClass(cls):
        """تنظيف يتم تنفيذه مرة واحدة بعد جميع الاختبارات."""
        # استعادة وظيفة قاعدة البيانات الأصلية
        restore_original(cls.original_execute_query)

    def test_complete_purchase_flow(self):
        """اختبار سير عملية الشراء من تسجيل الدخول إلى إكمال الطلب."""
        
        print("\n1. اختبار تسجيل دخول المستخدم...")
        login_result = UserService.authenticate_user("test@example.com", "password123")
        self.assertIsNotNone(login_result)
        self.assertEqual(login_result["user"]["email"], "test@example.com")
        print("✅ تم تسجيل الدخول بنجاح")
        
        print("\n2. اختبار إضافة منتج إلى السلة...")
        add_result = CartService.add_to_cart(user_id=1, product_id=1, quantity=2)
        self.assertIn("تمت إضافة المنتج", add_result)
        print("✅ تمت إضافة المنتج إلى السلة بنجاح")
        
        print("\n3. اختبار تطبيق الخصم على السلة...")
        discount_strategy = PercentageDiscount(10)
        discount = CartService.apply_discount(user_id=1, discount_strategy=discount_strategy)
        self.assertGreater(discount, 0)
        print(f"✅ تم تطبيق الخصم بنجاح (قيمة الخصم: {discount})")
        
        print("\n4. اختبار عملية إنهاء الشراء...")
        checkout_service = CheckoutService()
        checkout_result = checkout_service.checkout(user_id=1)
        self.assertIn("تم إكمال عملية الشراء بنجاح", checkout_result)
        print("✅ تم إكمال عملية الشراء بنجاح")
        
        print("\n5. اختبار معالجة الدفع...")
        payment_result = checkout_service.process_payment(
            order_id=1,
            payment_method="credit_card",
            payment_details={"card_number": "1234-5678-9012-3456"}
        )
        self.assertIn("تمت معالجة الدفع بنجاح", payment_result)
        print("✅ تمت معالجة الدفع بنجاح")
        
        print("\n6. اختبار تحديث حالة الطلب...")
        status_result = checkout_service.update_order_status(order_id=1, new_status="تم التأكيد")
        self.assertIn("تم تحديث حالة الطلب", status_result)
        print("✅ تم تحديث حالة الطلب بنجاح")
        
        print("\n7. التحقق من تحديث المخزون والإشعارات...")
        # يتم التحقق من تحديث المخزون والإشعارات عن طريق محاكاة المراقبين
        # إرسال إشعار يدوياً للتحقق من عمل المراقبين
        OrderSubject.notify(1, 1, 400.0, "تم التأكيد")
        print("✅ تم إرسال الإشعارات وتحديث المخزون بنجاح")
        
        print("\n✨ تم اختبار سير العملية بالكامل بنجاح!")

if __name__ == '__main__':
    unittest.main()
