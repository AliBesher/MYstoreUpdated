from abc import ABC, abstractmethod
from app.db.execute_query import execute_query


class Furniture(ABC):
    """Base abstract class for all furniture items."""
    
    def __init__(self, name, description, price, dimensions, stock_quantity, category_id, image_url):
        self.name = name
        self.description = description
        self.price = price
        self.dimensions = dimensions
        self.stock_quantity = stock_quantity
        self.category_id = category_id
        self.image_url = image_url
        
    def add_furniture(self):
        """Add furniture to the database."""
        query = """
        INSERT INTO Products (Name, Description, Price, Dimensions, StockQuantity, CategoryID, ImageURL, FurnitureType, CreatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
        """
        execute_query(query, (
            self.name, 
            self.description, 
            self.price, 
            self.dimensions, 
            self.stock_quantity, 
            self.category_id, 
            self.image_url,
            self.get_furniture_type()
        ))
        
    def update_furniture(self, furniture_id):
        """Update furniture in the database."""
        query = """
        UPDATE Products
        SET Name = ?, Description = ?, Price = ?, Dimensions = ?, 
            StockQuantity = ?, CategoryID = ?, ImageURL = ?, FurnitureType = ?
        WHERE ProductID = ?
        """
        execute_query(query, (
            self.name, 
            self.description, 
            self.price, 
            self.dimensions, 
            self.stock_quantity, 
            self.category_id, 
            self.image_url,
            self.get_furniture_type(),
            furniture_id
        ))
        
    @staticmethod
    def delete_furniture(furniture_id):
        """Delete furniture from the database."""
        query = "DELETE FROM Products WHERE ProductID = ?"
        execute_query(query, (furniture_id,))
        
    @abstractmethod
    def get_furniture_type(self):
        """Return the type of furniture."""
        pass
        
    @abstractmethod
    def calculate_discount(self, discount_percentage):
        """Calculate discount based on furniture type."""
        pass
        
    @staticmethod
    def get_furniture_by_id(furniture_id):
        """Get furniture by ID."""
        query = "SELECT * FROM Products WHERE ProductID = ?"
        result = execute_query(query, (furniture_id,), fetch=True)
        
        if result:
            row = result[0]
            furniture_type = row['FurnitureType']
            
            # Use Factory Pattern to create appropriate furniture object
            return FurnitureFactory.create_furniture(
                furniture_type,
                row['Name'],
                row['Description'],
                row['Price'],
                row['Dimensions'],
                row['StockQuantity'],
                row['CategoryID'],
                row['ImageURL'],
                row  # Pass the entire row for additional attributes
            )
            
        return None
    
    @staticmethod
    def update_stock(furniture_id, quantity):
        """Update furniture stock."""
        query = """
        UPDATE Products
        SET StockQuantity = StockQuantity - ?
        WHERE ProductID = ?
        """
        execute_query(query, (quantity, furniture_id))
        print(f"Stock updated for product {furniture_id}.")


class Chair(Furniture):
    """Chair furniture type."""
    
    def __init__(self, name, description, price, dimensions, stock_quantity, category_id, image_url, 
                 max_weight_capacity=100, has_armrests=True, is_adjustable=False):
        super().__init__(name, description, price, dimensions, stock_quantity, category_id, image_url)
        self.max_weight_capacity = max_weight_capacity
        self.has_armrests = has_armrests
        self.is_adjustable = is_adjustable
        
    def get_furniture_type(self):
        return "Chair"
        
    def calculate_discount(self, discount_percentage):
        """Calculate discount for chairs. 
        Adjustable chairs get an additional 5% discount."""
        base_discount = self.price * (discount_percentage / 100)
        if self.is_adjustable:
            additional_discount = self.price * 0.05
            return base_discount + additional_discount
        return base_discount


class Table(Furniture):
    """Table furniture type."""
    
    def __init__(self, name, description, price, dimensions, stock_quantity, category_id, image_url,
                 shape="Rectangle", max_weight_capacity=200, is_extendable=False):
        super().__init__(name, description, price, dimensions, stock_quantity, category_id, image_url)
        self.shape = shape
        self.max_weight_capacity = max_weight_capacity
        self.is_extendable = is_extendable
        
    def get_furniture_type(self):
        return "Table"
        
    def calculate_discount(self, discount_percentage):
        """Calculate discount for tables.
        Extendable tables get an additional 3% discount."""
        base_discount = self.price * (discount_percentage / 100)
        if self.is_extendable:
            additional_discount = self.price * 0.03
            return base_discount + additional_discount
        return base_discount


