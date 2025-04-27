import mysql.connector
from mysql.connector import Error
from typing import Any
from backend.config.config import DB_CONFIG
from backend.utils.exceptions import DatabaseError

_db_connection = None

def get_db():
    """
    Get database connection singleton
    
    Returns:
        Database connection object
        
    Raises:
        DatabaseError: If connection fails
    """
    global _db_connection
    
    try:
        if _db_connection is None:
            _db_connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )
            
        if not _db_connection.is_connected():
            _db_connection.reconnect()
            
        return _db_connection
        
    except Error as e:
        raise DatabaseError(f"Database connection failed: {str(e)}")
        
def close_db() -> None:
    """Close database connection"""
    global _db_connection
    
    if _db_connection:
        _db_connection.close()
        _db_connection = None 