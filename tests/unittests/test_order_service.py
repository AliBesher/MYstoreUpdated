import unittest
from app.services.order_service import OrderService
from app.models import Order, OrderItem
from unittest.mock import patch, MagicMock

class TestOrderService(unittest.TestCase):

    @patch('app.services.order_service.CartService.get_cart_items')
    @patch('app.services.order_service.Order.add_order')
    @patch('app.services.order_service.OrderItem.add_order_item')
    @patch('app.services.order_service.Furniture.update_stock')
    @patch('app.services.order_service.CartService.clear_cart')
    @patch('app.services.order_service.OrderSubject.notify')
    def test_create_order_success(self, mock_notify, mock_clear_cart, mock_update_stock,
                                 mock_add_order_item, mock_add_order, mock_get_cart_items):
        # Mock the cart items
        mock_get_cart_items.return_value = [
            {"ProductID": 1, "Quantity": 2, "Price": 100},
            {"ProductID": 2, "Quantity": 1, "Price": 200}
        ]

        # Mock the add_order method
        mock_add_order.return_value = 1

        # Mock the add_order_item method
        mock_add_order_item.return_value = None

        # Mock the update_stock method
        mock_update_stock.return_value = None

        # Mock the clear_cart method
        mock_clear_cart.return_value = None

        # Mock notify
        mock_notify.return_value = None

        # Test creating an order
        result = OrderService.create_order(user_id=1)
        self.assertEqual(result, "✅ Order completed successfully. Total amount: 400.")

        # Verify all mocks were called with correct parameters
        mock_get_cart_items.assert_called_once_with(1)
        mock_add_order.assert_called_once()
        self.assertEqual(mock_add_order_item.call_count, 2)
        self.assertEqual(mock_update_stock.call_count, 2)
        mock_clear_cart.assert_called_once_with(1)
        mock_notify.assert_called_once_with(1, 1, 400, "pending")

    @patch('app.services.order_service.CartService.get_cart_items')
    def test_create_order_empty_cart(self, mock_get_cart_items):
        # Mock empty cart
        mock_get_cart_items.return_value = []

        # Test creating an order with empty cart
        result = OrderService.create_order(user_id=1)
        self.assertEqual(result, "⚠️ No items in the cart.")

    @patch('app.services.order_service.Order.add_order')
    @patch('app.services.order_service.CartService.get_cart_items')
    def test_create_order_failed(self, mock_get_cart_items, mock_add_order):
        # Mock the cart items
        mock_get_cart_items.return_value = [
            {"ProductID": 1, "Quantity": 2, "Price": 100}
        ]

        # Mock order creation failure
        mock_add_order.return_value = None

        # Test creating an order that fails
        result = OrderService.create_order(user_id=1)
        self.assertEqual(result, "⚠️ Failed to create order.")

    @patch('app.services.order_service.Order.get_order_by_id')
    @patch('app.services.order_service.Order.update_order_status')
    @patch('app.services.order_service.OrderSubject.notify')
    def test_update_order_status_success(self, mock_notify, mock_update_status, mock_get_order):
        # Mock getting order
        mock_get_order.return_value = {
            "OrderID": 1,
            "UserID": 1,
            "TotalAmount": 400,
            "Status": "pending"
        }

        # Mock updating status
        mock_update_status.return_value = None

        # Mock notify
        mock_notify.return_value = None

        # Test updating order status
        result = OrderService.update_order_status(order_id=1, status="shipped")
        self.assertEqual(result, "Order #1 status updated to shipped.")

        # Verify mocks were called correctly
        mock_get_order.assert_called_with(1)
        mock_update_status.assert_called_once_with(1, "shipped")
        mock_notify.assert_called_once_with(1, 1, 400, "shipped")

    @patch('app.services.order_service.Order.get_order_by_id')
    def test_update_order_status_not_found(self, mock_get_order):
        # Mock order not found
        mock_get_order.return_value = None

        # Test updating non-existent order
        result = OrderService.update_order_status(order_id=999, status="shipped")
        self.assertEqual(result, "⚠️ Order #999 not found.")

    @patch('app.services.order_service.Order.get_order_by_id')
    def test_update_order_status_invalid(self, mock_get_order):
        # Mock getting order
        mock_get_order.return_value = {
            "OrderID": 1,
            "UserID": 1,
            "TotalAmount": 400,
            "Status": "pending"
        }

        # Test updating with invalid status
        result = OrderService.update_order_status(order_id=1, status="invalid_status")
        self.assertTrue("⚠️ Invalid status" in result)

    @patch('app.services.order_service.Order.get_order_by_id')
    @patch('app.services.order_service.Order.delete_order')
    def test_delete_order_success(self, mock_delete, mock_get_order):
        # Mock getting order
        mock_get_order.return_value = {
            "OrderID": 1,
            "UserID": 1,
            "TotalAmount": 400,
            "Status": "pending"
        }

        # Mock deletion
        mock_delete.return_value = None

        # Test deleting an order
        result = OrderService.delete_order(order_id=1)
        self.assertEqual(result, "Order #1 deleted successfully.")

        # Verify mocks were called correctly
        mock_get_order.assert_called_once_with(1)
        mock_delete.assert_called_once()

    @patch('app.services.order_service.Order.get_order_by_id')
    def test_delete_order_not_found(self, mock_get_order):
        # Mock order not found
        mock_get_order.return_value = None

        # Test deleting non-existent order
        result = OrderService.delete_order(order_id=999)
        self.assertEqual(result, "⚠️ Order not found.")

    @patch('app.models.order.Order.get_orders_by_user')
    def test_get_orders_by_user(self, mock_get_orders):
        # Mock orders
        mock_get_orders.return_value = [
            {"OrderID": 1, "Status": "pending", "TotalAmount": 400},
            {"OrderID": 2, "Status": "shipped", "TotalAmount": 250}
        ]

        # Test getting user's orders
        result = OrderService.get_order_by_user(1)
        self.assertEqual(len(result), 2)
        mock_get_orders.assert_called_once_with(1)

    @patch('app.models.order.Order.get_order_by_id')
    def test_get_order_by_id(self, mock_get_order):
        # Mock order
        mock_get_order.return_value = {"OrderID": 1, "Status": "pending", "TotalAmount": 400}

        # Test getting order by ID
        result = OrderService.get_order_by_id(1)
        self.assertEqual(result["OrderID"], 1)
        mock_get_order.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
