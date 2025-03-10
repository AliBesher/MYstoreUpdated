import unittest
from unittest.mock import patch, MagicMock
from app.models.furniture import (
    Furniture, Chair, Table, Sofa, Bed, Cabinet, FurnitureFactory
)

class TestFurnitureModel(unittest.TestCase):

    # Chair category tests
    @patch('app.models.furniture.execute_query')
    def test_chair_add_furniture(self, mock_execute_query):
        
        mock_execute_query.return_value = None

        # Create and add the chair object
        chair = Chair(
            name="Office Chair",
            description="Comfortable office chair",
            price=199.99,
            dimensions="60x60x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/office-chair.jpg",
            max_weight_capacity=120,
            has_armrests=True,
            is_adjustable=True
        )
        chair.add_furniture()

        # Verify that execute_query is called with the correct parameters.
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is to insert new furniture.
        self.assertIn("INSERT INTO Products", call_args[0])

        # Verify that the query parameters contain chair data.
        params = call_args[1]
        self.assertEqual(params[0], "Office Chair")  
        self.assertEqual(params[1], "Comfortable office chair")  
        self.assertEqual(params[2], 199.99)  
        self.assertEqual(params[3], "60x60x100")  
        self.assertEqual(params[4], 10)  
        self.assertEqual(params[5], 1)  
        self.assertEqual(params[6], "/images/office-chair.jpg")  
        self.assertEqual(params[7], "Chair") 

    def test_chair_get_furniture_type(self):
        
        chair = Chair("Test Chair", "Description", 100, "50x50x100", 5, 1, "/images/chair.jpg")

        
        self.assertEqual(chair.get_furniture_type(), "Chair")

    def test_chair_calculate_discount(self):
        
        chair_adjustable = Chair(
            "Test Chair", "Description", 100, "50x50x100", 5, 1, "/images/chair.jpg",
            is_adjustable=True
        )
        chair_not_adjustable = Chair(
            "Test Chair", "Description", 100, "50x50x100", 5, 1, "/images/chair.jpg",
            is_adjustable=False
        )

        # Adjustable chair gets an extra 5% discount
        discount_adjustable = chair_adjustable.calculate_discount(10)
        
        self.assertEqual(discount_adjustable, 15)

        # Non-adjustable chair only gets basic discount
        discount_not_adjustable = chair_not_adjustable.calculate_discount(10)
        
        self.assertEqual(discount_not_adjustable, 10)

    def test_chair_to_dict(self):
        
        chair = Chair(
            "Office Chair", "Comfortable office chair", 199.99, "60x60x100", 10, 1,
            "/images/chair.jpg", 120, True, True
        )

       
        chair_dict = chair.to_dict()

        # Check the result
        self.assertEqual(chair_dict["name"], "Office Chair")
        self.assertEqual(chair_dict["description"], "Comfortable office chair")
        self.assertEqual(chair_dict["price"], 199.99)
        self.assertEqual(chair_dict["furniture_type"], "Chair")
        self.assertEqual(chair_dict["max_weight_capacity"], 120)
        self.assertEqual(chair_dict["has_armrests"], True)
        self.assertEqual(chair_dict["is_adjustable"], True)

    # Tests for Table category
    @patch('app.models.furniture.execute_query')
    def test_table_add_furniture(self, mock_execute_query):
        
        mock_execute_query.return_value = None

        # Create and add the table object
        table = Table(
            name="Dining Table",
            description="Beautiful dining table",
            price=399.99,
            dimensions="120x80x75",
            stock_quantity=5,
            category_id=2,
            image_url="/images/dining-table.jpg",
            shape="Rectangle",
            max_weight_capacity=150,
            is_extendable=True
        )
        table.add_furniture()

        # Verify that execute_query is called with the correct parameters.
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("INSERT INTO Products", call_args[0])

        # Verify that query parameters contain table data
        params = call_args[1]
        self.assertEqual(params[0], "Dining Table") 
        self.assertEqual(params[7], "Table")  

    def test_table_get_furniture_type(self):
        
        table = Table("Test Table", "Description", 300, "120x80x75", 5, 2, "/images/table.jpg")

        
        self.assertEqual(table.get_furniture_type(), "Table")

    def test_table_calculate_discount(self):
        
        table_extendable = Table(
            "Test Table", "Description", 300, "120x80x75", 5, 2, "/images/table.jpg",
            is_extendable=True
        )
        table_not_extendable = Table(
            "Test Table", "Description", 300, "120x80x75", 5, 2, "/images/table.jpg",
            is_extendable=False
        )

        # Extendable table gets an additional 3% discount
        discount_extendable = table_extendable.calculate_discount(10)
        
        self.assertEqual(discount_extendable, 39)

        # Non-extendable table only gets basic discount
        discount_not_extendable = table_not_extendable.calculate_discount(10)
        
        self.assertEqual(discount_not_extendable, 30)

    # Sofa category tests
    def test_sofa_get_furniture_type(self):
        
        sofa = Sofa("Test Sofa", "Description", 500, "200x90x85", 3, 3, "/images/sofa.jpg")

       
        self.assertEqual(sofa.get_furniture_type(), "Sofa")

    def test_sofa_calculate_discount(self):
       
        sofa_convertible = Sofa(
            "Test Sofa", "Description", 500, "200x90x85", 3, 3, "/images/sofa.jpg",
            is_convertible=True
        )
        sofa_not_convertible = Sofa(
            "Test Sofa", "Description", 500, "200x90x85", 3, 3, "/images/sofa.jpg",
            is_convertible=False
        )

        #Convertible sofa gets an extra 7% off
        discount_convertible = sofa_convertible.calculate_discount(10)
        
        self.assertEqual(discount_convertible, 85)

        # Non-convertible sofa only gets basic discount
        discount_not_convertible = sofa_not_convertible.calculate_discount(10)
        
        self.assertEqual(discount_not_convertible, 50)

    # Bed category tests
    def test_bed_get_furniture_type(self):
        
        bed = Bed("Test Bed", "Description", 600, "200x180x60", 2, 4, "/images/bed.jpg")

        
        self.assertEqual(bed.get_furniture_type(), "Bed")

    def test_bed_calculate_discount(self):
       
        bed_with_storage = Bed(
            "Test Bed", "Description", 600, "200x180x60", 2, 4, "/images/bed.jpg",
            has_storage=True
        )
        bed_without_storage = Bed(
            "Test Bed", "Description", 600, "200x180x60", 2, 4, "/images/bed.jpg",
            has_storage=False
        )

        # Bed with storage gets an additional 4% discount
        discount_with_storage = bed_with_storage.calculate_discount(10)
      
        self.assertEqual(discount_with_storage, 84)

        # Bed without storage gets only basic discount
        discount_without_storage = bed_without_storage.calculate_discount(10)
        
        self.assertEqual(discount_without_storage, 60)

    # Cabinet class tests
    def test_cabinet_get_furniture_type(self):
       
        cabinet = Cabinet("Test Cabinet", "Description", 400, "120x50x180", 4, 5, "/images/cabinet.jpg")

       
        self.assertEqual(cabinet.get_furniture_type(), "Cabinet")

    def test_cabinet_calculate_discount(self):
       
        cabinet_with_lock = Cabinet(
            "Test Cabinet", "Description", 400, "120x50x180", 4, 5, "/images/cabinet.jpg",
            has_lock=True
        )
        cabinet_without_lock = Cabinet(
            "Test Cabinet", "Description", 400, "120x50x180", 4, 5, "/images/cabinet.jpg",
            has_lock=False
        )

        # Locker with lock get extra 2% discount
        discount_with_lock = cabinet_with_lock.calculate_discount(10)
        # 10% basic discount ($40) + 2% additional discount ($8) = $48
        self.assertEqual(discount_with_lock, 48)

        # Lockless safe only gets basic discount
        discount_without_lock = cabinet_without_lock.calculate_discount(10)
        # 10% off basic ($40) = $40
        self.assertEqual(discount_without_lock, 40)

    # Static Testing Methods in Furniture
    @patch('app.models.furniture.execute_query')
    def test_get_furniture_by_id(self, mock_execute_query):
       
        mock_execute_query.return_value = [{
            "ProductID": 1,
            "Name": "Office Chair",
            "Description": "Comfortable office chair",
            "Price": 199.99,
            "Dimensions": "60x60x100",
            "StockQuantity": 10,
            "CategoryID": 1,
            "ImageURL": "/images/office-chair.jpg",
            "FurnitureType": "Chair",
            "CreatedAt": "2023-04-01"
        }]

        # FurnitureFactory Simulation
        with patch('app.models.furniture.FurnitureFactory.create_furniture') as mock_create_furniture:
        
            mock_chair = Chair(
                "Office Chair", "Comfortable office chair", 199.99, "60x60x100", 10, 1,
                "/images/office-chair.jpg"
            )
            mock_create_furniture.return_value = mock_chair

         
            furniture = Furniture.get_furniture_by_id(1)

            
            mock_execute_query.assert_called_once()
            call_args = mock_execute_query.call_args[0]

           
            self.assertIn("SELECT * FROM Products WHERE ProductID = ?", call_args[0])
            self.assertEqual(call_args[1], (1,))

           
            mock_create_furniture.assert_called_once()

            
            self.assertEqual(furniture, mock_chair)

    @patch('app.models.furniture.execute_query')
    def test_update_stock(self, mock_execute_query):
        
        mock_execute_query.return_value = None

        
        Furniture.update_stock(1, 5)

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is to update the inventory.
        self.assertIn("UPDATE Products", call_args[0])
        self.assertEqual(call_args[1], (5, 1))

    # FurnitureFactory Factory Style Tests
    def test_furniture_factory_create_chair(self):
        
        chair = FurnitureFactory.create_furniture(
            furniture_type="Chair",
            name="Factory Chair",
            description="Created by factory",
            price=199.99,
            dimensions="60x60x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/chair.jpg",
            additional_data={
                "max_weight_capacity": 120,
                "has_armrests": True,
                "is_adjustable": True
            }
        )

        # Check the object type and furniture type
        self.assertIsInstance(chair, Chair)
        self.assertEqual(chair.get_furniture_type(), "Chair")
        self.assertEqual(chair.name, "Factory Chair")
        self.assertEqual(chair.max_weight_capacity, 120)
        self.assertEqual(chair.has_armrests, True)
        self.assertEqual(chair.is_adjustable, True)

    def test_furniture_factory_create_table(self):
        # Create a table using the factory
        table = FurnitureFactory.create_furniture(
            furniture_type="Table",
            name="Factory Table",
            description="Created by factory",
            price=399.99,
            dimensions="120x80x75",
            stock_quantity=5,
            category_id=2,
            image_url="/images/table.jpg",
            additional_data={
                "shape": "Round",
                "max_weight_capacity": 150,
                "is_extendable": True
            }
        )

   
        self.assertIsInstance(table, Table)
        self.assertEqual(table.get_furniture_type(), "Table")
        self.assertEqual(table.name, "Factory Table")
        self.assertEqual(table.shape, "Round")
        self.assertEqual(table.max_weight_capacity, 150)
        self.assertEqual(table.is_extendable, True)

    def test_furniture_factory_create_sofa(self):
        #Create a sofa using the factory
        sofa = FurnitureFactory.create_furniture(
            furniture_type="Sofa",
            name="Factory Sofa",
            description="Created by factory",
            price=599.99,
            dimensions="220x90x85",
            stock_quantity=3,
            category_id=3,
            image_url="/images/sofa.jpg",
            additional_data={
                "seats": 4,
                "is_convertible": True,
                "has_storage": True
            }
        )

        # Check the object type and furniture type
        self.assertIsInstance(sofa, Sofa)
        self.assertEqual(sofa.get_furniture_type(), "Sofa")
        self.assertEqual(sofa.name, "Factory Sofa")
        self.assertEqual(sofa.seats, 4)
        self.assertEqual(sofa.is_convertible, True)
        self.assertEqual(sofa.has_storage, True)

    def test_furniture_factory_create_bed(self):
        #Create a bed using a factory
        bed = FurnitureFactory.create_furniture(
            furniture_type="Bed",
            name="Factory Bed",
            description="Created by factory",
            price=699.99,
            dimensions="200x180x60",
            stock_quantity=2,
            category_id=4,
            image_url="/images/bed.jpg",
            additional_data={
                "size": "King",
                "has_storage": True,
                "material_type": "Oak"
            }
        )

        # Check the object type and furniture type
        self.assertIsInstance(bed, Bed)
        self.assertEqual(bed.get_furniture_type(), "Bed")
        self.assertEqual(bed.name, "Factory Bed")
        self.assertEqual(bed.size, "King")
        self.assertEqual(bed.has_storage, True)
        self.assertEqual(bed.material_type, "Oak")

    def test_furniture_factory_create_cabinet(self):
        # Create a cabinet using the factory
        cabinet = FurnitureFactory.create_furniture(
            furniture_type="Cabinet",
            name="Factory Cabinet",
            description="Created by factory",
            price=499.99,
            dimensions="120x50x180",
            stock_quantity=4,
            category_id=5,
            image_url="/images/cabinet.jpg",
            additional_data={
                "num_drawers": 3,
                "num_shelves": 4,
                "has_lock": True
            }
        )

        # Check the object type and furniture type
        self.assertIsInstance(cabinet, Cabinet)
        self.assertEqual(cabinet.get_furniture_type(), "Cabinet")
        self.assertEqual(cabinet.name, "Factory Cabinet")
        self.assertEqual(cabinet.num_drawers, 3)
        self.assertEqual(cabinet.num_shelves, 4)
        self.assertEqual(cabinet.has_lock, True)

    def test_furniture_factory_unknown_type(self):
        # Trying to create an unknown type of furniture
        with self.assertRaises(ValueError) as context:
            FurnitureFactory.create_furniture(
                furniture_type="Unknown",
                name="Unknown Furniture",
                description="Unknown type",
                price=100,
                dimensions="50x50x50",
                stock_quantity=1,
                category_id=1,
                image_url="/images/unknown.jpg"
            )

        self.assertIn("Unknown furniture type", str(context.exception))

    @patch('app.models.furniture.execute_query')
    def test_update_furniture(self, mock_execute_query):
       
        mock_execute_query.return_value = None

        # Create and update the chair object
        chair = Chair(
            name="Updated Chair",
            description="Updated description",
            price=249.99,
            dimensions="65x65x105",
            stock_quantity=8,
            category_id=1,
            image_url="/images/updated-chair.jpg",
            max_weight_capacity=130,
            has_armrests=True,
            is_adjustable=True
        )
        chair.update_furniture(1)

        # Verify that execute_query is called with the correct parameters.
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is to update furniture.
        self.assertIn("UPDATE Products", call_args[0])

        # Verify that the query parameters contain updated chair data.
        params = call_args[1]
        self.assertEqual(params[0], "Updated Chair")  
        self.assertEqual(params[1], "Updated description") 
        self.assertEqual(params[2], 249.99)  
        self.assertEqual(params[3], "65x65x105")  
        self.assertEqual(params[4], 8)  
        self.assertEqual(params[7], "Chair")  
        self.assertEqual(params[8], 1)  

    @patch('app.models.furniture.execute_query')
    def test_delete_furniture(self, mock_execute_query):
       
        mock_execute_query.return_value = None

  
        Furniture.delete_furniture(1)

        # Verify that execute_query is called with the correct parameters.
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is to delete furniture.
        self.assertIn("DELETE FROM Products WHERE ProductID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

if __name__ == '__main__':
    unittest.main()
