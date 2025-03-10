import unittest
from unittest.mock import patch
from app.services.cart_service import CartService, PercentageDiscount, BuyOneGetOneDiscount, BulkDiscount
from app.models import Cart
from decimal import Decimal


class TestCartService(unittest.TestCase):

    @patch('app.services.cart_service.Cart.add_to_cart')
    def test_add_to_cart(self, mock_add_to_cart):
        # Test successful addition
        mock_add_to_cart.return_value = None
        result = CartService.add_to_cart(user_id=1, product_id=1, quantity=2)
        self.assertEqual(result, "Product added to cart successfully.")

    def test_add_to_cart_invalid_quantity(self):
        # Test negative quantity
        with self.assertRaises(ValueError):
            CartService.add_to_cart(user_id=1, product_id=1, quantity=0)

        with self.assertRaises(ValueError):
            CartService.add_to_cart(user_id=1, product_id=1, quantity=-1)

    @patch('app.services.cart_service.Cart.update_cart')
    def test_update_cart(self, mock_update_cart):
        # Test successful update
        mock_update_cart.return_value = None
        result = CartService.update_cart(user_id=1, product_id=1, new_quantity=3)
        self.assertEqual(result, "Cart updated successfully.")

    def test_update_cart_invalid_quantity(self):
        # Test negative quantity
        with self.assertRaises(ValueError):
            CartService.update_cart(user_id=1, product_id=1, new_quantity=0)

        with self.assertRaises(ValueError):
            CartService.update_cart(user_id=1, product_id=1, new_quantity=-1)

    @patch('app.services.cart_service.Cart.get_cart_item')
    @patch('app.services.cart_service.Cart.remove_from_cart')
    def test_remove_from_cart(self, mock_remove_from_cart, mock_get_cart_item):
        # Test successful removal
        mock_get_cart_item.return_value = {"ProductID": 1, "Quantity": 2}
        mock_remove_from_cart.return_value = None
        result = CartService.remove_from_cart(user_id=1, product_id=1)
        self.assertEqual(result, "Product removed from cart successfully.")

    @patch('app.services.cart_service.Cart.get_cart_item')
    def test_remove_from_cart_not_found(self, mock_get_cart_item):
        # Test product not found in cart
        mock_get_cart_item.return_value = None
        with self.assertRaises(ValueError) as context:
            CartService.remove_from_cart(user_id=1, product_id=999)
        self.assertTrue("Product not found in cart" in str(context.exception))

    @patch('app.services.cart_service.Cart.clear_cart')
    def test_clear_cart(self, mock_clear_cart):
        # Test successful clear
        mock_clear_cart.return_value = None
        result = CartService.clear_cart(user_id=1)
        self.assertEqual(result, "Cart cleared successfully.")

    @patch('app.services.cart_service.Cart.get_cart_items')
    def test_get_cart_items(self, mock_get_cart_items):
        # Test getting cart items
        mock_get_cart_items.return_value = [
            {"ProductID": 1, "Quantity": 2, "Price": 100, "CategoryID": 1},
            {"ProductID": 2, "Quantity": 1, "Price": 200, "CategoryID": 2}
        ]
        result = CartService.get_cart_items(user_id=1)
        self.assertEqual(len(result), 2)

    @patch('app.services.cart_service.Cart.calculate_total')
    def test_calculate_cart_total(self, mock_calculate_total):
        # Test calculating cart total
        mock_calculate_total.return_value = 400
        result = CartService.calculate_cart_total(user_id=1)
        self.assertEqual(result, 400)

    def test_apply_discount_percentage(self):
        # Test percentage discount
        with patch('app.services.cart_service.CartService.get_cart_items') as mock_get_cart_items:
            mock_get_cart_items.return_value = [
                {"ProductID": 1, "Quantity": 2, "Price": 100, "CategoryID": 1},
                {"ProductID": 2, "Quantity": 1, "Price": 200, "CategoryID": 2}
            ]

            discount_strategy = PercentageDiscount(10)
            total_discount = CartService.apply_discount(user_id=1, discount_strategy=discount_strategy)
            self.assertEqual(float(total_discount), 40.0)  # 10% of 400

    def test_apply_discount_buy_one_get_one(self):
        # Test buy one get one discount
        with patch('app.services.cart_service.CartService.get_cart_items') as mock_get_cart_items:
            mock_get_cart_items.return_value = [
                {"ProductID": 1, "Quantity": 2, "Price": 100, "CategoryID": 1},
                {"ProductID": 2, "Quantity": 3, "Price": 200, "CategoryID": 2}
            ]

            discount_strategy = BuyOneGetOneDiscount(eligible_categories=[1, 2])
            total_discount = CartService.apply_discount(user_id=1, discount_strategy=discount_strategy)
            self.assertEqual(total_discount, 300)  # One free item per pair

    def test_apply_discount_bulk(self):
        # Test bulk discount
        with patch('app.services.cart_service.CartService.get_cart_items') as mock_get_cart_items:
            mock_get_cart_items.return_value = [
                {"ProductID": 1, "Quantity": 5, "Price": 100},
                {"ProductID": 2, "Quantity": 10, "Price": 50}
            ]

            discount_strategy = BulkDiscount(threshold=5, percentage=20)
            total_discount = CartService.apply_discount(user_id=1, discount_strategy=discount_strategy)
            self.assertEqual(total_discount, 200)  # 20% of total price for items with quantity >= 5

    def test_apply_discount_empty_cart(self):
        # Test discount on empty cart
        with patch('app.services.cart_service.CartService.get_cart_items') as mock_get_cart_items:
            mock_get_cart_items.return_value = []

            discount_strategy = PercentageDiscount(10)
            total_discount = CartService.apply_discount(user_id=1, discount_strategy=discount_strategy)
            self.assertEqual(total_discount, 0)


if __name__ == '__main__':
    unittest.main()
