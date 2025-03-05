from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.furniture import Furniture
from app.services.cart_service import CartService
from app.db.execute_query import execute_query
from app.services.checkout_service import OrderSubject


class OrderService:
    @staticmethod
    def create_order(user_id):
        """
        Create a new order based on cart contents.
        """
        # 1. Get cart contents
        cart_items = CartService.get_cart_items(user_id)
        if not cart_items:
            return "⚠️ No items in the cart."

        total_amount = 0
        # 2. Calculate total amount
        for item in cart_items:
            product_id = item['ProductID']
            quantity = item['Quantity']
            price = item['Price']
            total_amount += price * quantity

        # 3. Create order
        order = Order(user_id, total_amount)
        order_id = order.add_order()  # Add order to database

        # 4. Add order items
        for item in cart_items:
            product_id = item['ProductID']
            quantity = item['Quantity']
            price = item['Price']
            order_item = OrderItem(order_id, product_id, quantity, price)
            order_item.add_order_item()

        # 5. Update inventory
        for item in cart_items:
            product_id = item['ProductID']
            quantity = item['Quantity']
            Furniture.update_stock(product_id, quantity)

        # 6. Clear the cart
        CartService.clear_cart(user_id)
        
        # 7. Notify observers
        OrderSubject.notify(order_id, user_id, total_amount, "pending")

        return f"✅ Order completed successfully. Total amount: {total_amount}."

    @staticmethod
    def update_order_status(order_id, status):
        """
        Update order status.
        """
        # Update order status
        Order.update_order_status(order_id, status)
        
        # Get order details for notification
        order = Order.get_order_by_id(order_id)
        
        if not order:
            return "⚠️ Order not found."
            
        # Notify observers
        OrderSubject.notify(order_id, order['UserID'], order['TotalAmount'], status)
        
        return f"Order #{order_id} status updated to {status}."

    @staticmethod
    def delete_order(order_id):
        """
        Delete an order.
        """
        # Get order details before deletion for notification
        order = Order.get_order_by_id(order_id)
        
        if not order:
            return "⚠️ Order not found."
            
        # Create Order object and delete
        order_obj = Order(order['UserID'], order['TotalAmount'], order['Status'])
        order_obj.delete_order(order_id)
        
        return f"Order #{order_id} deleted successfully."

    @staticmethod
    def get_order_by_user(user_id):
        """
        Get all orders for a user.
        """
        return Order.get_orders_by_user(user_id)

    @staticmethod
    def get_order_by_id(order_id):
        """
        Get order details by ID.
        """
        return Order.get_order_by_id(order_id)
