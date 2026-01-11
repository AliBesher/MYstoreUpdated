# Furniture Store E-Commerce API

A complete backend API for a furniture e-commerce platform implementing multiple design patterns and following best practices for software development.

## by

- Ali Besher

## Project Description

This project is a comprehensive RESTful API for a furniture e-commerce platform built using Flask. The API supports all essential e-commerce operations including user management, product browsing, shopping cart functionality, checkout process, and order management.

### Features

- **User Management**: Registration, authentication, and profile management
- **Product Catalog**: Browse and search furniture items by various criteria
- **Shopping Cart**: Add, update, remove items, and apply discounts
- **Checkout Process**: Secure payment processing and order creation
- **Order Management**: Track, update, and manage orders

### Design Patterns Implemented

- **Factory Pattern**: For creating different types of furniture objects
- **Strategy Pattern**: For implementing various discount strategies
- **Observer Pattern**: For handling order status notifications and inventory updates
- **Singleton Pattern**: For database connection management

### Architecture

The application follows a layered architecture:
- **Routes Layer**: Handles HTTP requests and responses
- **Service Layer**: Contains business logic
- **Model Layer**: Represents data structures and database interactions
- **Database Layer**: Manages database connections and query execution

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- SQL Server with ODBC Driver 17
- Git

### Dependencies

The project requires the following Python packages:
- Flask
- pyodbc
- hashlib
- uuid

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/furniture-store-api.git
   cd furniture-store-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database connection:
   Open `app/db/connection.py` and update the connection string with your SQL Server details:
   ```python
   conn_str = (
       "Driver={ODBC Driver 17 for SQL Server};"
       "Server=YOUR_SERVER_NAME;"
       "Database=FurnitureStore;"
       "Trusted_Connection=yes;"
   )
   ```

5. Run the application:
   ```bash
   python main.py
   ```

### Running Tests

To run the test suite:
```bash
python -m unittest discover tests
```

To run a specific regression test:
```bash
python -m unittest tests.regression_test
```

## API Documentation

### User Management

#### Register a new user
```
POST /api/users
```
Request body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "customer" // Optional, defaults to "customer"
}
```

#### User login
```
POST /api/login
```
Request body:
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

#### Get user profile
```
GET /api/users/{user_id}
```

#### Update user profile
```
PUT /api/users/{user_id}
```
Request body:
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "password": "newpassword123" // Optional
}
```

#### Reset password
```
POST /api/users/{user_id}/reset-password
```
Request body:
```json
{
  "new_password": "newpassword123"
}
```

### Product Management

#### Get all products
```
GET /api/products
```

#### Get products by category
```
GET /api/products?category_id={category_id}
```

#### Get products by furniture type
```
GET /api/products?furniture_type={furniture_type}
```

#### Search products
```
GET /api/products?search={search_term}
```

#### Get product by ID
```
GET /api/products/{product_id}
```

#### Add new product
```
POST /api/products
```
Request body:
```json
{
  "name": "Office Chair",
  "description": "Comfortable office chair",
  "price": 199.99,
  "dimensions": "60x60x100",
  "stock_quantity": 10,
  "category_id": 1,
  "image_url": "/images/office-chair.jpg",
  "furniture_type": "Chair",
  "has_armrests": true,
  "is_adjustable": true,
  "max_weight_capacity": 120
}
```

#### Update product
```
PUT /api/products/{product_id}
```

#### Delete product
```
DELETE /api/products/{product_id}
```

### Shopping Cart

#### View cart contents
```
GET /api/cart?user_id={user_id}
```

#### Add item to cart
```
POST /api/cart
```
Request body:
```json
{
  "user_id": 1,
  "product_id": 101,
  "quantity": 2
}
```

#### Update item quantity
```
PUT /api/cart/{product_id}
```
Request body:
```json
{
  "user_id": 1,
  "quantity": 3
}
```

#### Remove item from cart
```
DELETE /api/cart/{product_id}
```
Request body:
```json
{
  "user_id": 1
}
```

#### Clear cart
```
POST /api/cart/clear
```
Request body:
```json
{
  "user_id": 1
}
```

#### Apply discount
```
POST /api/cart/discount
```
Request body:
```json
{
  "user_id": 1,
  "discount_type": "percentage",
  "percentage": 10
}
```
For Buy One Get One Free:
```json
{
  "user_id": 1,
  "discount_type": "buy_one_get_one",
  "eligible_categories": [1, 2]
}
```
For Bulk Discount:
```json
{
  "user_id": 1,
  "discount_type": "bulk",
  "threshold": 5,
  "percentage": 15
}
```

### Checkout and Orders

#### Process checkout
```
POST /api/checkout
```
Request body:
```json
{
  "user_id": 1
}
```

#### Process payment
```
POST /api/checkout/payment
```
Request body:
```json
{
  "order_id": 1,
  "payment_method": "credit_card",
  "payment_details": {
    "card_number": "**** **** **** 1234",
    "expiry": "12/25",
    "cvv": "***"
  }
}
```

#### Get user's orders
```
GET /api/orders?user_id={user_id}
```

#### Get order details
```
GET /api/orders/{order_id}
```

#### Update order status
```
PUT /api/orders/{order_id}/status
```
Request body:
```json
{
  "status": "shipped" // Possible values: "pending", "processing", "shipped", "delivered", "cancelled"
}
```

## Error Handling

The API uses consistent error responses with appropriate HTTP status codes:

- `400 Bad Request`: For invalid input data
- `401 Unauthorized`: For authentication failures
- `404 Not Found`: When requested resources don't exist
- `500 Internal Server Error`: For server-side errors

Error response format:
```json
{
  "message": "Error description"
}
```

