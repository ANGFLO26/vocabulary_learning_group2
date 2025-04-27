from typing import List, Optional, Any
from backend.database.connection import DatabaseConnection
from mysql.connector import Error

class BaseDAO:
    """Base Data Access Object with common database operations"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        
    def execute_query(self, query: str, params: tuple = None, fetch_one: bool = False, return_id: bool = False) -> Any:
        """
        Execute a database query with error handling
        
        Args:
            query: SQL query string
            params: Query parameters
            fetch_one: Whether to fetch only one row
            return_id: Whether to return the last inserted ID
            
        Returns:
            Query results or last inserted ID
        """
        try:
            cursor = self.db.get_connection().cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if query.lower().strip().startswith('select'):
                if fetch_one:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
            else:
                self.db.get_connection().commit()
                if return_id:
                    result = cursor.lastrowid
                else:
                    result = cursor.rowcount > 0
                    
            return result
            
        except Error as e:
            print(f"Error executing query: {e}")
            self.db.get_connection().rollback()
            raise
        finally:
            cursor.close()
            
    def fetch_all(self, query: str, params: tuple = None) -> List[tuple]:
        """Execute a SELECT query and return all results"""
        return self.execute_query(query, params)
        
    def fetch_one(self, query: str, params: tuple = None) -> Optional[tuple]:
        """Execute a SELECT query and return one result"""
        return self.execute_query(query, params, fetch_one=True)
        
    def execute(self, query: str, params: tuple = None) -> bool:
        """Execute an INSERT/UPDATE/DELETE query"""
        return self.execute_query(query, params)
        
    def insert(self, query: str, params: tuple = None) -> int:
        """Execute an INSERT query and return the last inserted ID"""
        return self.execute_query(query, params, return_id=True) 