import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.cart_service import CartService, PercentageDiscount
from app.services.checkout_service import CheckoutService
from app.services.order_service import OrderService
from app.models.furniture import Furniture

class TestCompletePurchaseFlow(unittest.TestCase):
    """
    Regression test covering the complete purchase flow:
    1. User login
    2. Add product to cart
    3. Apply discount to cart
    4. Checkout
    5. Process payment
    6. Update order status
    7. Verify inventory update
    """

    def setUp(self):
        """Set up the test environment."""
        # Create Flask app in test mode
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # Test user data
        self.test_user = {
            "id": 1,
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User",
            "role": "customer"
        }

        # Test product data
        self.test_product = {
            "id": 101,
            "name": "Test Chair",
            "description": "A comfortable test chair",
            "price": 199.99,
            "dimensions": "60x60x100",
            "stock_quantity": 10,
            "category_id": 1,
            "image_url": "/images/test-chair.jpg",
            "furniture_type": "Chair"
        }

    @patch('app.services.user_service.UserService.authenticate_user')
    def test_complete_purchase_flow(self, mock_authenticate):
        """Test the complete purchase flow from login to order completion."""
        # Step 1: User login
        print("\n1. Testing user login...")

        # Mock authentication service
        mock_authenticate.return_value = {
            "user": {
                "id": self.test_user["id"],
                "name": self.test_user["name"],
                "email": self.test_user["email"],
                "role": self.test_user["role"]
            },
            "token": "fake_token_12345"
        }

        # Send login request
        login_response = self.client.post('/api/login', json={
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        })

        # Verify login successful
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json["user"]["name"], self.test_user["name"])
        self.assertEqual(login_response.json["token"], "fake_token_12345")
        print("✅ Login successful")

        # Step 2: Add product to cart
        print("\n2. Testing adding product to cart...")
        with patch('app.services.cart_service.CartService.add_to_cart') as mock_add_to_cart:
            # Mock add to cart service
            mock_add_to_cart.return_value = "Product added to cart successfully."

            # Send add to cart request
            add_cart_response = self.client.post('/api/cart', json={
                "user_id": self.test_user["id"],
                "product_id": self.test_product["id"],
                "quantity": 2
            })

            # Verify product added to cart
            self.assertEqual(add_cart_response.status_code, 201)
            self.assertIn("Product added to cart successfully", add_cart_response.json["message"])
            print("✅ Product added to cart")

        # Step 3: Apply discount to cart
        print("\n3. Testing applying discount to cart...")
        with patch('app.services.cart_service.CartService.apply_discount') as mock_apply_discount:
            # Mock apply discount service
            mock_apply_discount.return_value = 20.0  # 10% of total price

            # Send apply discount request
            discount_response = self.client.post('/api/cart/discount', json={
                "user_id": self.test_user["id"],
                "discount_type": "percentage",
                "percentage": 10
            })

            # Verify discount applied
            self.assertEqual(discount_response.status_code, 200)
            self.assertEqual(discount_response.json["discount_amount"], 20.0)
            print("✅ Discount applied successfully")

        # Step 4: Checkout
        print("\n4. Testing checkout process...")
        with patch('app.services.checkout_service.CheckoutService.checkout') as mock_checkout:
            # Mock checkout service
            mock_checkout.return_value = "✅ Checkout completed successfully. Total amount: 380.0."

            # Send checkout request
            checkout_response = self.client.post('/api/checkout', json={
                "user_id": self.test_user["id"]
            })

            # Verify checkout successful
            self.assertEqual(checkout_response.status_code, 200)
            self.assertIn("Checkout completed successfully", checkout_response.json["message"])
            print("✅ Checkout completed")

        # Step 5: Process payment
        print("\n5. Testing payment processing...")
        with patch('app.services.checkout_service.CheckoutService.process_payment') as mock_process_payment:
            # Mock process payment service
            mock_process_payment.return_value = "✅ Payment processed successfully for order 1."

            # Assume order ID 1 was created during checkout
            order_id = 1

            # Send payment request
            payment_response = self.client.post('/api/checkout/payment', json={
                "order_id": order_id,
                "payment_method": "credit_card",
                "payment_details": {
                    "card_number": "**** **** **** 1234",
                    "expiry": "12/25",
                    "cvv": "***"
                }
            })

            # Verify payment successful
            self.assertEqual(payment_response.status_code, 200)
            self.assertIn("Payment processed successfully", payment_response.json["message"])
            print("✅ Payment processed")

        # Step 6: Update order status
        print("\n6. Testing order status update...")
        with patch('app.services.order_service.OrderService.update_order_status') as mock_update_status:
            # Mock update order status service
            mock_update_status.return_value = "Order #1 status updated to shipped."

            # Send update order status request
            status_response = self.client.put(f'/api/orders/{order_id}/status', json={
                "status": "shipped"
            })

            # Verify status updated
            self.assertEqual(status_response.status_code, 200)
            self.assertIn("status updated to shipped", status_response.json["message"])
            print("✅ Order status updated")

        # Step 7: Verify inventory update
        print("\n7. Verifying inventory update...")
        with patch('app.models.furniture.Furniture.update_stock') as mock_update_stock:
            # Mock update_stock to capture the call
            mock_update_stock.return_value = None

            # Create a trigger to simulate observer notification which updates inventory
            # (This would normally happen automatically via the Observer pattern)
            from app.services.checkout_service import OrderSubject, InventoryUpdate

            # Create and attach inventory observer
            inventory_observer = InventoryUpdate()
            OrderSubject.attach(inventory_observer)

            # Notify observers (simulating status change)
            OrderSubject.notify(order_id, self.test_user["id"], 380.0, "confirmed")

            # Verify inventory was updated
            mock_update_stock.assert_called()
            print("✅ Inventory updated")

        print("\n✅ Complete purchase flow test passed successfully")


if __name__ == '__main__':
    unittest.main()
