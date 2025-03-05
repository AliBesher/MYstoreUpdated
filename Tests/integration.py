import unittest
import os
import sys
import json
from decimal import Decimal
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Flask app
from main import app
from app.services import UserService
from app.services import ProductService
from app.services import CartService
from app.services import OrderService
from app.services import CheckoutService
from app.models import Chair, Table, Sofa, Bed, Cabinet
from app.db import execute_query

# Create a test client
class IntegrationTests(unittest.TestCase):
    """Integration tests for the online furniture store."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Mock the execute_query function
        self.patcher = patch('app.db.execute_query.execute_query')
        self.mock_execute_query = self.patcher.start()
        
        # Set up mock return values for different types of queries
        self.mock_execute_query.side_effect = self.mock_query_side_effect
    
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
    
    def mock_query_side_effect(self, query, params=None, fetch=False):
        """Side effect function for the mock execute_query."""
        # For SELECT queries that fetch data
        if "SELECT" in query and fetch:
            if "Users" in query:
                if params and params[0] == 1:  # User ID 1
                    return [{
                        'UserID': 1,
                        'Name': 'Test User',
                        'Email': 'test@example.com',
                        'Password': 'hashed_password',
                        'Salt': 'test_salt',
                        'Role': 'customer'
                    }]
                else:
                    return [{
                        'UserID': 1,
                        'Name': 'Test User',
                        'Email': 'test@example.com',
                        'Role': 'customer'
                    }]
            
            elif "Products" in query:
                if params and params[0] == 1:  # Product ID 1
                    return [{
                        'ProductID': 1,
                        'Name': 'Test Chair',
                        'Description': 'A test chair',
                        'Price': 99.99,
                        'Dimensions': '60x60x100',
                        'StockQuantity': 10,
                        'CategoryID': 1,
                        'ImageURL': '/images/test.jpg',
                        'FurnitureType': 'Chair'
                    }]
                else:
                    return [
                        {
                            'ProductID': 1,
                            'Name': 'Test Chair',
                            'Description': 'A test chair',
                            'Price': 99.99,
                            'CategoryID': 1,
                            'FurnitureType': 'Chair'
                        },
                        {
                            'ProductID': 2,
                            'Name': 'Test Table',
                            'Description': 'A test table',
                            'Price': 149.99,
                            'CategoryID': 1,
                            'FurnitureType': 'Table'
                        }
                    ]
            
            elif "Cart" in query:
                return [
                    {
                        'CartID': 1,
                        'UserID': 1,
                        'ProductID': 1,
                        'Quantity': 2,
                        'Name': 'Test Chair',
                        'Price': 99.99,
                        'CategoryID': 1
                    }
                ]
            
            elif "Orders" in query:
                if "OrderID" in query and params and params[0] == 1:
                    return [{
                        'OrderID': 1,
                        'UserID': 1,
                        'TotalAmount': 199.98,
                        'Status': 'pending',
                        'CreatedAt': '2023-01-01'
                    }]
                elif "UserID" in query and params and params[0] == 1:
                    return [
                        {
                            'OrderID': 1,
                            'UserID': 1,
                            'TotalAmount': 199.98,
                            'Status': 'pending',
                            'CreatedAt': '2023-01-01'
                        },
                        {
                            'OrderID': 2,
                            'UserID': 1,
                            'TotalAmount': 149.99,
                            'Status': 'delivered',
                            'CreatedAt': '2023-01-02'
                        }
                    ]
                else:
                    return []
            
            elif "OrderItems" in query:
                return [
                    {
                        'OrderItemID': 1,
                        'OrderID': 1,
                        'ProductID': 1,
                        'Quantity': 2,
                        'Price': 99.99
                    }
                ]
            
            else:
                return []
        
        # For INSERT queries that return IDs
        elif "INSERT" in query and "OUTPUT INSERTED" in query and fetch:
            return [(1,)]  # Return ID 1
        
        # For other non-fetch queries
        return None
    
    # Test user-related API endpoints
    def test_get_users(self):
        """Test the GET /api/users endpoint."""
        response = self.app.get('/api/users')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', data)
    
    def test_get_user_by_id(self):
        """Test the GET /api/users/<id> endpoint."""
        response = self.app.get('/api/users/1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', data)
        self.assertEqual(data['user']['UserID'], 1)
    
    def test_add_user(self):
        """Test the POST /api/users endpoint."""
        user_data = {
            'name': 'New User',
            'email': 'new@example.com',
            'password': 'password123',
            'role': 'customer'
        }
        
        response = self.app.post('/api/users', 
                                json=user_data)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
    
    # Test product-related API endpoints
    def test_get_products(self):
        """Test the GET /api/products endpoint."""
        response = self.app.get('/api/products')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', data)
    
    def test_get_product_by_id(self):
        """Test the GET /api/products/<id> endpoint."""
        # We need to patch the FurnitureFactory.create_furniture method
        with patch('app.models.furniture.FurnitureFactory.create_furniture') as mock_factory:
            # Create a mock chair
            chair = Chair("Test Chair", "A test chair", 99.99, "60x60x100", 
                        10, 1, "/images/test.jpg", 120, True, False)
            # Set up the mock to return our chair
            mock_factory.return_value = chair
            
            response = self.app.get('/api/products/1')
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('product', data)
    
    def test_add_product(self):
        """Test the POST /api/products endpoint."""
        product_data = {
            'name': 'New Chair',
            'description': 'A new test chair',
            'price': 129.99,
            'dimensions': '65x65x110',
            'stock_quantity': 5,
            'category_id': 1,
            'image_url': '/images/new_chair.jpg',
            'furniture_type': 'Chair',
            'max_weight_capacity': 130,
            'has_armrests': True,
            'is_adjustable': True
        }
        
        response = self.app.post('/api/products',
                                json=product_data)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
    
    # Test cart-related API endpoints
    def test_view_cart(self):
        """Test the GET /api/cart endpoint."""
        response = self.app.get('/api/cart?user_id=1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart_items', data)
    
    def test_add_to_cart(self):
        """Test the POST /api/cart endpoint."""
        cart_data = {
            'user_id': 1,
            'product_id': 1,
            'quantity': 2
        }
        
        response = self.app.post('/api/cart',
                                json=cart_data)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
    
    # Test order-related API endpoints
    def test_get_orders(self):
        """Test the GET /api/orders endpoint."""
        response = self.app.get('/api/orders?user_id=1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', data)
    
    def test_create_order(self):
        """Test the POST /api/orders endpoint."""
        order_data = {
            'user_id': 1
        }
        
        response = self.app.post('/api/orders',
                                json=order_data)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
    
    # Test checkout process
    def test_checkout_process(self):
        """Test the POST /api/checkout endpoint."""
        checkout_data = {
            'user_id': 1
        }
        
        # We need to patch the CheckoutService
        with patch('app.services.checkout_service.CheckoutService.checkout') as mock_checkout:
            mock_checkout.return_value = "✅ Checkout completed successfully. Total amount: 199.98."
            
            response = self.app.post('/api/checkout',
                                    json=checkout_data)
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('message', data)
            self.assertIn("Checkout completed successfully", data['message'])
    
    # Test integration between services
    def test_service_integration(self):
        """Test integration between multiple services."""
        # Mock direct calls to execute_query to provide fixed results
        # This allows us to test the interaction between services without 
        # making actual database calls
        
        # 1. User adds product to cart
        CartService.add_to_cart(1, 1, 2)
        self.mock_execute_query.assert_called()
        
        # Reset call count
        self.mock_execute_query.reset_mock()
        
        # 2. User gets cart contents
        cart_items = CartService.get_cart_items(1)
        self.assertIsNotNone(cart_items)
        self.mock_execute_query.assert_called()
        
        # 3. User proceeds to checkout
        checkout_service = CheckoutService()
        
        # Mock order creation to avoid DB changes
        with patch('app.models.order.Order.add_order') as mock_add_order:
            mock_add_order.return_value = 1  # Order ID
            
            result = checkout_service.checkout(1)
            self.assertIn("Checkout completed successfully", result)


if __name__ == "__main__":
    unittest.main()
