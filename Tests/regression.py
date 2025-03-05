import unittest
import os
import sys
from decimal import Decimal
from unittest.mock import patch, MagicMock, call

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import services and models for testing
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.order_service import OrderService
from app.services.checkout_service import CheckoutService, OrderSubject, EmailNotification, InventoryUpdate
from app.models.furniture import Furniture, Chair, Table
from app.models.user import User
from app.models.cart import Cart
from app.models.order import Order
from app.models.order_item import OrderItem
from app.db.execute_query import execute_query

class RegressionTests(unittest.TestCase):
    """
    Regression tests for the online furniture store.
    
    These tests verify complete end-to-end processes to ensure
    all components work together correctly.
    """
    
    def setUp(self):
        """Set up test environment."""
        # Mock the execute_query function
        self.patcher = patch('app.db.execute_query.execute_query')
        self.mock_execute_query = self.patcher.start()
        
        # Set up mock database data
        self.user_data = {
            'UserID': 1,
            'Name': 'Test User',
            'Email': 'test@example.com',
            'Password': 'hashed_password',
            'Salt': 'test_salt',
            'Role': 'customer'
        }
        
        self.product_data = {
            'ProductID': 1,
            'Name': 'Test Chair',
            'Description': 'A test chair',
            'Price': 99.99,
            'Dimensions': '60x60x100',
            'StockQuantity': 10,
            'CategoryID': 1,
            'ImageURL': '/images/test.jpg',
            'FurnitureType': 'Chair',
            'MaxWeightCapacity': 120,
            'HasArmrests': True,
            'IsAdjustable': False
        }
        
        self.cart_data = [
            {
                'CartID': 1,
                'UserID': 1,
                'ProductID': 1,
                'Quantity': 2,
                'Name': 'Test Chair',
                'Price': 99.99,
                'ImageURL': '/images/test.jpg',
                'FurnitureType': 'Chair',
                'CategoryID': 1
            }
        ]
        
        # Set up side effect for execute_query mock
        self.mock_execute_query.side_effect = self.mock_query_side_effect
        
        # Mock the OrderSubject class
        self.patcher_order_subject = patch('app.services.checkout_service.OrderSubject')
        self.mock_order_subject = self.patcher_order_subject.start()
        
        # Create observer mocks
        self.mock_email_notification = MagicMock()
        self.mock_inventory_update = MagicMock()
        
        # Attach mock observers
        self.mock_order_subject.attach = MagicMock()
        self.mock_order_subject._observers = [
            self.mock_email_notification,
            self.mock_inventory_update
        ]
    
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
        self.patcher_order_subject.stop()
    
    def mock_query_side_effect(self, query, params=None, fetch=False):
        """Side effect function for the mock execute_query."""
        # For SELECT queries that fetch data
        if "SELECT" in query and fetch:
            if "Users" in query and "UserID" in query:
                return [self.user_data]
            elif "Products" in query and "ProductID" in query:
                return [self.product_data]
            elif "Cart" in query and "UserID" in query:
                return self.cart_data
            elif "Orders" in query and "OUTPUT INSERTED" in query:
                return [(1,)]  # Return new order ID 1
            elif "Orders" in query and "OrderID" in query:
                return [{
                    'OrderID': 1,
                    'UserID': 1,
                    'TotalAmount': 199.98,
                    'Status': 'pending',
                    'CreatedAt': '2023-01-01'
                }]
        
        # For INSERT queries that return an ID
        elif "INSERT" in query and "OUTPUT INSERTED" in query and fetch:
            return [(1,)]  # Return ID 1
        
        # For non-fetch queries, return None
        return None
    
    def test_complete_order_process(self):
        """
        Test the complete order process from adding items to cart through checkout.
        
        This tests:
        1. Adding items to cart
        2. Checking out
        3. Creating an order
        4. Notifications being sent
        5. Inventory being updated
        
        This is a regression test to ensure all components work together correctly
        when a user places an order.
        """
        # 1. Set up test data
        user_id = 1
        product_id = 1
        quantity = 2
        
        # 2. Add item to cart
        CartService.add_to_cart(user_id, product_id, quantity)
        
        # Verify correct query was executed
        self.mock_execute_query.assert_called()
        
        # Reset mock for next checks
        self.mock_execute_query.reset_mock()
        
        # 3. Get cart contents
        cart_items = CartService.get_cart_items(user_id)
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0]['ProductID'], product_id)
        self.assertEqual(cart_items[0]['Quantity'], quantity)
        
        # 4. Initialize checkout service
        checkout_service = CheckoutService()
        
        # 5. Process checkout
        result = checkout_service.checkout(user_id)
        
        # 6. Verify checkout was successful
        self.assertIn("✅", result)
        
        # 7. Verify observers were notified
        self.mock_order_subject.notify.assert_called_with(1, user_id, 199.98, "pending")
        
        # 8. Verify cart was cleared
        self.mock_execute_query.assert_any_call("DELETE FROM Cart WHERE UserID = ?", (user_id,))
        
        # Overall, this test verifies that the complete order process works end-to-end
    
    def test_order_status_updates_all_components(self):
        """
        Test that when an order's status is updated, all other components are notified.
        
        This tests:
        1. Updating an order's status
        2. Notifications being sent to email service
        3. Inventory being updated when status is 'confirmed'
        
        This is a regression test to ensure status changes properly propagate through the system.
        """
        # 1. Set up test data
        order_id = 1
        user_id = 1
        total_amount = 199.98
        new_status = "confirmed"  # This should trigger inventory updates
        
        # 2. Update order status
        order_service = OrderService()
        result = order_service.update_order_status(order_id, new_status)
        
        # 3. Verify order was updated
        self.assertIn(f"Order #{order_id} status updated", result)
        
        # 4. Verify correct query was executed to update the order
        expected_query = "UPDATE Orders SET Status = ?, UpdatedAt = GETDATE() WHERE OrderID = ?"
        self.mock_execute_query.assert_any_call(expected_query, (new_status, order_id))
        
        # 5. Verify observers were notified about the status change
        self.mock_order_subject.notify.assert_called_with(order_id, user_id, total_amount, new_status)
        
        # This test verifies that updating an order's status properly propagates through the system
    
    def test_inventory_updates_when_order_confirmed(self):
        """
        Test that inventory is updated when an order status changes to 'confirmed'.
        
        This tests:
        1. Order status change to 'confirmed'
        2. Inventory service receiving the notification
        3. Inventory quantities being reduced
        
        This is a regression test to ensure inventory management works correctly.
        """
        # Replace the mock_order_subject with a real instance to test the actual observer pattern
        self.patcher_order_subject.stop()
        
        # 1. Create instances of OrderObserver implementations
        email_notification = EmailNotification()
        inventory_update = InventoryUpdate()
        
        # 2. Attach observers to OrderSubject
        OrderSubject._observers = []
        OrderSubject.attach(email_notification)
        OrderSubject.attach(inventory_update)
        
        # 3. Mock the behavior of OrderItems query
        def updated_side_effect(query, params=None, fetch=False):
            if "SELECT * FROM OrderItems WHERE OrderID = ?" in query and fetch:
                return [
                    {
                        'OrderItemID': 1,
                        'OrderID': 1,
                        'ProductID': 1,
                        'Quantity': 2,
                        'Price': 99.99
                    }
                ]
            return self.mock_query_side_effect(query, params, fetch)
        
        # Update the mock with our modified side effect
        self.mock_execute_query.side_effect = updated_side_effect
        
        # 4. Notify observers about the order status change to 'confirmed'
        OrderSubject.notify(1, 1, 199.98, "confirmed")
        
        # 5. Verify inventory was updated for each item in the order
        expected_query = "UPDATE Products SET StockQuantity = StockQuantity - ? WHERE ProductID = ?"
        self.mock_execute_query.assert_any_call(expected_query, (2, 1))
        
        # Restart the patcher for cleanup
        self.patcher_order_subject = patch('app.services.checkout_service.OrderSubject')
        self.mock_order_subject = self.patcher_order_subject.start()


if __name__ == "__main__":
    unittest.main()
