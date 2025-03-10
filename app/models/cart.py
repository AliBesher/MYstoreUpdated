from app.db import execute_query

class Cart:
    def __init__(self, user_id):
        self.user_id = user_id

    def add_to_cart(self, product_id, quantity):
        """Add item to cart."""
        # Validate quantity
        if quantity <= 0:
            raise ValueError("⚠️ Quantity must be greater than 0.")

        # Check if item exists in cart
        existing_item = self.get_cart_item(product_id)

        if existing_item:
            # Update quantity if item exists
            new_quantity = existing_item['Quantity'] + quantity
            self.update_cart(product_id, new_quantity)
        else:
            # Add new item to cart
            query = """
            INSERT INTO Cart (UserID, ProductID, Quantity, AddedAt)
            VALUES (?, ?, ?, GETDATE())
            """
            execute_query(query, (self.user_id, product_id, quantity))
            print(f"Product added to cart successfully.")

    def update_cart(self, product_id, new_quantity):
        """Update cart item quantity."""
        # Validate quantity
        if new_quantity <= 0:
            raise ValueError("⚠️ Quantity must be greater than 0.")

        # Check if item exists in cart
        existing_item = self.get_cart_item(product_id)
        if not existing_item:
            raise ValueError("⚠️ Product not found in cart.")

        query = """
        UPDATE Cart
        SET Quantity = ?
        WHERE UserID = ? AND ProductID = ?
        """
        execute_query(query, (new_quantity, self.user_id, product_id))
        print(f"Cart quantity updated successfully.")

    def remove_from_cart(self, product_id):
        """Remove item from cart."""
        # Check if item exists in cart
        existing_item = self.get_cart_item(product_id)
        if not existing_item:
            raise ValueError("⚠️ Product not found in cart.")

        query = "DELETE FROM Cart WHERE UserID = ? AND ProductID = ?"
        execute_query(query, (self.user_id, product_id))
        print(f"Product removed from cart successfully.")

    def clear_cart(self):
        """Remove all items from user's cart."""
        query = "DELETE FROM Cart WHERE UserID = ?"
        execute_query(query, (self.user_id,))
        print(f"Cart cleared successfully.")

    def get_cart_item(self, product_id):
        """Get a specific item from cart."""
        query = "SELECT * FROM Cart WHERE UserID = ? AND ProductID = ?"
        result = execute_query(query, (self.user_id, product_id), fetch=True)
        if result and len(result) > 0:
            return result[0]
        return None

    def get_cart_items(self):
        """Get all items in user's cart with product details."""
        query = """
        SELECT c.*, p.Name, p.Price, p.ImageURL, p.FurnitureType, p.CategoryID
        FROM Cart c
        JOIN Products p ON c.ProductID = p.ProductID
        WHERE c.UserID = ?
        """
        result = execute_query(query, (self.user_id,), fetch=True)
        if result:
            return result
        return []

    def calculate_total(self):
        """Calculate total price of items in cart."""
        cart_items = self.get_cart_items()

        if not cart_items:
            return 0

        total = 0
        for item in cart_items:
            item_total = item['Price'] * item['Quantity']
            total += item_total

        return total
