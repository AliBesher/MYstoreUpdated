import unittest
from unittest.mock import patch
from app import create_app
from app.services.product_service import ProductService

class TestProductRoutes(unittest.TestCase):

    def setUp(self):
        # Create Flask app in test mode
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    # --------------------------
    # Test adding a product
    # --------------------------
    @patch('app.services.product_service.ProductService.add_product')
    def test_add_product_success(self, mock_add_product):
        # Mock successful product addition
        mock_add_product.return_value = "Product 'Test Chair' added successfully."

        # Test data
        data = {
            "name": "Test Chair",
            "description": "A test chair",
            "price": 199.99,
            "dimensions": "50x50x100",
            "stock_quantity": 10,
            "category_id": 1,
            "image_url": "/images/test-chair.jpg",
            "furniture_type": "Chair",
            "has_armrests": True,
            "is_adjustable": False,
            "max_weight_capacity": 120
        }

        # Send POST request
        response = self.client.post('/api/products', json=data)

        # Verify results
        self.assertEqual(response.status_code, 201)
        self.assertIn("added successfully", response.json["message"])

    @patch('app.services.product_service.ProductService.add_product')
    def test_add_product_invalid_price(self, mock_add_product):
        # Mock invalid price error
        mock_add_product.return_value = "⚠️ Price must be greater than 0"

        # Test data with negative price
        data = {
            "name": "Test Chair",
            "description": "A test chair",
            "price": -50,
            "dimensions": "50x50x100",
            "stock_quantity": 10,
            "category_id": 1,
            "image_url": "/images/test-chair.jpg",
            "furniture_type": "Chair"
        }

        # Send POST request
        response = self.client.post('/api/products', json=data)

        # Verify results - expecting 400 Bad Request for invalid data
        self.assertEqual(response.status_code, 400)
        self.assertIn("Price must be greater than 0", response.json["message"])

    # --------------------------
    # Test updating a product
    # --------------------------
    @patch('app.services.product_service.ProductService.update_product')
    def test_update_product_success(self, mock_update_product):
        # Mock successful product update
        mock_update_product.return_value = "Product 'Updated Chair' updated successfully."

        # Test data
        data = {
            "name": "Updated Chair",
            "description": "An updated test chair",
            "price": 249.99,
            "dimensions": "60x60x120",
            "stock_quantity": 15,
            "category_id": 1,
            "image_url": "/images/updated-chair.jpg",
            "furniture_type": "Chair",
            "has_armrests": True,
            "is_adjustable": True,
            "max_weight_capacity": 150
        }

        # Send PUT request
        response = self.client.put('/api/products/1', json=data)

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertIn("updated successfully", response.json["message"])

    # --------------------------
    # Test deleting a product
    # --------------------------
    @patch('app.services.product_service.ProductService.delete_product')
    def test_delete_product(self, mock_delete_product):
        # Mock successful product deletion
        mock_delete_product.return_value = "Product deleted successfully."

        # Send DELETE request
        response = self.client.delete('/api/products/1')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.json["message"])

    # --------------------------
    # Test getting all products
    # --------------------------
    @patch('app.services.product_service.ProductService.get_all_products')
    def test_get_all_products(self, mock_get_all):
        # Mock product list
        mock_get_all.return_value = [
            {"ProductID": 1, "Name": "Chair", "Price": 199.99},
            {"ProductID": 2, "Name": "Table", "Price": 299.99}
        ]

        # Send GET request
        response = self.client.get('/api/products')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["products"]), 2)

    # --------------------------
    # Test getting products by category
    # --------------------------
    @patch('app.services.product_service.ProductService.get_products_by_category')
    def test_get_products_by_category(self, mock_get_by_category):
        # Mock products in category
        mock_get_by_category.return_value = [
            {"ProductID": 1, "Name": "Chair", "Price": 199.99, "CategoryID": 1},
            {"ProductID": 3, "Name": "Stool", "Price": 99.99, "CategoryID": 1}
        ]

        # Send GET request with category filter
        response = self.client.get('/api/products?category_id=1')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["products"]), 2)
        self.assertEqual(response.json["products"][0]["Name"], "Chair")

    # --------------------------
    # Test getting products by furniture type
    # --------------------------
    @patch('app.services.product_service.ProductService.get_products_by_furniture_type')
    def test_get_products_by_furniture_type(self, mock_get_by_type):
        # Mock products of specific type
        mock_get_by_type.return_value = [
            {"ProductID": 1, "Name": "Chair A", "Price": 199.99, "FurnitureType": "Chair"},
            {"ProductID": 4, "Name": "Chair B", "Price": 249.99, "FurnitureType": "Chair"}
        ]

        # Send GET request with furniture type filter
        response = self.client.get('/api/products?furniture_type=Chair')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["products"]), 2)
        self.assertEqual(response.json["products"][0]["FurnitureType"], "Chair")

    # --------------------------
    # Test searching products
    # --------------------------
    @patch('app.services.product_service.ProductService.search_products')
    def test_search_products(self, mock_search):
        # Mock search results
        mock_search.return_value = [
            {"ProductID": 1, "Name": "Office Chair", "Description": "Comfortable office chair"},
            {"ProductID": 5, "Name": "Gaming Chair", "Description": "Ergonomic gaming chair"}
        ]

        # Send GET request with search term
        response = self.client.get('/api/products?search=chair')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["products"]), 2)
        self.assertIn("Chair", response.json["products"][0]["Name"])

    # --------------------------
    # Test getting a specific product
    # --------------------------
    @patch('app.services.product_service.ProductService.get_product_by_id')
    def test_get_product_by_id_success(self, mock_get_by_id):
        # Create a mock product with to_dict method
        mock_product = unittest.mock.MagicMock()
        mock_product.to_dict.return_value = {
            "id": 1,
            "name": "Office Chair",
            "price": 199.99,
            "description": "Comfortable office chair",
            "furniture_type": "Chair"
        }
        mock_get_by_id.return_value = mock_product

        # Send GET request for specific product
        response = self.client.get('/api/products/1')

        # Verify results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["product"]["id"], 1)
        self.assertEqual(response.json["product"]["name"], "Office Chair")

    @patch('app.services.product_service.ProductService.get_product_by_id')
    def test_get_product_by_id_not_found(self, mock_get_by_id):
        # Mock product not found
        mock_get_by_id.return_value = None

        # Send GET request for non-existent product
        response = self.client.get('/api/products/999')

        # Verify results
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product not found", response.json["message"])

if __name__ == '__main__':
    unittest.main()
