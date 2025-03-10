from app.models import FurnitureFactory, Furniture
from app.db import execute_query

class ProductService:
    @staticmethod
    def add_product(name, description, price, dimensions, stock_quantity, category_id, image_url, furniture_type, **additional_attributes):
        """
        Add a new furniture product to the database after validation.
        """
        # Validate name and description
        if not name or not description:
            return "⚠️ Name and description are required"

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
        except Exception as e:
            return f"⚠️ An error occurred: {str(e)}"

    @staticmethod
    def update_product(product_id, name, description, price, dimensions, stock_quantity, category_id, image_url, furniture_type, **additional_attributes):
        """
        Update an existing furniture product.
        """
        # Check if product exists
        existing_product = ProductService.get_product_by_id(product_id)
        if not existing_product:
            return f"⚠️ Product with ID {product_id} not found"

        # Validate name and description
        if not name or not description:
            return "⚠️ Name and description are required"

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
        except Exception as e:
            return f"⚠️ An error occurred: {str(e)}"

    @staticmethod
    def delete_product(product_id):
        """
        Delete a product from the database.
        """
        # Check if product exists
        existing_product = ProductService.get_product_by_id(product_id)
        if not existing_product:
            return f"⚠️ Product with ID {product_id} not found"

        try:
            Furniture.delete_furniture(product_id)
            return "Product deleted successfully."
        except Exception as e:
            return f"⚠️ An error occurred while deleting the product: {str(e)}"

    @staticmethod
    def get_product_by_id(product_id):
        """
        Get product by ID.
        """
        if not product_id or product_id <= 0:
            return None

        try:
            return Furniture.get_furniture_by_id(product_id)
        except Exception:
            return None

    @staticmethod
    def update_product_stock(product_id, quantity):
        """
        Update product stock quantity.
        """
        # Check if product exists
        existing_product = ProductService.get_product_by_id(product_id)
        if not existing_product:
            return f"⚠️ Product with ID {product_id} not found"

        if quantity < 0:
            return "⚠️ Quantity must be greater than or equal to 0"

        # Update stock
        try:
            Furniture.update_stock(product_id, quantity)
            return f"Stock updated successfully for product {product_id}."
        except Exception as e:
            return f"⚠️ An error occurred: {str(e)}"

    @staticmethod
    def get_all_products():
        """Get all products."""
        query = """
        SELECT * FROM Products
        ORDER BY Name
        """
        try:
            return execute_query(query, fetch=True) or []
        except Exception:
            return []

    @staticmethod
    def search_products(search_term):
        """Search products by name or description."""
        if not search_term:
            return []

        query = """
        SELECT * FROM Products
        WHERE Name LIKE ? OR Description LIKE ?
        ORDER BY Name
        """
        search_pattern = f"%{search_term}%"
        try:
            return execute_query(query, (search_pattern, search_pattern), fetch=True) or []
        except Exception:
            return []

    @staticmethod
    def get_products_by_category(category_id):
        """Get products by category."""
        if not category_id:
            return []

        query = """
        SELECT * FROM Products
        WHERE CategoryID = ?
        ORDER BY Name
        """
        try:
            return execute_query(query, (category_id,), fetch=True) or []
        except Exception:
            return []

    @staticmethod
    def get_products_by_furniture_type(furniture_type):
        """Get products by furniture type."""
        if not furniture_type:
            return []

        query = """
        SELECT * FROM Products
        WHERE FurnitureType = ?
        ORDER BY Name
        """
        try:
            return execute_query(query, (furniture_type,), fetch=True) or []
        except Exception:
            return []
