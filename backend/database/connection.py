import mysql.connector
from mysql.connector import Error
from typing import Optional

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self):
        """Create database connection"""
        try:
            if self.connection is None:
                self.connection = mysql.connector.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='12345678',
                    database='vocabulary_learning'
                )
                print("Successfully connected to the database")
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            raise
    
    def get_connection(self):
        """Get the database connection"""
        if self.connection is None:
            self.connect()
        return self.connection
    
    def close_connection(self):
        """Close the database connection"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("Database connection closed")
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[list]:
        """Execute a query and return results if any"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if query.lower().strip().startswith('select'):
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return None
                
        except Error as e:
            print(f"Error executing query: {e}")
            connection.rollback()
            raise
        finally:
            cursor.close() 