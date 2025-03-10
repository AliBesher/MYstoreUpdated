import unittest
from unittest.mock import patch, MagicMock
from app.models.cart import Cart

class TestCartModel(unittest.TestCase):

    @patch('app.models.cart.execute_query')
    def test_add_to_cart_new_item(self, mock_execute_query):
        # Simulate item not in cart
        mock_execute_query.side_effect = [
            None,  
            None   
        ]

        # Create a basket object and add a new item.
        cart = Cart(1)
        cart.add_to_cart(101, 2)

        # Check that execute_query is called twice.
        self.assertEqual(mock_execute_query.call_count, 2)

        # Verify second call (insert new item)
        second_call_args = mock_execute_query.call_args_list[1][0]
        self.assertIn("INSERT INTO Cart", second_call_args[0])
        self.assertEqual(second_call_args[1][0], 1)  
        self.assertEqual(second_call_args[1][1], 101)  
        self.assertEqual(second_call_args[1][2], 2)  

    @patch('app.models.cart.Cart.get_cart_item')
    @patch('app.models.cart.Cart.update_cart')
    def test_add_to_cart_existing_item(self, mock_update_cart, mock_get_cart_item):
        # Simulate the item being in the cart
        mock_get_cart_item.return_value = {
            "CartID": 1,
            "UserID": 1,
            "ProductID": 101,
            "Quantity": 3
        }

        
        mock_update_cart.return_value = None

        # Create a basket object and add an existing item
        cart = Cart(1)
        cart.add_to_cart(101, 2)

        
        mock_get_cart_item.assert_called_once_with(101)

       
        mock_update_cart.assert_called_once_with(101, 5)  

    def test_add_to_cart_invalid_quantity(self):
        # Create a basket object
        cart = Cart(1)

        # Attempt to add an item with an invalid quantity (0 or negative)
        with self.assertRaises(ValueError) as context:
            cart.add_to_cart(101, 0)

        self.assertIn("Quantity must be greater than 0", str(context.exception))

        with self.assertRaises(ValueError) as context:
            cart.add_to_cart(101, -1)

        self.assertIn("Quantity must be greater than 0", str(context.exception))

    @patch('app.models.cart.execute_query')
    def test_update_cart_success(self, mock_execute_query):
        # Simulate sequential results: get_cart_item then update
        mock_execute_query.side_effect = [
            [{"CartID": 1, "ProductID": 101, "Quantity": 2}],  # get_cart_item result
            None 
        ]

        # Create the basket object and update the item quantity.
        cart = Cart(1)
        cart.update_cart(101, 5)

        
        self.assertEqual(mock_execute_query.call_count, 2)

        # Verify second recall (quantity update)
        second_call_args = mock_execute_query.call_args_list[1][0]
        self.assertIn("UPDATE Cart", second_call_args[0])
        self.assertEqual(second_call_args[1][0], 5)  
        self.assertEqual(second_call_args[1][1], 1)  
        self.assertEqual(second_call_args[1][2], 101)  

    def test_update_cart_invalid_quantity(self):
        # Create a basket object
        cart = Cart(1)

        # Attempt to update an item with an invalid quantity (0 or negative)
        with self.assertRaises(ValueError) as context:
            cart.update_cart(101, 0)

        self.assertIn("Quantity must be greater than 0", str(context.exception))

        with self.assertRaises(ValueError) as context:
            cart.update_cart(101, -1)

        self.assertIn("Quantity must be greater than 0", str(context.exception))

    @patch('app.models.cart.Cart.get_cart_item')
    def test_update_cart_item_not_found(self, mock_get_cart_item):
        # Simulate item not in cart
        mock_get_cart_item.return_value = None

        
        cart = Cart(1)

        # Trying to update a non-existent item
        with self.assertRaises(ValueError) as context:
            cart.update_cart(101, 5)

        self.assertIn("Product not found in cart", str(context.exception))
        mock_get_cart_item.assert_called_once_with(101)

    @patch('app.models.cart.execute_query')
    def test_remove_from_cart_success(self, mock_execute_query):
        # Simulate sequential results: get_cart_item then delete
        mock_execute_query.side_effect = [
            [{"CartID": 1, "ProductID": 101, "Quantity": 2}],  
            None  #result delete
        ]

        # Create a basket object and remove an item
        cart = Cart(1)
        cart.remove_from_cart(101)

        # Check execute_query is called twice
        self.assertEqual(mock_execute_query.call_count, 2)

        
        second_call_args = mock_execute_query.call_args_list[1][0]
        self.assertIn("DELETE FROM Cart", second_call_args[0])
        self.assertEqual(second_call_args[1][0], 1)  
        self.assertEqual(second_call_args[1][1], 101)  

    @patch('app.models.cart.Cart.get_cart_item')
    def test_remove_from_cart_item_not_found(self, mock_get_cart_item):
        # Simulate item not in cart
        mock_get_cart_item.return_value = None

        
        cart = Cart(1)

        # Attempt to remove a non-existent item
        with self.assertRaises(ValueError) as context:
            cart.remove_from_cart(101)

        self.assertIn("Product not found in cart", str(context.exception))
        mock_get_cart_item.assert_called_once_with(101)

    @patch('app.models.cart.execute_query')
    def test_clear_cart(self, mock_execute_query):
        
        mock_execute_query.return_value = None

        
        cart = Cart(1)
        cart.clear_cart()

        # Verify that execute_query is called with the correct parameters.
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is to delete all items in the basket.
        self.assertIn("DELETE FROM Cart WHERE UserID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

    @patch('app.models.cart.execute_query')
    def test_get_cart_item(self, mock_execute_query):
        
        mock_execute_query.return_value = [{
            "CartID": 1,
            "UserID": 1,
            "ProductID": 101,
            "Quantity": 2
        }]

        
        cart = Cart(1)
        item = cart.get_cart_item(101)

        # Verify that execute_query is called with the correct parameters.
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is to search for an item in the cart.
        self.assertIn("SELECT * FROM Cart WHERE UserID = ? AND ProductID = ?", call_args[0])
        self.assertEqual(call_args[1], (1, 101))

       
        self.assertEqual(item["ProductID"], 101)
        self.assertEqual(item["Quantity"], 2)

    @patch('app.models.cart.execute_query')
    def test_get_cart_item_not_found(self, mock_execute_query):
        
        mock_execute_query.return_value = []

        
        cart = Cart(1)
        item = cart.get_cart_item(999)

       
        mock_execute_query.assert_called_once()

       
        self.assertIsNone(item)

    @patch('app.models.cart.execute_query')
    def test_get_cart_items(self, mock_execute_query):
        
        mock_execute_query.return_value = [
            {
                "CartID": 1,
                "UserID": 1,
                "ProductID": 101,
                "Quantity": 2,
                "Name": "Chair",
                "Price": 100,
                "ImageURL": "/images/chair.jpg",
                "FurnitureType": "Chair",
                "CategoryID": 1
            },
            {
                "CartID": 2,
                "UserID": 1,
                "ProductID": 102,
                "Quantity": 1,
                "Name": "Table",
                "Price": 300,
                "ImageURL": "/images/table.jpg",
                "FurnitureType": "Table",
                "CategoryID": 2
            }
        ]

        
        cart = Cart(1)
        items = cart.get_cart_items()

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # Verify that the SQL query is to get all cart items with product details
        self.assertIn("SELECT c.*, p.Name, p.Price, p.ImageURL, p.FurnitureType, p.CategoryID", call_args[0])
        self.assertEqual(call_args[1], (1,))

        # Check the result
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["ProductID"], 101)
        self.assertEqual(items[1]["ProductID"], 102)
        self.assertEqual(items[0]["Name"], "Chair")
        self.assertEqual(items[1]["Name"], "Table")
        self.assertEqual(items[0]["Quantity"], 2)
        self.assertEqual(items[1]["Quantity"], 1)

    @patch('app.models.cart.execute_query')
    def test_get_cart_items_empty(self, mock_execute_query):
        
        mock_execute_query.return_value = []

        
        cart = Cart(1)
        items = cart.get_cart_items()

        
        mock_execute_query.assert_called_once()

        
        self.assertEqual(items, [])

    @patch('app.models.cart.Cart.get_cart_items')
    def test_calculate_total(self, mock_get_cart_items):
        
        mock_get_cart_items.return_value = [
            {"Price": 100, "Quantity": 2},
            {"Price": 300, "Quantity": 1}
        ]

        # Create a basket object and calculate the total amount.
        cart = Cart(1)
        total = cart.calculate_total()

        # Verify get_cart_items call
        mock_get_cart_items.assert_called_once()

        # Check the result (2*100 + 1*300 = 500)
        self.assertEqual(total, 500)

    @patch('app.models.cart.Cart.get_cart_items')
    def test_calculate_total_empty_cart(self, mock_get_cart_items):
        # Simulate the result of getting empty cart items
        mock_get_cart_items.return_value = []

        
        cart = Cart(1)
        total = cart.calculate_total()

     
        mock_get_cart_items.assert_called_once()

       
        self.assertEqual(total, 0)

if __name__ == '__main__':
    unittest.main()
