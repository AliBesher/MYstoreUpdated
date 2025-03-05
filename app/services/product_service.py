from app.models.furniture import FurnitureFactory, Furniture

class ProductService:
    @staticmethod
    def add_product(name, description, price, dimensions, stock_quantity, category_id, image_url, furniture_type, **additional_attributes):
        """
        Add a new furniture product to the database after validation.
        """
        # Validate price
        if price <= 0:
            return "⚠️ Price must be greater than 0"

        # Validate stock quantity
        if stock_quantity < 0:
            return "⚠️ Stock quantity must be greater than or equal to 0"

        # Create furniture object using factory pattern
        try:
            furniture = FurnitureFactory.create_furniture(
                furniture_type,
                name,
                description,
                price,
                dimensions,
                stock_quantity,
                category_id,
                image_url,
                additional_attributes
            )
            
            # Add to database
            furniture.add_furniture()
            return f"Product '{name}' added successfully."
            
        except ValueError as e:
            return f"⚠️ {str(e)}"

    @staticmethod
    def update_product(product_id, name, description, price, dimensions, stock_quantity, category_id, image_url, furniture_type, **additional_attributes):
        """
        Update an existing furniture product.
        """
        # Validate price
        if price <= 0:
            return "⚠️ Price must be greater than 0"

        # Validate stock quantity
        if stock_quantity < 0:
            return "⚠️ Stock quantity must be greater than or equal to 0"

        # Create furniture object using factory pattern
        try:
            furniture = FurnitureFactory.create_furniture(
                furniture_type,
                name,
                description,
                price,
                dimensions,
                stock_quantity,
                category_id,
                image_url,
                additional_attributes
            )
            
            # Update in database
            furniture.update_furniture(product_id)
            return f"Product '{name}' updated successfully."
            
        except ValueError as e:
            return f"⚠️ {str(e)}"

    @staticmethod
    def delete_product(product_id):
        """
        Delete a product from the database.
        """
        Furniture.delete_furniture(product_id)
        return "Product deleted successfully."

    @staticmethod
    def get_product_by_id(product_id):
        """
        Get product by ID.
        """
        return Furniture.get_furniture_by_id(product_id)

    @staticmethod
    def update_product_stock(product_id, quantity):
        """
        Update product stock quantity.
        """
        if quantity < 0:
            return "⚠️ Quantity must be greater than or equal to 0"

        # Update stock
        Furniture.update_stock(product_id, quantity)
        return f"Stock updated successfully for product {product_id}."
    
    @staticmethod
    def get_all_products():
        """Get all products."""
        query = """
        SELECT * FROM Products
        ORDER BY Name
        """
        return execute_query(query, fetch=True)
    
    @staticmethod
    def search_products(search_term):
        """Search products by name or description."""
        query = """
        SELECT * FROM Products
        WHERE Name LIKE ? OR Description LIKE ?
        ORDER BY Name
        """
        search_pattern = f"%{search_term}%"
        return execute_query(query, (search_pattern, search_pattern), fetch=True)
    
    @staticmethod
    def get_products_by_category(category_id):
        """Get products by category."""
        query = """
        SELECT * FROM Products
        WHERE CategoryID = ?
        ORDER BY Name
        """
        return execute_query(query, (category_id,), fetch=True)
    
    @staticmethod
    def get_products_by_furniture_type(furniture_type):
        """Get products by furniture type."""
        query = """
        SELECT * FROM Products
        WHERE FurnitureType = ?
        ORDER BY Name
        """
        return execute_query(query, (furniture_type,), fetch=True)
