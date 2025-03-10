import unittest
from unittest.mock import patch, MagicMock
from app.models.order_item import OrderItem

class TestOrderItemModel(unittest.TestCase):

    @patch('app.models.order_item.execute_query')
    def test_add_order_item(self, mock_execute_query):
        
        mock_execute_query.return_value = None

       
        order_item = OrderItem(1, 101, 2, 150)
        order_item.add_order_item()

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("INSERT INTO OrderItems", call_args[0])

        # Verify that the query parameters contain the request item data.
        params = call_args[1]
        self.assertEqual(params[0], 1)  
        self.assertEqual(params[1], 101) 
        self.assertEqual(params[2], 2)  
        self.assertEqual(params[3], 150) 

    @patch('app.models.order_item.execute_query')
    def test_update_order_item(self, mock_execute_query):
        
        mock_execute_query.return_value = None

        
        order_item = OrderItem(1, 101, 3, 160)
        order_item.update_order_item(1)

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("UPDATE OrderItems", call_args[0])

        # Verify that the query parameters contain updated request item data.
        params = call_args[1]
        self.assertEqual(params[0], 3)  
        self.assertEqual(params[1], 160)  
        self.assertEqual(params[2], 1)  

    @patch('app.models.order_item.execute_query')
    def test_delete_order_item(self, mock_execute_query):
     
        mock_execute_query.return_value = None

        
        OrderItem.delete_order_item(1)

        
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("DELETE FROM OrderItems WHERE OrderItemID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

    @patch('app.models.order_item.execute_query')
    def test_get_order_item(self, mock_execute_query):
     
        mock_execute_query.return_value = [{
            "OrderItemID": 1,
            "OrderID": 1,
            "ProductID": 101,
            "Quantity": 2,
            "Price": 150,
            "ProductName": "Chair"
        }]

        
        item = OrderItem.get_order_item(1)

    
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("SELECT oi.*, p.Name as ProductName", call_args[0])
        self.assertEqual(call_args[1], (1,))

        
        self.assertEqual(item["OrderItemID"], 1)
        self.assertEqual(item["ProductID"], 101)
        self.assertEqual(item["Quantity"], 2)
        self.assertEqual(item["Price"], 150)
        self.assertEqual(item["ProductName"], "Chair")

    @patch('app.models.order_item.execute_query')
    def test_get_order_item_not_found(self, mock_execute_query):
     
        mock_execute_query.return_value = []

       
        item = OrderItem.get_order_item(999)

       
        mock_execute_query.assert_called_once()

        
        self.assertIsNone(item)

    @patch('app.models.order_item.execute_query')
    def test_get_items_by_order(self, mock_execute_query):
        
        mock_execute_query.return_value = [
            {
                "OrderItemID": 1,
                "OrderID": 1,
                "ProductID": 101,
                "Quantity": 2,
                "Price": 150,
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

        
        items = OrderItem.get_items_by_order(1)

        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("SELECT oi.*, p.Name as ProductName, p.ImageURL as ProductImage", call_args[0])
        self.assertEqual(call_args[1], (1,))

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["ProductName"], "Chair")
        self.assertEqual(items[1]["ProductName"], "Table")
        self.assertEqual(items[0]["Quantity"], 2)
        self.assertEqual(items[1]["Quantity"], 1)

    @patch('app.models.order_item.execute_query')
    def test_calculate_order_total(self, mock_execute_query):
        
        mock_execute_query.return_value = [
            (600,) 
        ]

     
        total = OrderItem.calculate_order_total(1)

       
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        
        self.assertIn("SELECT SUM(Quantity * Price) as Total", call_args[0])
        self.assertEqual(call_args[1], (1,))

        
        self.assertEqual(total, 600)

    @patch('app.models.order_item.execute_query')
    def test_calculate_order_total_no_items(self, mock_execute_query):
     
        mock_execute_query.return_value = [
            (None,)  
        ]

        
        total = OrderItem.calculate_order_total(1)

       
        mock_execute_query.assert_called_once()

        
        self.assertEqual(total, 0)

if __name__ == '__main__':
    unittest.main()
