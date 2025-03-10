import unittest
from unittest.mock import patch, MagicMock
from app.models.category import Category

class TestCategoryModel(unittest.TestCase):

    @patch('app.models.category.execute_query')
    def test_add_category(self, mock_execute_query):
        # Simulate query execution
        mock_execute_query.return_value = None

        # Create a category object and add it
        category = Category("Test Category", "Test Description")
        category.add_category()

        # Verify that execute_query was called with the correct parameters
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is for inserting a new category
        self.assertIn("INSERT INTO Categories", call_args[0])

        # Verify that the query parameters contain category data
        params = call_args[1]
        self.assertEqual(params[0], "Test Category")
        self.assertEqual(params[1], "Test Description")

    @patch('app.models.category.execute_query')
    def test_update_category(self, mock_execute_query):
        # Simulate query execution
        mock_execute_query.return_value = None

        # Create a category object and update it
        category = Category("Updated Category", "Updated Description")
        category.update_category(1)

        # Verify that execute_query was called with the correct parameters
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is for updating a category
        self.assertIn("UPDATE Categories", call_args[0])

        # Verify that the query parameters contain updated category data
        params = call_args[1]
        self.assertEqual(params[0], "Updated Category")
        self.assertEqual(params[1], "Updated Description")
        self.assertEqual(params[2], 1)  # Category ID

    @patch('app.models.category.execute_query')
    def test_delete_category(self, mock_execute_query):
        # Simulate query execution
        mock_execute_query.return_value = None

        # Create a category object and delete it
        category = Category("Test Category", "Test Description")
        category.delete_category(1)

        # Verify that execute_query was called with the correct parameters
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is for deleting a category
        self.assertIn("DELETE FROM Categories WHERE CategoryID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

    @patch('app.models.category.execute_query')
    def test_get_category_by_id(self, mock_execute_query):
        # Simulate query result
        mock_execute_query.return_value = [{
            "CategoryID": 1,
            "Name": "Test Category",
            "Description": "Test Description"
        }]

        # Call the function to get a category by ID
        category = Category.get_category_by_id(1)

        # Verify that execute_query was called with the correct parameters
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is for retrieving a category
        self.assertIn("SELECT * FROM Categories WHERE CategoryID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

        # Verify the result
        self.assertEqual(category["CategoryID"], 1)
        self.assertEqual(category["Name"], "Test Category")
        self.assertEqual(category["Description"], "Test Description")

    @patch('app.models.category.execute_query')
    def test_get_category_by_id_not_found(self, mock_execute_query):
        # Simulate query result for a non-existent category
        mock_execute_query.return_value = []

        # Call the function to get a category by ID
        category = Category.get_category_by_id(999)

        # Verify that execute_query was called with the correct parameters
        mock_execute_query.assert_called_once()

        # Verify the result
        self.assertIsNone(category)

    @patch('app.models.category.execute_query')
    def test_get_all_categories(self, mock_execute_query):
        # Simulate query result
        mock_execute_query.return_value = [
            {
                "CategoryID": 1,
                "Name": "Category 1",
                "Description": "Description 1"
            },
            {
                "CategoryID": 2,
                "Name": "Category 2",
                "Description": "Description 2"
            }
        ]

        # Call the function to get all categories
        categories = Category.get_all_categories()

        # Verify that execute_query was called with the correct parameters
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is for retrieving all categories
        self.assertIn("SELECT * FROM Categories ORDER BY Name", call_args[0])

        # Verify the result
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0]["Name"], "Category 1")
        self.assertEqual(categories[1]["Name"], "Category 2")

    @patch('app.models.category.execute_query')
    def test_get_all_categories_empty(self, mock_execute_query):
        # Simulate query result for an empty category list
        mock_execute_query.return_value = []

        # Call the function to get all categories
        categories = Category.get_all_categories()

        # Verify that execute_query was called with the correct parameters
        mock_execute_query.assert_called_once()

        # Verify the result
        self.assertEqual(categories, [])

if __name__ == '__main__':
    unittest.main()
