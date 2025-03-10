from app.db import execute_query


class Order:
    """Order class for managing customer orders."""

    def __init__(self, user_id, total_amount, status="pending"):
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status



    def add_order(self):
        """
        Add order to the database and return the order ID.

        Improved error handling and validation.
        """
        query = """
        INSERT INTO Orders (UserID, TotalAmount, Status, OrderDate)
        OUTPUT INSERTED.OrderID
        VALUES (?, ?, ?, GETDATE())
        """
        try:
            result = execute_query(query, (self.user_id, self.total_amount, self.status), fetch=True)

            # Robust error checking
            if not result:
                print("No result returned from order insertion.")
                return None

            # Safely extract the order ID
            if isinstance(result, list) and len(result) > 0:
                # Check if the first item is a tuple or list
                if isinstance(result[0], (tuple, list)) and len(result[0]) > 0:
                    order_id = result[0][0]
                    print(f"Order #{order_id} added successfully.")
                    return order_id
                elif isinstance(result[0], int):
                    order_id = result[0]
                    print(f"Order #{order_id} added successfully.")
                    return order_id

            # If we can't extract the order ID
            print("Unable to extract order ID from the result.")
            return None

        except Exception as e:
            print(f"Error adding order: {e}")
            return None




    def update_order(self, order_id):
        """Update order status and total amount."""
        query = """
        UPDATE Orders
        SET Status = ?, TotalAmount = ?, UpdatedAt = GETDATE()
        WHERE OrderID = ?
        """
        execute_query(query, (self.status, self.total_amount, order_id))
        print(f"Order #{order_id} updated successfully.")

    def delete_order(self, order_id):
        """Delete order and related order items."""
        # First delete related order items
        query = "DELETE FROM OrderItems WHERE OrderID = ?"
        execute_query(query, (order_id,))

        # Then delete the order
        query = "DELETE FROM Orders WHERE OrderID = ?"
        execute_query(query, (order_id,))
        print(f"Order #{order_id} deleted successfully.")

    @staticmethod
    def get_order_by_id(order_id):
        """Get order by ID."""
        query = """
        SELECT o.*, u.Name as UserName, u.Email as UserEmail 
        FROM Orders o
        JOIN Users u ON o.UserID = u.UserID
        WHERE o.OrderID = ?
        """
        result = execute_query(query, (order_id,), fetch=True)

        if result:
            return result[0]
        return None

    @staticmethod
    def get_order_items(order_id):
        """Get all items for an order."""
        query = """
        SELECT oi.*, p.Name as ProductName, p.ImageURL as ProductImage, p.FurnitureType
        FROM OrderItems oi
        JOIN Products p ON oi.ProductID = p.ProductID
        WHERE oi.OrderID = ?
        """
        return execute_query(query, (order_id,), fetch=True)

    @staticmethod
    def get_orders_by_user(user_id):
        """Get all orders for a user."""
        query = """
        SELECT o.*, COUNT(oi.OrderItemID) as ItemCount
        FROM Orders o
        LEFT JOIN OrderItems oi ON o.OrderID = oi.OrderID
        WHERE o.UserID = ?
        GROUP BY o.OrderID, o.UserID, o.TotalAmount, o.Status, o.CreatedAt, o.UpdatedAt, o.PaymentMethod
        ORDER BY o.CreatedAt DESC
        """
        return execute_query(query, (user_id,), fetch=True)

    @staticmethod
    def get_orders_by_status(status):
        """Get all orders with a specific status."""
        query = """
        SELECT o.*, u.Name as UserName
        FROM Orders o
        JOIN Users u ON o.UserID = u.UserID
        WHERE o.Status = ?
        ORDER BY o.CreatedAt DESC
        """
        return execute_query(query, (status,), fetch=True)

    @staticmethod
    def update_order_status(order_id, status):
        """Update order status."""
        query = """
        UPDATE Orders
        SET Status = ?, UpdatedAt = GETDATE()
        WHERE OrderID = ?
        """
        execute_query(query, (status, order_id))
        print(f"Order #{order_id} status updated to {status} successfully.")

        # Return the updated order
        return Order.get_order_by_id(order_id)
