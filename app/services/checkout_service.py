from abc import ABC, abstractmethod
from app.services.cart_service import CartService
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.furniture import Furniture
from app.db.execute_query import execute_query


# Observer Pattern for order notifications
class OrderObserver(ABC):
    """Abstract base class for order observers."""
    
    @abstractmethod
    def update(self, order_id, user_id, total_amount, status):
        """Update method called when order status changes."""
        pass


class EmailNotification(OrderObserver):
    """Send email notifications for order updates."""
    
    def update(self, order_id, user_id, total_amount, status):
        """Send email notification to user."""
        # In a real application, this would send an actual email
        print(f"Sending email notification to user {user_id} about order {order_id}.")
        print(f"Order status: {status}, Total amount: {total_amount}")
        
        # Mock implementation - in reality would use an email service
        query = """
        INSERT INTO Notifications (UserID, OrderID, Message, CreatedAt)
        VALUES (?, ?, ?, GETDATE())
        """
        message = f"Your order #{order_id} status is now: {status}. Total amount: {total_amount}"
        execute_query(query, (user_id, order_id, message))


class InventoryUpdate(OrderObserver):
    """Update inventory when order status changes."""
    
    def update(self, order_id, user_id, total_amount, status):
        """Update inventory based on order status."""
        if status == "confirmed":
            # Get order items
            query = "SELECT * FROM OrderItems WHERE OrderID = ?"
            order_items = execute_query(query, (order_id,), fetch=True)
            
            # Update inventory for each item
            for item in order_items:
                product_id = item['ProductID']
                quantity = item['Quantity']
                Furniture.update_stock(product_id, quantity)
                
            print(f"Inventory updated for order {order_id}")


class OrderSubject:
    """Subject class for the Observer pattern."""
    
    _observers = []
    
    @classmethod
    def attach(cls, observer):
        """Attach an observer."""
        if observer not in cls._observers:
            cls._observers.append(observer)
    
    @classmethod
    def detach(cls, observer):
        """Detach an observer."""
        try:
            cls._observers.remove(observer)
        except ValueError:
            pass
    
    @classmethod
    def notify(cls, order_id, user_id, total_amount, status):
        """Notify all observers about order update."""
        for observer in cls._observers:
            observer.update(order_id, user_id, total_amount, status)


class CheckoutService:
    """Service for processing checkout operations."""
    
    def __init__(self):
        """Initialize checkout service and attach observers."""
        # Attach observers for order notifications
        OrderSubject.attach(EmailNotification())
        OrderSubject.attach(InventoryUpdate())
    
    @staticmethod
    def checkout(user_id):
        """Process checkout for a user's cart."""
        # 1. Get cart contents
        cart_items = CartService.get_cart_items(user_id)
        if not cart_items:
            return "⚠️ No items in the cart."

        # 2. Calculate total amount
        total_amount = 0
        for item in cart_items:
            product_id = item['ProductID']
            quantity = item['Quantity']
            price = item['Price']
            total_amount += price * quantity

        # 3. Create order
        order = Order(user_id, total_amount, "pending")
        order_id = order.add_order()  # Returns the new order ID

        # 4. Add order items
        for item in cart_items:
            product_id = item['ProductID']
            quantity = item['Quantity']
            price = item['Price']
            order_item = OrderItem(order_id, product_id, quantity, price)
            order_item.add_order_item()

        # 5. Notify observers of the new order
        OrderSubject.notify(order_id, user_id, total_amount, "pending")

        # 6. Clear the cart
        CartService.clear_cart(user_id)

        return f"✅ Checkout completed successfully. Total amount: {total_amount}."
    
    @staticmethod
    def process_payment(order_id, payment_method, payment_details):
        """Process payment for an order."""
        # This would connect to a payment gateway in a real application
        # For this implementation, we'll just update the order status
        
        # Update order status to "paid"
        query = """
        UPDATE Orders
        SET Status = 'paid', PaymentMethod = ?, UpdatedAt = GETDATE()
        WHERE OrderID = ?
        """
        execute_query(query, (payment_method, order_id))
        
        # Get order details for notification
        query = "SELECT * FROM Orders WHERE OrderID = ?"
        order_result = execute_query(query, (order_id,), fetch=True)
        
        if not order_result:
            return "⚠️ Order not found."
            
        order = order_result[0]
        
        # Notify observers about payment
        OrderSubject.notify(order_id, order['UserID'], order['TotalAmount'], "paid")
        
        return f"✅ Payment processed successfully for order {order_id}."
    
    @staticmethod
    def update_order_status(order_id, new_status):
        """Update order status and notify observers."""
        # Update order status
        query = """
        UPDATE Orders
        SET Status = ?, UpdatedAt = GETDATE()
        WHERE OrderID = ?
        """
        execute_query(query, (new_status, order_id))
        
        # Get order details for notification
        query = "SELECT * FROM Orders WHERE OrderID = ?"
        order_result = execute_query(query, (order_id,), fetch=True)
        
        if not order_result:
            return "⚠️ Order not found."
            
        order = order_result[0]
        
        # Notify observers about status change
        OrderSubject.notify(order_id, order['UserID'], order['TotalAmount'], new_status)
        
        return f"✅ Order {order_id} status updated to {new_status}."
    
    @staticmethod
    def get_order_by_user(user_id):
        """Get all orders for a user."""
        query = "SELECT * FROM Orders WHERE UserID = ? ORDER BY CreatedAt DESC"
        return execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_order_by_id(order_id):
        """Get order details by ID."""
        query = "SELECT * FROM Orders WHERE OrderID = ?"
        return execute_query(query, (order_id,), fetch=True)
