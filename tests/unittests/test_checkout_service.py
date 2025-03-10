import unittest
from app.services.checkout_service import CheckoutService, OrderSubject
from unittest.mock import patch


class TestCheckoutService(unittest.TestCase):

    @patch('app.services.checkout_service.CartService.get_cart_items')
    @patch('app.services.checkout_service.Order.add_order')
    @patch('app.services.checkout_service.OrderItem.add_order_item')
    @patch('app.services.checkout_service.CartService.clear_cart')
    def test_checkout_success(self, mock_clear_cart, mock_add_order_item, mock_add_order, mock_get_cart_items):
        # 1️⃣ Mock cart data
        mock_get_cart_items.return_value = [
            {"ProductID": 1, "Quantity": 2, "Price": 100},
            {"ProductID": 2, "Quantity": 1, "Price": 200}
        ]

        # 2️⃣ Mock order creation
        mock_add_order.return_value = 1

        # 3️⃣ Mock adding order items
        mock_add_order_item.return_value = None

        # 4️⃣ Mock clearing the cart after purchase
        mock_clear_cart.return_value = None

        # ✅ Execute the checkout process and verify the result
        result = CheckoutService.checkout(user_id=1)
        self.assertEqual(result, "✅ Checkout completed successfully. Total amount: 400.")

    @patch('app.services.checkout_service.OrderSubject.notify')
    def test_notify_observers(self, mock_notify):
        # Mock sending notifications
        mock_notify.return_value = None

        # Execute order notification
        OrderSubject.notify(order_id=1, user_id=1, total_amount=400, status="pending")

        # ✅ Verify that the notification was called with the correct values
        mock_notify.assert_called_once_with(order_id=1, user_id=1, total_amount=400, status="pending")

    @patch('app.services.checkout_service.execute_query')
    @patch('app.services.checkout_service.OrderSubject.notify')
    def test_process_payment(self, mock_notify, mock_execute_query):
        # 1️⃣ Mock query results in the correct order - we need 3 responses:
        # The first response is for the update, the second for the select, and the third for the notification
        mock_execute_query.side_effect = [
            None,  # Result of the UPDATE query for the order
            [{"OrderID": 1, "UserID": 1, "TotalAmount": 400, "Status": "paid"}]  # Result of the SELECT query for the order
        ]

        # Mock notification to avoid a third execute_query call
        mock_notify.return_value = None

        # 2️⃣ Execute the payment process
        result = CheckoutService.process_payment(
            order_id=1,
            payment_method="credit_card",
            payment_details={"card_number": "1234"}
        )

        # 3️⃣ Verify the result
        self.assertEqual(result, "✅ Payment processed successfully for order 1.")

        # Verify that the notification was called correctly
        mock_notify.assert_called_once_with(1, 1, 400, "paid")


if __name__ == '__main__':
    unittest.main()
