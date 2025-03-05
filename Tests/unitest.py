import unittest
import os
import sys
from decimal import Decimal
import hashlib
import hmac

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules to test
from app.models import Furniture, Chair, Table, Sofa, Bed, Cabinet, FurnitureFactory
from app.models import User
from app.models import Cart
from app.models import Order
from app.models import OrderItem
from app.models import Category
from app.services import CartService, PercentageDiscount, BuyOneGetOneDiscount, BulkDiscount

# Mock the execute_query function to avoid actual database calls
def mock_execute_query(query, params=None, fetch=False):
    # For testing, just return predefined results based on the query
    if "SELECT" in query and fetch:
        if "Users" in query and "Email" in query:
            # Mocking a user query result
            return [
                {
                    'UserID': 1, 
                    'Name': 'Test User', 
                    'Email': 'test@example.com',
                    'Password': 'hashed_password',
                    'Salt': 'test_salt',
                    'Role': 'customer'
                }
            ]
        elif "Products" in query and "ProductID" in query:
            # Mocking a product query result
            return [
                {
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
            ]
        elif "Cart" in query:
            # Mocking cart items
            return [
                {
                    'CartID': 1,
                    'UserID': 1,
                    'ProductID': 1,
                    'Quantity': 2,
                    'Price': 99.99,
                    'Name': 'Test Chair',
                    'CategoryID': 1
                }
            ]
    # For other queries, just return None or empty list
    return [] if fetch else None

# Replace the actual execute_query with our mock
import app.db.execute_query
app.db.execute_query.execute_query = mock_execute_query

# Unit tests for models and services
class TestFurnitureModels(unittest.TestCase):
    """Test cases for furniture model classes."""
    
    def test_chair_creation(self):
        """Test creating a Chair object."""
        chair = Chair(
            name="Test Chair",
            description="A test chair",
            price=Decimal("99.99"),
            dimensions="60x60x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/test.jpg",
            max_weight_capacity=120,
            has_armrests=True,
            is_adjustable=False
        )
        
        self.assertEqual(chair.name, "Test Chair")
        self.assertEqual(chair.price, Decimal("99.99"))
        self.assertEqual(chair.get_furniture_type(), "Chair")
        self.assertTrue(chair.has_armrests)
        self.assertFalse(chair.is_adjustable)
    
    def test_table_creation(self):
        """Test creating a Table object."""
        table = Table(
            name="Test Table",
            description="A test table",
            price=Decimal("149.99"),
            dimensions="120x80x75",
            stock_quantity=5,
            category_id=1,
            image_url="/images/test_table.jpg",
            shape="Rectangle",
            max_weight_capacity=200,
            is_extendable=True
        )
        
        self.assertEqual(table.name, "Test Table")
        self.assertEqual(table.price, Decimal("149.99"))
        self.assertEqual(table.get_furniture_type(), "Table")
        self.assertEqual(table.shape, "Rectangle")
        self.assertTrue(table.is_extendable)
    
    def test_sofa_creation(self):
        """Test creating a Sofa object."""
        sofa = Sofa(
            name="Test Sofa",
            description="A test sofa",
            price=Decimal("499.99"),
            dimensions="220x90x85",
            stock_quantity=3,
            category_id=1,
            image_url="/images/test_sofa.jpg",
            seats=3,
            is_convertible=True,
            has_storage=False
        )
        
        self.assertEqual(sofa.name, "Test Sofa")
        self.assertEqual(sofa.price, Decimal("499.99"))
        self.assertEqual(sofa.get_furniture_type(), "Sofa")
        self.assertEqual(sofa.seats, 3)
        self.assertTrue(sofa.is_convertible)
        self.assertFalse(sofa.has_storage)
    
    def test_factory_pattern(self):
        """Test the FurnitureFactory creates correct objects."""
        # Create a chair using the factory
        chair = FurnitureFactory.create_furniture(
            "Chair",
            "Factory Chair",
            "A chair created by the factory",
            Decimal("129.99"),
            "65x65x110",
            8,
            1,
            "/images/factory_chair.jpg",
            {"max_weight_capacity": 130, "has_armrests": True, "is_adjustable": True}
        )
        
        # Check that it's the correct type and has the right properties
        self.assertIsInstance(chair, Chair)
        self.assertEqual(chair.name, "Factory Chair")
        self.assertEqual(chair.get_furniture_type(), "Chair")
        self.assertTrue(chair.is_adjustable)
        
        # Create a table using the factory
        table = FurnitureFactory.create_furniture(
            "Table",
            "Factory Table",
            "A table created by the factory",
            Decimal("179.99"),
            "130x80x75",
            6,
            1,
            "/images/factory_table.jpg",
            {"shape": "Round", "max_weight_capacity": 180, "is_extendable": False}
        )
        
        # Check that it's the correct type and has the right properties
        self.assertIsInstance(table, Table)
        self.assertEqual(table.name, "Factory Table")
        self.assertEqual(table.get_furniture_type(), "Table")
        self.assertEqual(table.shape, "Round")
    
    def test_discount_calculation(self):
        """Test that furniture-specific discounts are calculated correctly."""
        # Chair with adjustable feature (gets extra 5% discount)
        chair = Chair(
            name="Discounted Chair",
            description="A chair with a discount",
            price=Decimal("100.00"),
            dimensions="60x60x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/disc_chair.jpg",
            max_weight_capacity=120,
            has_armrests=True,
            is_adjustable=True  # Should get extra discount
        )
        
        # Apply 10% discount
        discount = chair.calculate_discount(10)
        
        # Should be 10% base + 5% additional = 15% of 100 = 15
        self.assertEqual(discount, Decimal("15.00"))
        
        # Table without extendable feature
        table = Table(
            name="Discounted Table",
            description="A table with a discount",
            price=Decimal("200.00"),
            dimensions="120x80x75",
            stock_quantity=5,
            category_id=1,
            image_url="/images/disc_table.jpg",
            shape="Rectangle",
            max_weight_capacity=200,
            is_extendable=False  # No extra discount
        )
        
        # Apply 10% discount
        discount = table.calculate_discount(10)
        
        # Should be just 10% = 20
        self.assertEqual(discount, Decimal("20.00"))


class TestUserModel(unittest.TestCase):
    """Test cases for User model."""
    
    def test_password_hashing(self):
        """Test that passwords are hashed correctly."""
        # Test the static hash method
        password = "testpassword"
        salt = "testsalt"
        
        hashed_pwd = User._hash_password(password, salt)
        
        # Verify the hash is correct
        self.assertTrue(isinstance(hashed_pwd, str))
        self.assertNotEqual(hashed_pwd, password)  # Should not be plaintext
        
        # Verify the same password + salt always produces the same hash
        hashed_pwd2 = User._hash_password(password, salt)
        self.assertEqual(hashed_pwd, hashed_pwd2)
        
        # Verify different passwords produce different hashes
        hashed_pwd3 = User._hash_password("differentpassword", salt)
        self.assertNotEqual(hashed_pwd, hashed_pwd3)
    
    def test_password_verification(self):
        """Test that password verification works correctly."""
        password = "testpassword"
        salt = "testsalt"
        
        # Hash the password
        hashed_pwd = User._hash_password(password, salt)
        
        # Verify correct password returns True
        result = User.verify_password(password, hashed_pwd, salt)
        self.assertTrue(result)
        
        # Verify incorrect password returns False
        result = User.verify_password("wrongpassword", hashed_pwd, salt)
        self.assertFalse(result)


class TestDiscountStrategies(unittest.TestCase):
    """Test cases for discount strategy classes."""
    
    def test_percentage_discount(self):
        """Test the percentage discount strategy."""
        # Create a percentage discount of 10%
        discount_strategy = PercentageDiscount(10)
        
        # Create mock cart items
        cart_items = [
            {'ProductID': 1, 'Quantity': 2, 'Price': Decimal("100.00")},
            {'ProductID': 2, 'Quantity': 1, 'Price': Decimal("50.00")}
        ]
        
        # Expected discount: 10% of (2*100 + 1*50) = 10% of 250 = 25
        expected_discount = Decimal("25.00")
        actual_discount = discount_strategy.apply_discount(cart_items)
        
        self.assertAlmostEqual(float(actual_discount), float(expected_discount), places=2)
    
    def test_buy_one_get_one_discount(self):
        """Test the buy one get one discount strategy."""
        # Create a BOGO discount for category 1
        discount_strategy = BuyOneGetOneDiscount([1])
        
        # Create mock cart items (2 items in eligible category)
        cart_items = [
            {'ProductID': 1, 'Quantity': 2, 'Price': Decimal("100.00"), 'CategoryID': 1},
            {'ProductID': 2, 'Quantity': 3, 'Price': Decimal("50.00"), 'CategoryID': 1},
            {'ProductID': 3, 'Quantity': 1, 'Price': Decimal("75.00"), 'CategoryID': 2}  # Not eligible
        ]
        
        # Expected discount: 1 free chair (100) + 1 free chair (50) = 150
        expected_discount = Decimal("150.00")
        actual_discount = discount_strategy.apply_discount(cart_items)
        
        self.assertAlmostEqual(float(actual_discount), float(expected_discount), places=2)
    
    def test_bulk_discount(self):
        """Test the bulk discount strategy."""
        # Create a bulk discount: 15% off when quantity >= 3
        discount_strategy = BulkDiscount(3, 15)
        
        # Create mock cart items
        cart_items = [
            {'ProductID': 1, 'Quantity': 4, 'Price': Decimal("100.00")},  # Eligible
            {'ProductID': 2, 'Quantity': 2, 'Price': Decimal("50.00")},   # Not eligible
            {'ProductID': 3, 'Quantity': 3, 'Price': Decimal("75.00")}    # Eligible
        ]
        
        # Expected discount: 15% of (4*100) + 15% of (3*75) = 60 + 33.75 = 93.75
        expected_discount = Decimal("93.75")
        actual_discount = discount_strategy.apply_discount(cart_items)
        
        self.assertAlmostEqual(float(actual_discount), float(expected_discount), places=2)


class TestCartModel(unittest.TestCase):
    """Test cases for Cart model."""
    
    def test_cart_total_calculation(self):
        """Test calculating the cart total."""
        # Create a Cart instance
        cart = Cart(1)  # user_id = 1
        
        # Mock the get_cart_items method to return test data
        original_method = cart.get_cart_items
        cart.get_cart_items = lambda: [
            {'ProductID': 1, 'Quantity': 2, 'Price': Decimal("100.00")},
            {'ProductID': 2, 'Quantity': 1, 'Price': Decimal("50.00")}
        ]
        
        # Calculate total: 2*100 + 1*50 = 250
        expected_total = Decimal("250.00")
        actual_total = cart.calculate_total()
        
        # Restore original method
        cart.get_cart_items = original_method
        
        self.assertEqual(actual_total, expected_total)


if __name__ == "__main__":
    unittest.main()
