import unittest
from unittest.mock import patch
from app import create_app
from app.services.cart_service import CartService

class TestCartRoutes(unittest.TestCase):

    def setUp(self):
        # Create Flask app in test mode
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    # --------------------------
    # Test adding item to cart
    # --------------------------
    @patch('app.services.cart_service.CartService.add_to_cart')
    def test_add_to_cart_success(self, mock_add):
        # Mock successful addition
        mock_add.return_value = "Product added to cart successfully."

        # Test data
        data = {
            "user_id": 1,
            "product_id": 101,
            "quantity": 2
        }

        # Send POST request
        response = self.client.post('/api/cart', json=data)

        # Verify results
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Product added to cart successfully", response.data)

    @patch('app.services.cart_service.CartService.add_to_cart')
    def test_add_to_cart_invalid_data(self, mock_add):
        # Mock invalid data
        mock_add.return_value = "⚠️ Invalid product data."

        # Incomplete data (missing product_id)
        data = {
            "user_id": 1,
            "quantity": 2
        }

        response = self.client.post('/api/cart', json=data)
        self.assertEqual(response.status_code, 400)

    # -------------------------------
    # Test updating cart item quantity
    # -------------------------------
    @patch('app.services.cart_service.CartService.update_cart')
    def test_update_cart_success(self, mock_update):
        # Mock successful update
        mock_update.return_value = "Cart updated successfully."

        data = {
            "user_id": 1,
            "quantity": 5
        }

        response = self.client.put('/api/cart/101', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cart updated successfully", response.data)

    def test_update_cart_invalid_quantity(self):
        # Test invalid quantity (negative)
        data = {
            "user_id": 1,
            "quantity": -3
        }

        response = self.client.put('/api/cart/101', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Quantity must be positive", response.data)

    # --------------------------
    # Test removing item from cart
    # --------------------------
    @patch('app.services.cart_service.CartService.remove_from_cart')
    def test_remove_item_success(self, mock_remove):
        # Mock successful removal
        mock_remove.return_value = "Product removed from cart successfully."

        data = {"user_id": 1}

        response = self.client.delete('/api/cart/101', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product removed from cart successfully", response.data)

    @patch('app.services.cart_service.CartService.remove_from_cart')
    def test_remove_item_not_found(self, mock_remove):
        # Mock item not found and raise an exception
        mock_remove.side_effect = ValueError("⚠️ Product not found in cart.")

        data = {"user_id": 1}

        response = self.client.delete('/api/cart/999', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Product not found in cart", response.data)

    # ----------------------
    # Test clearing cart
    # ----------------------
    @patch('app.services.cart_service.CartService.clear_cart')
    def test_clear_cart_success(self, mock_clear):
        # Mock successful clearing
        mock_clear.return_value = "Cart cleared successfully."

        data = {"user_id": 1}

        response = self.client.post('/api/cart/clear', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cart cleared successfully", response.data)

    # ----------------------
    # Test viewing cart contents
    # ----------------------
    @patch('app.services.cart_service.CartService.get_cart_items')
    @patch('app.services.cart_service.CartService.calculate_cart_total')
    def test_view_cart_with_items(self, mock_total, mock_get):
        # Mock cart with items
        mock_get.return_value = [
            {"ProductID": 101, "Name": "Chair", "Price": 150, "Quantity": 2},
            {"ProductID": 102, "Name": "Table", "Price": 300, "Quantity": 1}
        ]
        mock_total.return_value = 600

        response = self.client.get('/api/cart?user_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['cart_items']), 2)
        self.assertEqual(response.json['cart_total'], 600)

    @patch('app.services.cart_service.CartService.get_cart_items')
    def test_view_empty_cart(self, mock_get):
        # Mock empty cart
        mock_get.return_value = []

        response = self.client.get('/api/cart?user_id=1')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"No items in the cart", response.data)

if __name__ == '__main__':
    unittest.main()
