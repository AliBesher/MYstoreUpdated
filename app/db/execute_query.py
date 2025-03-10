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
                    # Convert rows to dictionaries
                    columns = [column[0] for column in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]

                connection.commit()
    except pyodbc.Error as e:
        print(f"Error while executing query: {e}")
        return None

