import pyodbc

# Database connection configuration
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-4809N4L;"
    "Database=FurnitureStore;"
    "Trusted_Connection=yes;"
)

def get_connection():
    """Function to get database connection"""
    return pyodbc.connect(conn_str)
