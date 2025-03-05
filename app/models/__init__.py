# app/models/__init__.py
from app.models.user import User
from app.models.furniture import (
    Furniture, Chair, Table, Sofa, Bed, Cabinet, FurnitureFactory
)
from app.models.cart import Cart
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.category import Category

# This allows imports like: from app.models import User, Cart
