import unittest
from unittest.mock import patch, MagicMock
from app.models.order import Order

class TestOrderModel(unittest.TestCase):

    @patch('app.models.order.execute_query')
    def test_add_order_success(self, mock_execute_query):
        # Simulate query result with order ID included
        mock_execute_query.return_value = [(1,)]

        
        order = Order(1, 500, "pending")
        order_id = order.add_order()

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("INSERT INTO Orders", call_args[0])

        # Verify that the query parameters contain the request data.
        params = call_args[1]
        self.assertEqual(params[0], 1)  
        self.assertEqual(params[1], 500)  
        self.assertEqual(params[2], "pending")  

       
        self.assertEqual(order_id, 1)

    @patch('app.models.order.execute_query')
    def test_add_order_no_result(self, mock_execute_query):
        # Simulate query result without any results
        mock_execute_query.return_value = []

        
        order = Order(1, 500, "pending")
        order_id = order.add_order()

     
        mock_execute_query.assert_called_once()

        
        self.assertIsNone(order_id)

    @patch('app.models.order.execute_query')
    def test_update_order(self, mock_execute_query):
        
        mock_execute_query.return_value = None

        
        order = Order(1, 600, "shipped")
        order.update_order(1)

        # Verify that execute_query is called with the correct parameters.
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("UPDATE Orders", call_args[0])

        
        params = call_args[1]
        self.assertEqual(params[0], "shipped")  
        self.assertEqual(params[1], 600)  
        self.assertEqual(params[2], 1)  

    @patch('app.models.order.execute_query')
    def test_delete_order(self, mock_execute_query):
        
        mock_execute_query.return_value = None

        
        order = Order(1, 500, "pending")
        order.delete_order(1)

        
        self.assertEqual(mock_execute_query.call_count, 2)

        
        first_call_args = mock_execute_query.call_args_list[0][0]
        self.assertIn("DELETE FROM OrderItems WHERE OrderID = ?", first_call_args[0])
        self.assertEqual(first_call_args[1], (1,))

       
        second_call_args = mock_execute_query.call_args_list[1][0]
        self.assertIn("DELETE FROM Orders WHERE OrderID = ?", second_call_args[0])
        self.assertEqual(second_call_args[1], (1,))

    @patch('app.models.order.execute_query')
    def test_get_order_by_id(self, mock_execute_query):
        
        mock_execute_query.return_value = [{
            "OrderID": 1,
            "UserID": 1,
            "TotalAmount": 500,
            "Status": "pending",
            "UserName": "Test User",
            "UserEmail": "test@example.com"
        }]

        # Call the get request function by id
        order = Order.get_order_by_id(1)

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("SELECT o.*, u.Name as UserName, u.Email as UserEmail", call_args[0])
        self.assertEqual(call_args[1], (1,))

        
        self.assertEqual(order["OrderID"], 1)
        self.assertEqual(order["TotalAmount"], 500)
        self.assertEqual(order["Status"], "pending")
        self.assertEqual(order["UserName"], "Test User")

    @patch('app.models.order.execute_query')
    def test_get_order_by_id_not_found(self, mock_execute_query):
       
        mock_execute_query.return_value = []

        
        order = Order.get_order_by_id(999)

        mock_execute_query.assert_called_once()

       
        self.assertIsNone(order)

    @patch('app.models.order.execute_query')
    def test_get_order_items(self, mock_execute_query):
       
        mock_execute_query.return_value = [
            {
                "OrderItemID": 1,
                "OrderID": 1,
                "ProductID": 101,
                "Quantity": 2,
                "Price": 100,
                "ProductName": "Chair",
                "ProductImage": "/images/chair.jpg",
                "FurnitureType": "Chair"
            },
            {
                "OrderItemID": 2,
                "OrderID": 1,
                "ProductID": 102,
                "Quantity": 1,
                "Price": 300,
                "ProductName": "Table",
                "ProductImage": "/images/table.jpg",
                "FurnitureType": "Table"
            }
        ]

        # Call the function to get the request elements
        items = Order.get_order_items(1)

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("SELECT oi.*, p.Name as ProductName, p.ImageURL as ProductImage", call_args[0])
        self.assertEqual(call_args[1], (1,))

        
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["ProductName"], "Chair")
        self.assertEqual(items[1]["ProductName"], "Table")
        self.assertEqual(items[0]["Quantity"], 2)
        self.assertEqual(items[1]["Quantity"], 1)

    @patch('app.models.order.execute_query')
    def test_get_orders_by_user(self, mock_execute_query):
     
        mock_execute_query.return_value = [
            {
                "OrderID": 1,
                "UserID": 1,
                "TotalAmount": 500,
                "Status": "pending",
                "ItemCount": 3
            },
            {
                "OrderID": 2,
                "UserID": 1,
                "TotalAmount": 300,
                "Status": "shipped",
                "ItemCount": 2
            }
        ]

       
        orders = Order.get_orders_by_user(1)

       
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        self.assertIn("SELECT o.*, COUNT(oi.OrderItemID) as ItemCount", call_args[0])
        self.assertEqual(call_args[1], (1,))

        
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]["OrderID"], 1)
        self.assertEqual(orders[1]["OrderID"], 2)
        self.assertEqual(orders[0]["TotalAmount"], 500)
        self.assertEqual(orders[1]["TotalAmount"], 300)
        self.assertEqual(orders[0]["ItemCount"], 3)
        self.assertEqual(orders[1]["ItemCount"], 2)

    @patch('app.models.order.execute_query')
    def test_get_orders_by_status(self, mock_execute_query):
        
        mock_execute_query.return_value = [
            {
                "OrderID": 1,
                "UserID": 1,
                "TotalAmount": 500,
                "Status": "pending",
                "UserName": "User 1"
            },
            {
                "OrderID": 3,
                "UserID": 2,
                "TotalAmount": 700,
                "Status": "pending",
                "UserName": "User 2"
            }
        ]

        
        orders = Order.get_orders_by_status("pending")

       
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("SELECT o.*, u.Name as UserName", call_args[0])
        self.assertEqual(call_args[1], ("pending",))

       
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]["OrderID"], 1)
        self.assertEqual(orders[1]["OrderID"], 3)
        self.assertEqual(orders[0]["Status"], "pending")
        self.assertEqual(orders[1]["Status"], "pending")
        self.assertEqual(orders[0]["UserName"], "User 1")
        self.assertEqual(orders[1]["UserName"], "User 2")

    @patch('app.models.order.execute_query')
    def test_update_order_status(self, mock_execute_query):
       
        mock_execute_query.side_effect = [
            None,  
            [{"OrderID": 1, "UserID": 1, "TotalAmount": 400}] 
        ]

       
        Order.update_order_status(1, "shipped")

        # Check that execute_query is called twice.
        self.assertEqual(mock_execute_query.call_count, 2)

        
        first_call_args = mock_execute_query.call_args_list[0][0]
        self.assertIn("UPDATE Orders", first_call_args[0])
        self.assertEqual(first_call_args[1], ("shipped", 1))

if __name__ == '__main__':
    unittest.main()