class Sofa(Furniture):
    """Sofa furniture type."""
    
    def __init__(self, name, description, price, dimensions, stock_quantity, category_id, image_url,
                 seats=3, is_convertible=False, has_storage=False):
        super().__init__(name, description, price, dimensions, stock_quantity, category_id, image_url)
        self.seats = seats
        self.is_convertible = is_convertible
        self.has_storage = has_storage
        
    def get_furniture_type(self):
        return "Sofa"
        
    def calculate_discount(self, discount_percentage):
        """Calculate discount for sofas.
        Convertible sofas get an additional 7% discount."""
        base_discount = self.price * (discount_percentage / 100)
        if self.is_convertible:
            additional_discount = self.price * 0.07
            return base_discount + additional_discount
        return base_discount


class Bed(Furniture):
    """Bed furniture type."""
    
    def __init__(self, name, description, price, dimensions, stock_quantity, category_id, image_url,
                 size="Queen", has_storage=False, material_type="Wood"):
        super().__init__(name, description, price, dimensions, stock_quantity, category_id, image_url)
        self.size = size
        self.has_storage = has_storage
        self.material_type = material_type
        
    def get_furniture_type(self):
        return "Bed"
        
    def calculate_discount(self, discount_percentage):
        """Calculate discount for beds.
        Storage beds get an additional 4% discount."""
        base_discount = self.price * (discount_percentage / 100)
        if self.has_storage:
            additional_discount = self.price * 0.04
            return base_discount + additional_discount
        return base_discount


class Cabinet(Furniture):
    """Cabinet furniture type."""
    
    def __init__(self, name, description, price, dimensions, stock_quantity, category_id, image_url,
                 num_drawers=0, num_shelves=0, has_lock=False):
        super().__init__(name, description, price, dimensions, stock_quantity, category_id, image_url)
        self.num_drawers = num_drawers
        self.num_shelves = num_shelves
        self.has_lock = has_lock
        
    def get_furniture_type(self):
        return "Cabinet"
        
    def calculate_discount(self, discount_percentage):
        """Calculate discount for cabinets.
        Cabinets with locks get an additional 2% discount."""
        base_discount = self.price * (discount_percentage / 100)
        if self.has_lock:
            additional_discount = self.price * 0.02
            return base_discount + additional_discount
        return base_discount


# Factory Pattern implementation
class FurnitureFactory:
    """Factory class for creating furniture objects."""
    
    @staticmethod
    def create_furniture(furniture_type, name, description, price, dimensions, stock_quantity, category_id, image_url, additional_data=None):
        """Create and return a furniture object based on the type."""
        if furniture_type == "Chair":
            return Chair(
                name, description, price, dimensions, stock_quantity, category_id, image_url,
                additional_data.get('max_weight_capacity', 100) if additional_data else 100,
                additional_data.get('has_armrests', True) if additional_data else True,
                additional_data.get('is_adjustable', False) if additional_data else False
            )
        elif furniture_type == "Table":
            return Table(
                name, description, price, dimensions, stock_quantity, category_id, image_url,
                additional_data.get('shape', "Rectangle") if additional_data else "Rectangle",
                additional_data.get('max_weight_capacity', 200) if additional_data else 200,
                additional_data.get('is_extendable', False) if additional_data else False
            )
        elif furniture_type == "Sofa":
            return Sofa(
                name, description, price, dimensions, stock_quantity, category_id, image_url,
                additional_data.get('seats', 3) if additional_data else 3,
                additional_data.get('is_convertible', False) if additional_data else False,
                additional_data.get('has_storage', False) if additional_data else False
            )
        elif furniture_type == "Bed":
            return Bed(
                name, description, price, dimensions, stock_quantity, category_id, image_url,
                additional_data.get('size', "Queen") if additional_data else "Queen",
                additional_data.get('has_storage', False) if additional_data else False,
                additional_data.get('material_type', "Wood") if additional_data else "Wood"
            )
        elif furniture_type == "Cabinet":
            return Cabinet(
                name, description, price, dimensions, stock_quantity, category_id, image_url,
                additional_data.get('num_drawers', 0) if additional_data else 0,
                additional_data.get('num_shelves', 0) if additional_data else 0,
                additional_data.get('has_lock', False) if additional_data else False
            )
        else:
            raise ValueError(f"Unknown furniture type: {furniture_type}")
