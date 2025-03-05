from abc import ABC, abstractmethod
from app.db.execute_query import execute_query
from app.models.cart import Cart
from app.models.furniture import Furniture


# Strategy Pattern for discount calculation
class DiscountStrategy(ABC):
    """Abstract base class for discount strategies."""
    
    @abstractmethod
    def apply_discount(self, cart_items):
        """Apply discount to cart items."""
        pass


class PercentageDiscount(DiscountStrategy):
    """Apply a percentage discount to all items in cart."""
    
    def __init__(self, percentage):
        self.percentage = percentage
        
    def apply_discount(self, cart_items):
        """Apply percentage discount to all items."""
        total_discount = 0
        for item in cart_items:
            item_price = item['Price'] * item['Quantity']
            item_discount = item_price * (self.percentage / 100)
            total_discount += item_discount
        
        return total_discount


class BuyOneGetOneDiscount(DiscountStrategy):
    """Buy one get one free for specified product categories."""
    
    def __init__(self, eligible_categories):
        self.eligible_categories = eligible_categories
        
    def apply_discount(self, cart_items):
        """Apply buy one get one free discount."""
        total_discount = 0
        
        # Group items by product ID
        product_quantities = {}
        for item in cart_items:
            product_id = item['ProductID']
            category_id = item['CategoryID']
            
            if category_id in self.eligible_categories:
                if product_id not in product_quantities:
                    product_quantities[product_id] = {
                        'quantity': 0,
                        'price': item['Price']
                    }
                
                product_quantities[product_id]['quantity'] += item['Quantity']
        
        # Calculate discount for eligible products
        for product_data in product_quantities.values():
            free_items = product_data['quantity'] // 2  # Integer division
            item_discount = free_items * product_data['price']
            total_discount += item_discount
        
        return total_discount


class BulkDiscount(DiscountStrategy):
    """Apply discount when quantity exceeds threshold."""
    
    def __init__(self, threshold, percentage):
        self.threshold = threshold
        self.percentage = percentage
        
    def apply_discount(self, cart_items):
        """Apply bulk purchase discount."""
        total_discount = 0
        
        for item in cart_items:
            if item['Quantity'] >= self.threshold:
                item_price = item['Price'] * item['Quantity']
                item_discount = item_price * (self.percentage / 100)
                total_discount += item_discount
        
        return total_discount


class CartService:
    """Service for managing shopping cart operations."""
    
    @staticmethod
    def add_to_cart(user_id, product_id, quantity):
        """Add item to cart."""
        cart = Cart(user_id)
        cart.add_to_cart(product_id, quantity)
        return "Product added to cart successfully."

    @staticmethod
    def update_cart(user_id, product_id, new_quantity):
        """Update cart item quantity."""
        cart = Cart(user_id)
        cart.update_cart(product_id, new_quantity)
        return "Cart updated successfully."

    @staticmethod
    def remove_from_cart(user_id, product_id):
        """Remove item from cart."""
        cart = Cart(user_id)
        cart.remove_from_cart(product_id)
        return "Product removed from cart successfully."
        
    @staticmethod
    def clear_cart(user_id):
        """Remove all items from user's cart."""
        cart = Cart(user_id)
        cart.clear_cart()
        return "Cart cleared successfully."

    @staticmethod
    def get_cart_items(user_id):
        """Get all cart items for a user."""
        cart = Cart(user_id)
        return cart.get_cart_items()
        
    @staticmethod
    def calculate_cart_total(user_id):
        """Calculate total price of items in cart."""
        cart = Cart(user_id)
        return cart.calculate_total()
        
    @staticmethod
    def apply_discount(user_id, discount_strategy):
        """Apply discount strategy to cart."""
        cart_items = CartService.get_cart_items(user_id)
        
        if not cart_items:
            return 0
            
        return discount_strategy.apply_discount(cart_items)
        
    @staticmethod
    def get_cart_count(user_id):
        """Get number of items in cart."""
        query = "SELECT COUNT(*) FROM Cart WHERE UserID = ?"
        result = execute_query(query, (user_id,), fetch=True)
        
        if result:
            return result[0][0]
        return 0
