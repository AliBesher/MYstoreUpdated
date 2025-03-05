# Online Furniture Store

A web application for an online furniture store with inventory management, shopping cart, and order processing capabilities.

## Project Overview

This project implements an online furniture store with the following features:
- Multiple furniture types (Chair, Table, Sofa, Bed, Cabinet)
- User authentication and management
- Shopping cart with discount strategies
- Checkout process
- Order management and tracking
- RESTful API

## Design Patterns Used

1. **Factory Pattern**: Used in FurnitureFactory to create different types of furniture objects
2. **Strategy Pattern**: Used in discount calculation for the shopping cart
3. **Observer Pattern**: Used for order notifications and inventory updates
4. **Repository Pattern**: Used for data access abstraction

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Microsoft SQL Server
- ODBC Driver for SQL Server

### Installation

1. Clone the repository: git clone https://github.com/AliBesher/online-furniture-store.git
cd online-furniture-store

2. Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Configure the database:
- Create a new database in SQL Server
- Run the SQL scripts in `sql/create_tables.sql` to create the tables
- Update the connection string in `app/db/connection.py` with your database details

5. Run the application:
python main.py

## API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products?category_id=<id>` - Get products by category
- `GET /api/products?furniture_type=<type>` - Get products by furniture type
- `GET /api/products?search=<term>` - Search products
- `GET /api/products/<id>` - Get product by ID
- `POST /api/products` - Add new product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Users
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get user by ID
- `POST /api/users` - Add new user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user
- `POST /api/login` - User login

### Cart
- `GET /api/cart?user_id=<id>` - Get user's cart
- `POST /api/cart` - Add to cart
- `PUT /api/cart/<product_id>` - Update cart item
- `DELETE /api/cart/<product_id>` - Remove from cart
- `POST /api/cart/clear` - Clear cart
- `POST /api/cart/discount` - Apply discount

### Orders
- `GET /api/orders?user_id=<id>` - Get user's orders
- `GET /api/orders/<id>` - Get order details
- `POST /api/orders` - Create new order
- `PUT /api/orders/<id>/status` - Update order status
- `DELETE /api/orders/<id>` - Delete order

### Checkout
- `POST /api/checkout` - Process checkout
- `POST /api/checkout/payment` - Process payment

## Contributors
- Ali Besher

## License
This project is licensed under the MIT License - see the LICENSE file for details.
This completes the implementation of the online furniture store project according to the requirements. The key highlights include:

Object-Oriented Design: Using inheritance for furniture types with proper abstraction
Design Patterns: Implementing Factory, Strategy, Observer, and Repository patterns
RESTful API: Well-structured API endpoints for all functionality
Security: Password hashing and token-based authentication
Code Organization: Clear separation of concerns with models, services, and routes


