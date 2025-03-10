from app.db import execute_query


class OrderItem:
    """Class representing items within an order."""

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def add_order_item(self):
        """Add an item to an order."""
        query = """
        INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price)
        VALUES (?, ?, ?, ?)
        """
        execute_query(query, (self.order_id, self.product_id, self.quantity, self.price))
        print(f"Order item for product {self.product_id} added successfully.")

    def update_order_item(self, order_item_id):
        """Update an existing order item."""
        query = """
        UPDATE OrderItems
        SET Quantity = ?, Price = ?
        WHERE OrderItemID = ?
        """
        execute_query(query, (self.quantity, self.price, order_item_id))
        print(f"Order item #{order_item_id} updated successfully.")

    @staticmethod
    def delete_order_item(order_item_id):
        """Delete an order item."""
        query = "DELETE FROM OrderItems WHERE OrderItemID = ?"
        execute_query(query, (order_item_id,))
        print(f"Order item #{order_item_id} deleted successfully.")

    @staticmethod
    def get_order_item(order_item_id):
        """Get an order item by ID."""
        query = """
        SELECT oi.*, p.Name as ProductName
        FROM OrderItems oi
        JOIN Products p ON oi.ProductID = p.ProductID
        WHERE oi.OrderItemID = ?
        """
        result = execute_query(query, (order_item_id,), fetch=True)

        if result:
            return result[0]
        return None

    @staticmethod
    def get_items_by_order(order_id):
        """Get all items for an order."""
        query = """
        SELECT oi.*, p.Name as ProductName, p.ImageURL as ProductImage, p.FurnitureType
        FROM OrderItems oi
        JOIN Products p ON oi.ProductID = p.ProductID
        WHERE oi.OrderID = ?
        """
        return execute_query(query, (order_id,), fetch=True)

    @staticmethod
    def calculate_order_total(order_id):
        """Calculate the total price of all items in an order."""
        query = """
        SELECT SUM(Quantity * Price) as Total
        FROM OrderItems
        WHERE OrderID = ?
        """
        result = execute_query(query, (order_id,), fetch=True)

        if result and result[0][0]:
            return result[0][0]
        return 0
