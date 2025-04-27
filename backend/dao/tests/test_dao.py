from typing import List, Optional
from datetime import datetime
import logging

from backend.dao.base_dao import BaseDAO
from backend.dao.tests.test_entity import TestEntity
from backend.utils.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class TestDAO(BaseDAO):
    """Data Access Object for tests table."""

    def create_test(self, topic_id: int, question: str, correct_answer: str,
                   option1: str, option2: str, option3: str) -> Optional[TestEntity]:
        """Creates a new test in the database."""
        try:
            query = """
                INSERT INTO tests (topic_id, question, correct_answer, option1, option2, option3, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = (topic_id, question, correct_answer, option1, option2, option3, created_at)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                test_id = cursor.lastrowid
                return TestEntity(test_id, topic_id, question, correct_answer, 
                                option1, option2, option3, created_at)
        except Exception as e:
            logger.error(f"Error creating test: {str(e)}")
            raise DatabaseError("Failed to create test")

    def get_test_by_id(self, test_id: int) -> Optional[TestEntity]:
        """Retrieves a test by its ID."""
        try:
            query = "SELECT * FROM tests WHERE id = %s"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (test_id,))
                row = cursor.fetchone()
                return TestEntity.from_db_row(row) if row else None
        except Exception as e:
            logger.error(f"Error retrieving test {test_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve test {test_id}")

    def get_tests_by_topic(self, topic_id: int) -> List[TestEntity]:
        """Retrieves all tests for a specific topic."""
        try:
            query = "SELECT * FROM tests WHERE topic_id = %s ORDER BY created_at DESC"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (topic_id,))
                rows = cursor.fetchall()
                return [TestEntity.from_db_row(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving tests for topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve tests for topic {topic_id}")

    def update_test(self, test_id: int, question: str, correct_answer: str,
                   option1: str, option2: str, option3: str) -> bool:
        """Updates an existing test."""
        try:
            query = """
                UPDATE tests
                SET question = %s, correct_answer = %s, option1 = %s, option2 = %s, option3 = %s
                WHERE id = %s
            """
            params = (question, correct_answer, option1, option2, option3, test_id)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating test {test_id}: {str(e)}")
            raise DatabaseError(f"Failed to update test {test_id}")

    def delete_test(self, test_id: int) -> bool:
        """Deletes a test by its ID."""
        try:
            query = "DELETE FROM tests WHERE id = %s"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (test_id,))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting test {test_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete test {test_id}")

    def get_random_tests(self, topic_id: int, limit: int = 10) -> List[TestEntity]:
        """Retrieves random tests for a specific topic."""
        try:
            query = "SELECT * FROM tests WHERE topic_id = %s ORDER BY RAND() LIMIT %s"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (topic_id, limit))
                rows = cursor.fetchall()
                return [TestEntity.from_db_row(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving random tests for topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve random tests for topic {topic_id}") 