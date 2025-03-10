import unittest
from unittest.mock import patch, MagicMock
from app.models.furniture import (
    Furniture, Chair, Table, Sofa, Bed, Cabinet, FurnitureFactory
)

class TestFurnitureModel(unittest.TestCase):

    # اختبارات لفئة Chair
    @patch('app.models.furniture.execute_query')
    def test_chair_add_furniture(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن الكرسي وإضافته
        chair = Chair(
            name="Office Chair",
            description="Comfortable office chair",
            price=199.99,
            dimensions="60x60x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/office-chair.jpg",
            max_weight_capacity=120,
            has_armrests=True,
            is_adjustable=True
        )
        chair.add_furniture()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لإدراج أثاث جديد
        self.assertIn("INSERT INTO Products", call_args[0])

        # التحقق من أن معلمات الاستعلام تحتوي على بيانات الكرسي
        params = call_args[1]
        self.assertEqual(params[0], "Office Chair")  # الاسم
        self.assertEqual(params[1], "Comfortable office chair")  # الوصف
        self.assertEqual(params[2], 199.99)  # السعر
        self.assertEqual(params[3], "60x60x100")  # الأبعاد
        self.assertEqual(params[4], 10)  # الكمية
        self.assertEqual(params[5], 1)  # معرف الفئة
        self.assertEqual(params[6], "/images/office-chair.jpg")  # URL الصورة
        self.assertEqual(params[7], "Chair")  # نوع الأثاث

    def test_chair_get_furniture_type(self):
        # إنشاء كائن الكرسي
        chair = Chair("Test Chair", "Description", 100, "50x50x100", 5, 1, "/images/chair.jpg")

        # التحقق من نوع الأثاث
        self.assertEqual(chair.get_furniture_type(), "Chair")

    def test_chair_calculate_discount(self):
        # إنشاء كائن الكرسي
        chair_adjustable = Chair(
            "Test Chair", "Description", 100, "50x50x100", 5, 1, "/images/chair.jpg",
            is_adjustable=True
        )
        chair_not_adjustable = Chair(
            "Test Chair", "Description", 100, "50x50x100", 5, 1, "/images/chair.jpg",
            is_adjustable=False
        )

        # الكرسي القابل للتعديل يحصل على خصم إضافي 5%
        discount_adjustable = chair_adjustable.calculate_discount(10)
        # 10% خصم أساسي (10 دولار) + 5% خصم إضافي (5 دولار) = 15 دولار
        self.assertEqual(discount_adjustable, 15)

        # الكرسي غير القابل للتعديل يحصل فقط على الخصم الأساسي
        discount_not_adjustable = chair_not_adjustable.calculate_discount(10)
        # 10% خصم أساسي (10 دولار) = 10 دولار
        self.assertEqual(discount_not_adjustable, 10)

    def test_chair_to_dict(self):
        # إنشاء كائن الكرسي
        chair = Chair(
            "Office Chair", "Comfortable office chair", 199.99, "60x60x100", 10, 1,
            "/images/chair.jpg", 120, True, True
        )

        # استدعاء دالة to_dict
        chair_dict = chair.to_dict()

        # التحقق من النتيجة
        self.assertEqual(chair_dict["name"], "Office Chair")
        self.assertEqual(chair_dict["description"], "Comfortable office chair")
        self.assertEqual(chair_dict["price"], 199.99)
        self.assertEqual(chair_dict["furniture_type"], "Chair")
        self.assertEqual(chair_dict["max_weight_capacity"], 120)
        self.assertEqual(chair_dict["has_armrests"], True)
        self.assertEqual(chair_dict["is_adjustable"], True)

    # اختبارات لفئة Table
    @patch('app.models.furniture.execute_query')
    def test_table_add_furniture(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن الطاولة وإضافته
        table = Table(
            name="Dining Table",
            description="Beautiful dining table",
            price=399.99,
            dimensions="120x80x75",
            stock_quantity=5,
            category_id=2,
            image_url="/images/dining-table.jpg",
            shape="Rectangle",
            max_weight_capacity=150,
            is_extendable=True
        )
        table.add_furniture()

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لإدراج أثاث جديد
        self.assertIn("INSERT INTO Products", call_args[0])

        # التحقق من أن معلمات الاستعلام تحتوي على بيانات الطاولة
        params = call_args[1]
        self.assertEqual(params[0], "Dining Table")  # الاسم
        self.assertEqual(params[7], "Table")  # نوع الأثاث

    def test_table_get_furniture_type(self):
        # إنشاء كائن الطاولة
        table = Table("Test Table", "Description", 300, "120x80x75", 5, 2, "/images/table.jpg")

        # التحقق من نوع الأثاث
        self.assertEqual(table.get_furniture_type(), "Table")

    def test_table_calculate_discount(self):
        # إنشاء كائن الطاولة
        table_extendable = Table(
            "Test Table", "Description", 300, "120x80x75", 5, 2, "/images/table.jpg",
            is_extendable=True
        )
        table_not_extendable = Table(
            "Test Table", "Description", 300, "120x80x75", 5, 2, "/images/table.jpg",
            is_extendable=False
        )

        # الطاولة القابلة للتمديد تحصل على خصم إضافي 3%
        discount_extendable = table_extendable.calculate_discount(10)
        # 10% خصم أساسي (30 دولار) + 3% خصم إضافي (9 دولار) = 39 دولار
        self.assertEqual(discount_extendable, 39)

        # الطاولة غير القابلة للتمديد تحصل فقط على الخصم الأساسي
        discount_not_extendable = table_not_extendable.calculate_discount(10)
        # 10% خصم أساسي (30 دولار) = 30 دولار
        self.assertEqual(discount_not_extendable, 30)

    # اختبارات لفئة Sofa
    def test_sofa_get_furniture_type(self):
        # إنشاء كائن الأريكة
        sofa = Sofa("Test Sofa", "Description", 500, "200x90x85", 3, 3, "/images/sofa.jpg")

        # التحقق من نوع الأثاث
        self.assertEqual(sofa.get_furniture_type(), "Sofa")

    def test_sofa_calculate_discount(self):
        # إنشاء كائن الأريكة
        sofa_convertible = Sofa(
            "Test Sofa", "Description", 500, "200x90x85", 3, 3, "/images/sofa.jpg",
            is_convertible=True
        )
        sofa_not_convertible = Sofa(
            "Test Sofa", "Description", 500, "200x90x85", 3, 3, "/images/sofa.jpg",
            is_convertible=False
        )

        # الأريكة القابلة للتحويل تحصل على خصم إضافي 7%
        discount_convertible = sofa_convertible.calculate_discount(10)
        # 10% خصم أساسي (50 دولار) + 7% خصم إضافي (35 دولار) = 85 دولار
        self.assertEqual(discount_convertible, 85)

        # الأريكة غير القابلة للتحويل تحصل فقط على الخصم الأساسي
        discount_not_convertible = sofa_not_convertible.calculate_discount(10)
        # 10% خصم أساسي (50 دولار) = 50 دولار
        self.assertEqual(discount_not_convertible, 50)

    # اختبارات لفئة Bed
    def test_bed_get_furniture_type(self):
        # إنشاء كائن السرير
        bed = Bed("Test Bed", "Description", 600, "200x180x60", 2, 4, "/images/bed.jpg")

        # التحقق من نوع الأثاث
        self.assertEqual(bed.get_furniture_type(), "Bed")

    def test_bed_calculate_discount(self):
        # إنشاء كائن السرير
        bed_with_storage = Bed(
            "Test Bed", "Description", 600, "200x180x60", 2, 4, "/images/bed.jpg",
            has_storage=True
        )
        bed_without_storage = Bed(
            "Test Bed", "Description", 600, "200x180x60", 2, 4, "/images/bed.jpg",
            has_storage=False
        )

        # السرير مع تخزين يحصل على خصم إضافي 4%
        discount_with_storage = bed_with_storage.calculate_discount(10)
        # 10% خصم أساسي (60 دولار) + 4% خصم إضافي (24 دولار) = 84 دولار
        self.assertEqual(discount_with_storage, 84)

        # السرير بدون تخزين يحصل فقط على الخصم الأساسي
        discount_without_storage = bed_without_storage.calculate_discount(10)
        # 10% خصم أساسي (60 دولار) = 60 دولار
        self.assertEqual(discount_without_storage, 60)

    # اختبارات لفئة Cabinet
    def test_cabinet_get_furniture_type(self):
        # إنشاء كائن الخزانة
        cabinet = Cabinet("Test Cabinet", "Description", 400, "120x50x180", 4, 5, "/images/cabinet.jpg")

        # التحقق من نوع الأثاث
        self.assertEqual(cabinet.get_furniture_type(), "Cabinet")

    def test_cabinet_calculate_discount(self):
        # إنشاء كائن الخزانة
        cabinet_with_lock = Cabinet(
            "Test Cabinet", "Description", 400, "120x50x180", 4, 5, "/images/cabinet.jpg",
            has_lock=True
        )
        cabinet_without_lock = Cabinet(
            "Test Cabinet", "Description", 400, "120x50x180", 4, 5, "/images/cabinet.jpg",
            has_lock=False
        )

        # الخزانة مع قفل تحصل على خصم إضافي 2%
        discount_with_lock = cabinet_with_lock.calculate_discount(10)
        # 10% خصم أساسي (40 دولار) + 2% خصم إضافي (8 دولار) = 48 دولار
        self.assertEqual(discount_with_lock, 48)

        # الخزانة بدون قفل تحصل فقط على الخصم الأساسي
        discount_without_lock = cabinet_without_lock.calculate_discount(10)
        # 10% خصم أساسي (40 دولار) = 40 دولار
        self.assertEqual(discount_without_lock, 40)

    # اختبارات لاستاتيك ميثودس في Furniture
    @patch('app.models.furniture.execute_query')
    def test_get_furniture_by_id(self, mock_execute_query):
        # محاكاة نتيجة الاستعلام
        mock_execute_query.return_value = [{
            "ProductID": 1,
            "Name": "Office Chair",
            "Description": "Comfortable office chair",
            "Price": 199.99,
            "Dimensions": "60x60x100",
            "StockQuantity": 10,
            "CategoryID": 1,
            "ImageURL": "/images/office-chair.jpg",
            "FurnitureType": "Chair",
            "CreatedAt": "2023-04-01"
        }]

        # محاكاة FurnitureFactory
        with patch('app.models.furniture.FurnitureFactory.create_furniture') as mock_create_furniture:
            # إنشاء كائن الكرسي
            mock_chair = Chair(
                "Office Chair", "Comfortable office chair", 199.99, "60x60x100", 10, 1,
                "/images/office-chair.jpg"
            )
            mock_create_furniture.return_value = mock_chair

            # استدعاء دالة الحصول على الأثاث بواسطة المعرف
            furniture = Furniture.get_furniture_by_id(1)

            # التحقق من استدعاء execute_query بالمعلمات الصحيحة
            mock_execute_query.assert_called_once()
            call_args = mock_execute_query.call_args[0]

            # التحقق من أن الاستعلام SQL هو للبحث عن أثاث
            self.assertIn("SELECT * FROM Products WHERE ProductID = ?", call_args[0])
            self.assertEqual(call_args[1], (1,))

            # التحقق من استدعاء FurnitureFactory.create_furniture
            mock_create_furniture.assert_called_once()

            # التحقق من النتيجة
            self.assertEqual(furniture, mock_chair)

    @patch('app.models.furniture.execute_query')
    def test_update_stock(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # استدعاء دالة تحديث المخزون
        Furniture.update_stock(1, 5)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لتحديث المخزون
        self.assertIn("UPDATE Products", call_args[0])
        self.assertEqual(call_args[1], (5, 1))

    # اختبارات لنمط المصنع FurnitureFactory
    def test_furniture_factory_create_chair(self):
        # إنشاء كرسي باستخدام المصنع
        chair = FurnitureFactory.create_furniture(
            furniture_type="Chair",
            name="Factory Chair",
            description="Created by factory",
            price=199.99,
            dimensions="60x60x100",
            stock_quantity=10,
            category_id=1,
            image_url="/images/chair.jpg",
            additional_data={
                "max_weight_capacity": 120,
                "has_armrests": True,
                "is_adjustable": True
            }
        )

        # التحقق من نوع الكائن ونوع الأثاث
        self.assertIsInstance(chair, Chair)
        self.assertEqual(chair.get_furniture_type(), "Chair")
        self.assertEqual(chair.name, "Factory Chair")
        self.assertEqual(chair.max_weight_capacity, 120)
        self.assertEqual(chair.has_armrests, True)
        self.assertEqual(chair.is_adjustable, True)

    def test_furniture_factory_create_table(self):
        # إنشاء طاولة باستخدام المصنع
        table = FurnitureFactory.create_furniture(
            furniture_type="Table",
            name="Factory Table",
            description="Created by factory",
            price=399.99,
            dimensions="120x80x75",
            stock_quantity=5,
            category_id=2,
            image_url="/images/table.jpg",
            additional_data={
                "shape": "Round",
                "max_weight_capacity": 150,
                "is_extendable": True
            }
        )

        # التحقق من نوع الكائن ونوع الأثاث
        self.assertIsInstance(table, Table)
        self.assertEqual(table.get_furniture_type(), "Table")
        self.assertEqual(table.name, "Factory Table")
        self.assertEqual(table.shape, "Round")
        self.assertEqual(table.max_weight_capacity, 150)
        self.assertEqual(table.is_extendable, True)

    def test_furniture_factory_create_sofa(self):
        # إنشاء أريكة باستخدام المصنع
        sofa = FurnitureFactory.create_furniture(
            furniture_type="Sofa",
            name="Factory Sofa",
            description="Created by factory",
            price=599.99,
            dimensions="220x90x85",
            stock_quantity=3,
            category_id=3,
            image_url="/images/sofa.jpg",
            additional_data={
                "seats": 4,
                "is_convertible": True,
                "has_storage": True
            }
        )

        # التحقق من نوع الكائن ونوع الأثاث
        self.assertIsInstance(sofa, Sofa)
        self.assertEqual(sofa.get_furniture_type(), "Sofa")
        self.assertEqual(sofa.name, "Factory Sofa")
        self.assertEqual(sofa.seats, 4)
        self.assertEqual(sofa.is_convertible, True)
        self.assertEqual(sofa.has_storage, True)

    def test_furniture_factory_create_bed(self):
        # إنشاء سرير باستخدام المصنع
        bed = FurnitureFactory.create_furniture(
            furniture_type="Bed",
            name="Factory Bed",
            description="Created by factory",
            price=699.99,
            dimensions="200x180x60",
            stock_quantity=2,
            category_id=4,
            image_url="/images/bed.jpg",
            additional_data={
                "size": "King",
                "has_storage": True,
                "material_type": "Oak"
            }
        )

        # التحقق من نوع الكائن ونوع الأثاث
        self.assertIsInstance(bed, Bed)
        self.assertEqual(bed.get_furniture_type(), "Bed")
        self.assertEqual(bed.name, "Factory Bed")
        self.assertEqual(bed.size, "King")
        self.assertEqual(bed.has_storage, True)
        self.assertEqual(bed.material_type, "Oak")

    def test_furniture_factory_create_cabinet(self):
        # إنشاء خزانة باستخدام المصنع
        cabinet = FurnitureFactory.create_furniture(
            furniture_type="Cabinet",
            name="Factory Cabinet",
            description="Created by factory",
            price=499.99,
            dimensions="120x50x180",
            stock_quantity=4,
            category_id=5,
            image_url="/images/cabinet.jpg",
            additional_data={
                "num_drawers": 3,
                "num_shelves": 4,
                "has_lock": True
            }
        )

        # التحقق من نوع الكائن ونوع الأثاث
        self.assertIsInstance(cabinet, Cabinet)
        self.assertEqual(cabinet.get_furniture_type(), "Cabinet")
        self.assertEqual(cabinet.name, "Factory Cabinet")
        self.assertEqual(cabinet.num_drawers, 3)
        self.assertEqual(cabinet.num_shelves, 4)
        self.assertEqual(cabinet.has_lock, True)

    def test_furniture_factory_unknown_type(self):
        # محاولة إنشاء نوع أثاث غير معروف
        with self.assertRaises(ValueError) as context:
            FurnitureFactory.create_furniture(
                furniture_type="Unknown",
                name="Unknown Furniture",
                description="Unknown type",
                price=100,
                dimensions="50x50x50",
                stock_quantity=1,
                category_id=1,
                image_url="/images/unknown.jpg"
            )

        self.assertIn("Unknown furniture type", str(context.exception))

    @patch('app.models.furniture.execute_query')
    def test_update_furniture(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # إنشاء كائن الكرسي وتحديثه
        chair = Chair(
            name="Updated Chair",
            description="Updated description",
            price=249.99,
            dimensions="65x65x105",
            stock_quantity=8,
            category_id=1,
            image_url="/images/updated-chair.jpg",
            max_weight_capacity=130,
            has_armrests=True,
            is_adjustable=True
        )
        chair.update_furniture(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لتحديث الأثاث
        self.assertIn("UPDATE Products", call_args[0])

        # التحقق من أن معلمات الاستعلام تحتوي على بيانات الكرسي المحدثة
        params = call_args[1]
        self.assertEqual(params[0], "Updated Chair")  # الاسم
        self.assertEqual(params[1], "Updated description")  # الوصف
        self.assertEqual(params[2], 249.99)  # السعر
        self.assertEqual(params[3], "65x65x105")  # الأبعاد
        self.assertEqual(params[4], 8)  # الكمية
        self.assertEqual(params[7], "Chair")  # نوع الأثاث
        self.assertEqual(params[8], 1)  # معرف المنتج

    @patch('app.models.furniture.execute_query')
    def test_delete_furniture(self, mock_execute_query):
        # محاكاة تنفيذ الاستعلام
        mock_execute_query.return_value = None

        # حذف الأثاث
        Furniture.delete_furniture(1)

        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]

        # التحقق من أن الاستعلام SQL هو لحذف الأثاث
        self.assertIn("DELETE FROM Products WHERE ProductID = ?", call_args[0])
        self.assertEqual(call_args[1], (1,))

if __name__ == '__main__':
    unittest.main()
