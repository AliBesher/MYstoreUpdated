from app.db import execute_query


class Category:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def add_category(self):
        query = """
        INSERT INTO Categories (Name, Description, CreatedAt)
        VALUES (?, ?, GETDATE())
        """
        execute_query(query, (self.name, self.description))
        print(f"Category '{self.name}' added successfully.")

    def update_category(self, category_id):
        query = """
        UPDATE Categories
        SET Name = ?, Description = ?
        WHERE CategoryID = ?
        """
        execute_query(query, (self.name, self.description, category_id))
        print(f"Category '{self.name}' updated successfully.")

    def delete_category(self, category_id):
        query = "DELETE FROM Categories WHERE CategoryID = ?"
        execute_query(query, (category_id,))
        print(f"Category deleted successfully.")
        
    @staticmethod
    def get_category_by_id(category_id):
        """Get category by ID."""
        query = "SELECT * FROM Categories WHERE CategoryID = ?"
        result = execute_query(query, (category_id,), fetch=True)
        if result:
            return result[0]
        return None
        
    @staticmethod
    def get_all_categories():
        """Get all categories."""
        query = "SELECT * FROM Categories ORDER BY Name"
        return execute_query(query, fetch=True)
