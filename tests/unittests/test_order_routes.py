import unittest
from unittest.mock import patch
from app import create_app
from app.services.order_service import OrderService

class TestOrderRoutes(unittest.TestCase):

    def setUp(self):
        # Create Flask app in test mode
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    # --------------------------
    # Test creating an order
    # --------------------------
    @patch('app.services.order_service.OrderService.create_order')
    def test_create_order_success(self, mock_create_order):
        # Mock successful order creation
        mock_create_order.return_value = "✅ Order completed successfully. Total amount: 500."

        # Test data
        data = {"user_id": 1}

        # Send POST request
        response = self.client.post('/api/orders', json=data)

        # Verify results
        self.assertEqual(response.status_code, 201)
        self.assertIn("Order completed successfully", response.json["message"])
        mock_create_order.assert_called_once_with(1)

    @patch('app.services.order_service.OrderService.create_order')
    def test_create_order_empty_cart(self, mock_create_order):
        # Mock empty cart error
        mock_create_order.return_value = "⚠️ No items in the cart."

        # Test data
        data = {"user_id": 1}

        # Send POST request
        response = self.client.post('/api/orders', json=data)

        # Verify results
        self.assertEqual(response.status_code, 400)
        self.assertIn("No items in the cart", response.json["message"])

    # --------------------------
    # Test updating order status
    # --------------------------
    @patch('app.services.order_service.OrderService.update_order_status')
    def test_update_order_status(self, mock_update_status):
        # Mock successful status update
        mock_update_status.return_value = "Order #1 status updated to shipped."

        # Test data
        data = {"status": "shipped"}

        # Send PUT request
        response = self.client.put('/api/orders/1/status', json=data)

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertIn("status updated to shipped", response.json["message"])
        mock_update_status.assert_called_once_with(1, "shipped")

    # --------------------------
    # Test deleting an order
    # --------------------------
    @patch('app.services.order_service.OrderService.delete_order')
    def test_delete_order(self, mock_delete_order):
        # Mock successful order deletion
        mock_delete_order.return_value = "Order #1 deleted successfully."

        # Send DELETE request
        response = self.client.delete('/api/orders/1')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.json["message"])
        mock_delete_order.assert_called_once_with(1)

    # --------------------------
    # Test viewing user's orders
    # --------------------------
    @patch('app.services.order_service.OrderService.get_order_by_user')
    def test_view_orders_success(self, mock_get_orders):
        # Mock orders list
        mock_orders = [
            {"OrderID": 1, "TotalAmount": 200, "Status": "pending"},
            {"OrderID": 2, "TotalAmount": 350, "Status": "shipped"}
        ]
        mock_get_orders.return_value = mock_orders

        # Send GET request
        response = self.client.get('/api/orders?user_id=1')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["orders"]), 2)
        mock_get_orders.assert_called_once_with("1")  # user_id as string from query

    @patch('app.services.order_service.OrderService.get_order_by_user')
    def test_view_orders_none_found(self, mock_get_orders):
        # Mock no orders found
        mock_get_orders.return_value = []

        # Send GET request
        response = self.client.get('/api/orders?user_id=1')

        # Verify results
        self.assertEqual(response.status_code, 404)
        self.assertIn("No orders found", response.json["message"])

    # --------------------------
    # Test getting order details
    # --------------------------
    @patch('app.services.order_service.OrderService.get_order_by_id')
    @patch('app.models.order.Order.get_order_items')
    def test_get_order_details_success(self, mock_get_items, mock_get_order):
        # Mock order details
        mock_get_order.return_value = {
            "OrderID": 1,
            "UserID": 1,
            "TotalAmount": 500,
            "Status": "shipped",
            "CreatedAt": "2023-04-01"
        }

        # Mock order items
        mock_get_items.return_value = [
            {"OrderItemID": 1, "ProductID": 101, "Quantity": 2, "Price": 150},
            {"OrderItemID": 2, "ProductID": 102, "Quantity": 1, "Price": 200}
        ]

        # Send GET request
        response = self.client.get('/api/orders/1')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["order"]["OrderID"], 1)
        self.assertEqual(len(response.json["items"]), 2)
        mock_get_order.assert_called_once_with(1)

    @patch('app.services.order_service.OrderService.get_order_by_id')
    def test_get_order_details_not_found(self, mock_get_order):
        # Mock order not found
        mock_get_order.return_value = None

        # Send GET request
        response = self.client.get('/api/orders/999')

        # Verify results
        self.assertEqual(response.status_code, 404)
        self.assertIn("Order not found", response.json["message"])

if __name__ == '__main__':
    unittest.main()
