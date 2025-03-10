# app/db/mock_db.py
"""
وحدة محاكاة قاعدة البيانات تستخدم للاختبارات بدون اتصال حقيقي بقاعدة البيانات.
"""

from unittest.mock import MagicMock
import copy

# بيانات محاكاة للجداول المختلفة
mock_data = {
    "Users": [
        {
            "UserID": 1,
            "Name": "Test User",
            "Email": "test@example.com",
            "Password": "hashedpassword",
            "Salt": "salt123",
            "Role": "customer",
            "CreatedAt": "2023-05-01"
        }
    ],
    "Products": [
        {
            "ProductID": 1,
            "Name": "Test Chair",
            "Description": "A comfortable test chair",
            "Price": 200.0,
            "Dimensions": "60x60x100",
            "StockQuantity": 10,
            "CategoryID": 1,
            "ImageURL": "/images/chair.jpg",
            "FurnitureType": "Chair",
            "CreatedAt": "2023-05-01"
        },
        {
            "ProductID": 2,
            "Name": "Test Table",
            "Description": "A sturdy test table",
            "Price": 350.0,
            "Dimensions": "120x80x75",
            "StockQuantity": 5,
            "CategoryID": 2,
            "ImageURL": "/images/table.jpg",
            "FurnitureType": "Table",
            "CreatedAt": "2023-05-01"
        }
    ],
    "Categories": [
        {
            "CategoryID": 1,
            "Name": "Chairs",
            "Description": "Comfortable seating options",
            "CreatedAt": "2023-05-01"
        },
        {
            "CategoryID": 2,
            "Name": "Tables",
            "Description": "Sturdy tables for various uses",
            "CreatedAt": "2023-05-01"
        }
    ],
    "Cart": [
        {
            "CartID": 1,
            "UserID": 1,
            "ProductID": 1,
            "Quantity": 2,
            "AddedAt": "2023-05-01"
        }
    ],
    "Orders": [
        {
            "OrderID": 1,
            "UserID": 1,
            "TotalAmount": 400.0,
            "Status": "pending",
            "PaymentMethod": None,
            "OrderDate": "2023-05-01",
            "CreatedAt": "2023-05-01",
            "UpdatedAt": None
        }
    ],
    "OrderItems": [
        {
            "OrderItemID": 1,
            "OrderID": 1,
            "ProductID": 1,
            "Quantity": 2,
            "Price": 200.0
        }
    ],
    "AuthTokens": [
        {
            "TokenID": 1,
            "UserID": 1,
            "Token": "fake_token_123",
            "CreatedAt": "2023-05-01",
            "ExpiresAt": "2023-06-01"
        }
    ],
    "Notifications": []
}

