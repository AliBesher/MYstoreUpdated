import pyodbc
from app.db.connection import get_connection

def execute_query(query, params=None, fetch=False):
    """
    Function to execute SQL queries on the database.
    - query: Query text.
    - params: Parameters to pass to the query (if any).
    - fetch: Set to True if the operation needs to fetch data.
    """
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if fetch:
                    return cursor.fetchall()

                connection.commit()
    except pyodbc.Error as e:
        print(f"Error executing query: {e}")
        return None
