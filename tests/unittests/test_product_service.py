import unittest
from unittest.mock import patch, MagicMock
from app.services.product_service import ProductService
from app.models.furniture import Chair

class TestProductService(unittest.TestCase):

    @patch('app.services.product_service.FurnitureFactory.create_furniture')
    @patch('app.models.furniture.Furniture.add_furniture')
    def test_add_product_success(self, mock_add_furniture, mock_create_furniture):
        # Mock the furniture object
        mock_chair = Chair(
            "Test Chair", "Test Description", 100, "50x50x100", 10, 1, "/images/test.jpg"
        )
        mock_create_furniture.return_value = mock_chair
        mock_add_furniture.return_value = None

        # Call the add_product method
        result = ProductService.add_product(
            name="Test Chair",
            description="Test Description",
            price=100,
            dimensions="50x50x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/test.jpg",
            furniture_type="Chair"
        )

        # Verify result
        self.assertEqual(result, "Product 'Test Chair' added successfully.")
        mock_create_furniture.assert_called_once()
        mock_add_furniture.assert_called_once()

    def test_add_product_invalid_price(self):
        # Test with invalid price
        result = ProductService.add_product(
            name="Test Chair",
            description="Test Description",
            price=-10,  # Negative price
            dimensions="50x50x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/test.jpg",
            furniture_type="Chair"
        )

        # Verify result
        self.assertEqual(result, "⚠️ Price must be greater than 0")

    def test_add_product_invalid_stock(self):
        # Test with invalid stock quantity
        result = ProductService.add_product(
            name="Test Chair",
            description="Test Description",
            price=100,
            dimensions="50x50x100",
            stock_quantity=-5,  # Negative stock
            category_id=1,
            image_url="/images/test.jpg",
            furniture_type="Chair"
        )

        # Verify result
        self.assertEqual(result, "⚠️ Stock quantity must be greater than or equal to 0")

    def test_add_product_no_name_description(self):
        # Test with missing name and description
        result = ProductService.add_product(
            name="",  # Empty name
            description="",  # Empty description
            price=100,
            dimensions="50x50x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/test.jpg",
            furniture_type="Chair"
        )

        # Verify result
        self.assertEqual(result, "⚠️ Name and description are required")

    @patch('app.services.product_service.FurnitureFactory.create_furniture')
    @patch('app.models.furniture.Furniture.add_furniture')
    def test_add_product_factory_exception(self, mock_add_furniture, mock_create_furniture):
        # Mock the factory throwing an exception
        mock_create_furniture.side_effect = ValueError("Invalid furniture type")

        # Call the add_product method
        result = ProductService.add_product(
            name="Test Chair",
            description="Test Description",
            price=100,
            dimensions="50x50x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/test.jpg",
            furniture_type="InvalidType"  # This will cause the exception
        )

        # Verify result
        self.assertEqual(result, "⚠️ Invalid furniture type")
        mock_create_furniture.assert_called_once()
        mock_add_furniture.assert_not_called()

    @patch('app.services.product_service.ProductService.get_product_by_id')
    @patch('app.services.product_service.FurnitureFactory.create_furniture')
    @patch('app.models.furniture.Furniture.update_furniture')
    def test_update_product_success(self, mock_update_furniture, mock_create_furniture, mock_get_product):
        # Mock getting existing product
        mock_product = MagicMock()
        mock_get_product.return_value = mock_product

        # Mock creating furniture
        mock_chair = Chair(
            "Updated Chair", "Updated Description", 120, "60x60x120", 15, 1, "/images/updated.jpg"
        )
        mock_create_furniture.return_value = mock_chair

        # Mock updating furniture
        mock_update_furniture.return_value = None

        # Call the update_product method
        result = ProductService.update_product(
            product_id=1,
            name="Updated Chair",
            description="Updated Description",
            price=120,
            dimensions="60x60x120",
            stock_quantity=15,
            category_id=1,
            image_url="/images/updated.jpg",
            furniture_type="Chair"
        )

        # Verify result
        self.assertEqual(result, "Product 'Updated Chair' updated successfully.")
        mock_get_product.assert_called_once_with(1)
        mock_create_furniture.assert_called_once()
        mock_update_furniture.assert_called_once_with(1)

    @patch('app.services.product_service.ProductService.get_product_by_id')
    def test_update_product_not_found(self, mock_get_product):
        # Mock product not found
        mock_get_product.return_value = None

        # Call the update_product method
        result = ProductService.update_product(
            product_id=999,
            name="Updated Chair",
            description="Updated Description",
            price=120,
            dimensions="60x60x120",
            stock_quantity=15,
            category_id=1,
            image_url="/images/updated.jpg",
            furniture_type="Chair"
        )

        # Verify result
        self.assertEqual(result, "⚠️ Product with ID 999 not found")
        mock_get_product.assert_called_once_with(999)

    def test_update_product_invalid_price(self):
        # Mock getting existing product
        with patch('app.services.product_service.ProductService.get_product_by_id') as mock_get_product:
            mock_product = MagicMock()
            mock_get_product.return_value = mock_product

            # Call the update_product method with negative price
            result = ProductService.update_product(
                product_id=1,
                name="Updated Chair",
                description="Updated Description",
                price=-120,  # Negative price
                dimensions="60x60x120",
                stock_quantity=15,
                category_id=1,
                image_url="/images/updated.jpg",
                furniture_type="Chair"
            )

            # Verify result
            self.assertEqual(result, "⚠️ Price must be greater than 0")

    @patch('app.services.product_service.ProductService.get_product_by_id')
    @patch('app.models.furniture.Furniture.delete_furniture')
    def test_delete_product_success(self, mock_delete_furniture, mock_get_product):
        # Mock getting existing product
        mock_product = MagicMock()
        mock_get_product.return_value = mock_product

        # Mock deleting furniture
        mock_delete_furniture.return_value = None

        # Call the delete_product method
        result = ProductService.delete_product(1)

        # Verify result
        self.assertEqual(result, "Product deleted successfully.")
        mock_get_product.assert_called_once_with(1)
        mock_delete_furniture.assert_called_once_with(1)

    @patch('app.services.product_service.ProductService.get_product_by_id')
    def test_delete_product_not_found(self, mock_get_product):
        # Mock product not found
        mock_get_product.return_value = None

        # Call the delete_product method
        result = ProductService.delete_product(999)

        # Verify result
        self.assertEqual(result, "⚠️ Product with ID 999 not found")
        mock_get_product.assert_called_once_with(999)

    @patch('app.models.furniture.Furniture.get_furniture_by_id')
    def test_get_product_by_id_success(self, mock_get_furniture):
        # Mock the furniture object
        mock_product = MagicMock()
        mock_get_furniture.return_value = mock_product

        # Call the get_product_by_id method
        result = ProductService.get_product_by_id(1)

        # Verify result
        self.assertEqual(result, mock_product)
        mock_get_furniture.assert_called_once_with(1)

    @patch('app.models.furniture.Furniture.get_furniture_by_id')
    def test_get_product_by_id_not_found(self, mock_get_furniture):
        # Mock product not found
        mock_get_furniture.return_value = None

        # Call the get_product_by_id method
        result = ProductService.get_product_by_id(999)

        # Verify result
        self.assertIsNone(result)
        mock_get_furniture.assert_called_once_with(999)

    def test_get_product_by_id_invalid(self):
        # Test with invalid ID
        result = ProductService.get_product_by_id(0)  # Invalid ID

        # Verify result
        self.assertIsNone(result)

    @patch('app.services.product_service.ProductService.get_product_by_id')
    @patch('app.models.furniture.Furniture.update_stock')
    def test_update_product_stock_success(self, mock_update_stock, mock_get_product):
        # Mock getting existing product
        mock_product = MagicMock()
        mock_get_product.return_value = mock_product

        # Mock updating stock
        mock_update_stock.return_value = None

        # Call the update_product_stock method
        result = ProductService.update_product_stock(1, 20)

        # Verify result
        self.assertEqual(result, "Stock updated successfully for product 1.")
        mock_get_product.assert_called_once_with(1)
        mock_update_stock.assert_called_once_with(1, 20)

    @patch('app.services.product_service.ProductService.get_product_by_id')
    def test_update_product_stock_not_found(self, mock_get_product):
        # Mock product not found
        mock_get_product.return_value = None

        # Call the update_product_stock method
        result = ProductService.update_product_stock(999, 20)

        # Verify result
        self.assertEqual(result, "⚠️ Product with ID 999 not found")
        mock_get_product.assert_called_once_with(999)

    def test_update_product_stock_invalid_quantity(self):
        # Mock getting existing product
        with patch('app.services.product_service.ProductService.get_product_by_id') as mock_get_product:
            mock_product = MagicMock()
            mock_get_product.return_value = mock_product

            # Call the update_product_stock method with negative quantity
            result = ProductService.update_product_stock(1, -10)  # Negative quantity

            # Verify result
            self.assertEqual(result, "⚠️ Quantity must be greater than or equal to 0")

    @patch('app.services.product_service.execute_query')
    def test_get_all_products(self, mock_execute_query):
        # Mock database query
        mock_products = [
            {"ProductID": 1, "Name": "Chair", "Price": 199.99},
            {"ProductID": 2, "Name": "Table", "Price": 299.99}
        ]
        mock_execute_query.return_value = mock_products

        # Call the get_all_products method
        result = ProductService.get_all_products()

        # Verify result
        self.assertEqual(result, mock_products)
        mock_execute_query.assert_called_once()

    @patch('app.services.product_service.execute_query')
    def test_get_all_products_empty(self, mock_execute_query):
        # Mock empty result
        mock_execute_query.return_value = []

        # Call the get_all_products method
        result = ProductService.get_all_products()

        # Verify result
        self.assertEqual(result, [])
        mock_execute_query.assert_called_once()

    @patch('app.services.product_service.execute_query')
    def test_search_products(self, mock_execute_query):
        # Mock database query
        mock_products = [
            {"ProductID": 1, "Name": "Office Chair", "Price": 199.99},
            {"ProductID": 5, "Name": "Gaming Chair", "Price": 299.99}
        ]
        mock_execute_query.return_value = mock_products

        # Call the search_products method
        result = ProductService.search_products("chair")

        # Verify result
        self.assertEqual(result, mock_products)
        mock_execute_query.assert_called_once()

    @patch('app.services.product_service.execute_query')
    def test_get_products_by_category(self, mock_execute_query):
        # Mock database query
        mock_products = [
            {"ProductID": 1, "Name": "Chair", "Price": 199.99, "CategoryID": 1},
            {"ProductID": 3, "Name": "Stool", "Price": 99.99, "CategoryID": 1}
        ]
        mock_execute_query.return_value = mock_products

        # Call the get_products_by_category method
        result = ProductService.get_products_by_category(1)

        # Verify result
        self.assertEqual(result, mock_products)
        mock_execute_query.assert_called_once()

    @patch('app.services.product_service.execute_query')
    def test_get_products_by_furniture_type(self, mock_execute_query):
        # Mock database query
        mock_products = [
            {"ProductID": 1, "Name": "Chair A", "Price": 199.99, "FurnitureType": "Chair"},
            {"ProductID": 4, "Name": "Chair B", "Price": 249.99, "FurnitureType": "Chair"}
        ]
        mock_execute_query.return_value = mock_products

        # Call the get_products_by_furniture_type method
        result = ProductService.get_products_by_furniture_type("Chair")

        # Verify result
        self.assertEqual(result, mock_products)
        mock_execute_query.assert_called_once()

if __name__ == '__main__':
    unittest.main()