# محاكاة لتنفيذ استعلام SQL
def mock_execute_query(query, params=None, fetch=False):
    """
    محاكاة لوظيفة execute_query لتجنب الاتصال الفعلي بقاعدة البيانات.
    """
    # إذا كان الاستعلام للاسترجاع، نقوم بمعالجته حسب نوع الجدول
    if fetch:
        # نسخة من البيانات لتجنب التعديل على البيانات الأصلية
        local_data = copy.deepcopy(mock_data)
        
        # استعلامات المستخدمين
        if "SELECT * FROM Users WHERE UserID = ?" in query and params:
            user_id = params[0]
            for user in local_data["Users"]:
                if user["UserID"] == user_id:
                    return [user]
            return []
            
        elif "SELECT * FROM Users WHERE Email = ?" in query and params:
            email = params[0]
            for user in local_data["Users"]:
                if user["Email"] == email:
                    return [user]
            return []
            
        elif "SELECT UserID, Name, Email, Role, CreatedAt FROM Users" in query:
            return local_data["Users"]
        
        # استعلامات المنتجات
        elif "SELECT * FROM Products WHERE ProductID = ?" in query and params:
            product_id = params[0]
            for product in local_data["Products"]:
                if product["ProductID"] == product_id:
                    return [product]
            return []
            
        elif "SELECT * FROM Products ORDER BY Name" in query:
            return local_data["Products"]
            
        elif "SELECT * FROM Products WHERE CategoryID = ?" in query and params:
            category_id = params[0]
            return [p for p in local_data["Products"] if p["CategoryID"] == category_id]
            
        elif "SELECT * FROM Products WHERE FurnitureType = ?" in query and params:
            furniture_type = params[0]
            return [p for p in local_data["Products"] if p["FurnitureType"] == furniture_type]
        
        # استعلامات السلة
        elif "SELECT * FROM Cart WHERE UserID = ? AND ProductID = ?" in query and params:
            user_id, product_id = params
            for cart_item in local_data["Cart"]:
                if cart_item["UserID"] == user_id and cart_item["ProductID"] == product_id:
                    return [cart_item]
            return []
            
        elif "SELECT c.*, p.Name, p.Price, p.ImageURL, p.FurnitureType, p.CategoryID" in query and params:
            user_id = params[0]
            cart_items = []
            for cart_item in local_data["Cart"]:
                if cart_item["UserID"] == user_id:
                    # دمج بيانات السلة مع بيانات المنتج
                    for product in local_data["Products"]:
                        if product["ProductID"] == cart_item["ProductID"]:
                            merged_item = {**cart_item, **{
                                "Name": product["Name"],
                                "Price": product["Price"],
                                "ImageURL": product["ImageURL"],
                                "FurnitureType": product["FurnitureType"],
                                "CategoryID": product["CategoryID"]
                            }}
                            cart_items.append(merged_item)
            return cart_items
        
        # استعلامات الطلبات
        elif "SELECT o.*, u.Name as UserName, u.Email as UserEmail" in query and params:
            order_id = params[0]
            for order in local_data["Orders"]:
                if order["OrderID"] == order_id:
                    # إضافة اسم المستخدم والبريد الإلكتروني
                    for user in local_data["Users"]:
                        if user["UserID"] == order["UserID"]:
                            order_with_user = {**order, **{
                                "UserName": user["Name"],
                                "UserEmail": user["Email"]
                            }}
                            return [order_with_user]
            return []
            
        elif "SELECT * FROM Orders WHERE UserID = ?" in query and params:
            user_id = params[0]
            return [o for o in local_data["Orders"] if o["UserID"] == user_id]
            
        elif "SELECT oi.*, p.Name as ProductName, p.ImageURL as ProductImage, p.FurnitureType" in query and params:
            order_id = params[0]
            order_items = []
            for order_item in local_data["OrderItems"]:
                if order_item["OrderID"] == order_id:
                    # دمج بيانات عنصر الطلب مع بيانات المنتج
                    for product in local_data["Products"]:
                        if product["ProductID"] == order_item["ProductID"]:
                            merged_item = {**order_item, **{
                                "ProductName": product["Name"],
                                "ProductImage": product["ImageURL"],
                                "FurnitureType": product["FurnitureType"]
                            }}
                            order_items.append(merged_item)
            return order_items
        
        # استعلامات أخرى
        elif "SELECT * FROM Categories" in query:
            return local_data["Categories"]
            
        elif "SELECT u.*" in query and "FROM AuthTokens t JOIN Users u" in query and params:
            token = params[0]
            for auth_token in local_data["AuthTokens"]:
                if auth_token["Token"] == token:
                    for user in local_data["Users"]:
                        if user["UserID"] == auth_token["UserID"]:
                            return [user]
            return []
        
        # في حالة عدم تطابق الاستعلام مع أي من الحالات السابقة
        return []
    
    # إذا كان الاستعلام للإدراج أو التحديث أو الحذف
    else:
        # ملاحظة: في الاختبارات، عادة ما نهتم فقط بالاسترجاع ولا نقوم بتعديل البيانات فعلياً
        # لكن يمكن إضافة منطق هنا للتعامل مع الإدراج والتحديث والحذف إذا كان ذلك مطلوباً
        
        # إرجاع قيمة افتراضية تشير إلى نجاح العملية
        if "INSERT INTO" in query and "OUTPUT INSERTED" in query:
            # محاكاة إرجاع معرف العنصر المدرج
            return [(1,)]
        return None

# استبدال وظائف الاتصال الأصلية بوظائف المحاكاة
def apply_mock():
    """
    تطبيق المحاكاة على وظائف قاعدة البيانات.
    """
    import app.db.execute_query
    
    # حفظ الوظيفة الأصلية للرجوع إليها لاحقاً إذا لزم الأمر
    original_execute_query = app.db.execute_query.execute_query
    
    # استبدال الوظيفة الأصلية بالمحاكاة
    app.db.execute_query.execute_query = mock_execute_query
    
    # إرجاع الوظيفة الأصلية لاستعادتها لاحقاً
    return original_execute_query

def restore_original(original_function):
    """
    استعادة وظيفة قاعدة البيانات الأصلية.
    """
    import app.db.execute_query
    app.db.execute_query.execute_query = original_function
