import pyodbc
from app.db.connection import get_connection

def execute_query(query, params=None, fetch=False):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if fetch:
                    # تحويل الصفوف إلى قواميس
                    columns = [column[0] for column in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]

                connection.commit()
    except pyodbc.Error as e:
        print(f"خطأ أثناء تنفيذ الاستعلام: {e}")
        return None
