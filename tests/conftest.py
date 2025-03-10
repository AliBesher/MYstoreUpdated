# tests/conftest.py
"""
ملف إعداد لـ pytest يقوم بتطبيق محاكاة قاعدة البيانات تلقائياً.
"""

import pytest
from app.db.mock_db import apply_mock, restore_original

@pytest.fixture(scope="session", autouse=True)
def setup_database_mock():
    """
    تطبيق محاكاة قاعدة البيانات قبل تشغيل الاختبارات واستعادة الدالة الأصلية بعد الانتهاء.
    """
    # تطبيق المحاكاة
    original_function = apply_mock()
    
    # إرجاع التحكم للاختبارات
    yield
    
    # استعادة الدالة الأصلية
    restore_original(original_function)

@pytest.fixture
def mock_user():
    """
    توفير بيانات مستخدم للاختبارات.
    """
    return {
        "UserID": 1,
        "Name": "Test User",
        "Email": "test@example.com",
        "Role": "customer"
    }

@pytest.fixture
def mock_product():
    """
    توفير بيانات منتج للاختبارات.
    """
    return {
        "ProductID": 1,
        "Name": "Test Chair",
        "Description": "A comfortable test chair",
        "Price": 200.0,
        "StockQuantity": 10,
        "CategoryID": 1,
        "FurnitureType": "Chair"
    }

@pytest.fixture
def mock_cart_items():
    """
    توفير بيانات سلة للاختبارات.
    """
    return [
        {
            "CartID": 1,
            "UserID": 1,
            "ProductID": 1,
            "Quantity": 2,
            "Name": "Test Chair",
            "Price": 200.0,
            "ImageURL": "/images/chair.jpg",
            "FurnitureType": "Chair",
            "CategoryID": 1
        }
    ]

@pytest.fixture
def mock_order():
    """
    توفير بيانات طلب للاختبارات.
    """
    return {
        "OrderID": 1,
        "UserID": 1,
        "TotalAmount": 400.0,
        "Status": "pending",
        "CreatedAt": "2023-05-01"
    }
