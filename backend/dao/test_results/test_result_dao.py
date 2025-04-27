from typing import List, Optional
from datetime import datetime
import logging

from backend.dao.base_dao import BaseDAO
from backend.dao.test_results.test_result_entity import TestResultEntity
from backend.utils.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class TestResultDAO(BaseDAO):
    """Data Access Object for test_results table."""

    def create_result(self, user_id: int, topic_id: int, score: int,
                     total_questions: int, completion_time: int) -> Optional[TestResultEntity]:
        """Creates a new test result in the database."""
        try:
            query = """
                INSERT INTO test_results 
                (user_id, topic_id, score, total_questions, completion_time, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = (user_id, topic_id, score, total_questions, completion_time, created_at)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                result_id = cursor.lastrowid
                return TestResultEntity(result_id, user_id, topic_id, score,
                                     total_questions, completion_time, created_at)
        except Exception as e:
            logger.error(f"Error creating test result: {str(e)}")
            raise DatabaseError("Failed to create test result")

    def get_result_by_id(self, result_id: int) -> Optional[TestResultEntity]:
        """Retrieves a test result by its ID."""
        try:
            query = "SELECT * FROM test_results WHERE id = %s"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (result_id,))
                row = cursor.fetchone()
                return TestResultEntity.from_db_row(row) if row else None
        except Exception as e:
            logger.error(f"Error retrieving test result {result_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve test result {result_id}")

    def get_results_by_user(self, user_id: int) -> List[TestResultEntity]:
        """Retrieves all test results for a specific user."""
        try:
            query = "SELECT * FROM test_results WHERE user_id = %s ORDER BY created_at DESC"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (user_id,))
                rows = cursor.fetchall()
                return [TestResultEntity.from_db_row(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving test results for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve test results for user {user_id}")

    def get_results_by_topic(self, topic_id: int) -> List[TestResultEntity]:
        """Retrieves all test results for a specific topic."""
        try:
            query = "SELECT * FROM test_results WHERE topic_id = %s ORDER BY created_at DESC"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (topic_id,))
                rows = cursor.fetchall()
                return [TestResultEntity.from_db_row(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving test results for topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve test results for topic {topic_id}")

    def get_results_by_user_and_topic(self, user_id: int, topic_id: int) -> List[TestResultEntity]:
        """Retrieves all test results for a specific user in a specific topic."""
        try:
            query = """
                SELECT * FROM test_results 
                WHERE user_id = %s AND topic_id = %s 
                ORDER BY created_at DESC
            """
            params = (user_id, topic_id)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [TestResultEntity.from_db_row(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving test results for user {user_id} in topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve test results for user {user_id} in topic {topic_id}")

    def get_user_statistics(self, user_id: int) -> dict:
        """Retrieves statistics for a specific user."""
        try:
            query = """
                SELECT 
                    COUNT(*) as total_tests,
                    AVG(score) as average_score,
                    SUM(score) as total_correct,
                    SUM(total_questions) as total_questions,
                    AVG(completion_time) as average_time
                FROM test_results 
                WHERE user_id = %s
            """
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
                if not row:
                    return {
                        'total_tests': 0,
                        'average_score': 0,
                        'total_correct': 0,
                        'total_questions': 0,
                        'average_time': 0
                    }
                    
                return {
                    'total_tests': row[0],
                    'average_score': float(row[1]) if row[1] else 0,
                    'total_correct': int(row[2]) if row[2] else 0,
                    'total_questions': int(row[3]) if row[3] else 0,
                    'average_time': float(row[4]) if row[4] else 0
                }
        except Exception as e:
            logger.error(f"Error retrieving statistics for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve statistics for user {user_id}")

    def get_topic_statistics(self, topic_id: int) -> dict:
        """Retrieves statistics for a specific topic."""
        try:
            query = """
                SELECT 
                    COUNT(*) as total_attempts,
                    AVG(score) as average_score,
                    MAX(score) as highest_score,
                    MIN(score) as lowest_score,
                    AVG(completion_time) as average_time
                FROM test_results 
                WHERE topic_id = %s
            """
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (topic_id,))
                row = cursor.fetchone()
                if not row:
                    return {
                        'total_attempts': 0,
                        'average_score': 0,
                        'highest_score': 0,
                        'lowest_score': 0,
                        'average_time': 0
                    }
                    
                return {
                    'total_attempts': row[0],
                    'average_score': float(row[1]) if row[1] else 0,
                    'highest_score': int(row[2]) if row[2] else 0,
                    'lowest_score': int(row[3]) if row[3] else 0,
                    'average_time': float(row[4]) if row[4] else 0
                }
        except Exception as e:
            logger.error(f"Error retrieving statistics for topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve statistics for topic {topic_id}")

    def get_all(self) -> List[TestResultEntity]:
        """Get all test results"""
        query = """
            SELECT id, user_id, topic_id, score, total_questions, completion_time, created_at 
            FROM test_results
        """
        rows = self.fetch_all(query)
        return [TestResultEntity.from_db_row(row) for row in rows]
        
    def get_by_user(self, user_id: int) -> List[TestResultEntity]:
        """Get test results by user ID"""
        query = """
            SELECT id, user_id, topic_id, score, total_questions, completion_time, created_at 
            FROM test_results WHERE user_id = %s
        """
        rows = self.fetch_all(query, (user_id,))
        return [TestResultEntity.from_db_row(row) for row in rows]
        
    def get_by_topic(self, topic_id: int) -> List[TestResultEntity]:
        """Get test results by topic ID"""
        query = """
            SELECT id, user_id, topic_id, score, total_questions, completion_time, created_at 
            FROM test_results WHERE topic_id = %s
        """
        rows = self.fetch_all(query, (topic_id,))
        return [TestResultEntity.from_db_row(row) for row in rows]
        
    def get_by_user_and_topic(self, user_id: int, topic_id: int) -> List[TestResultEntity]:
        """Get test results by user ID and topic ID"""
        query = """
            SELECT id, user_id, topic_id, score, total_questions, completion_time, created_at 
            FROM test_results WHERE user_id = %s AND topic_id = %s
        """
        rows = self.fetch_all(query, (user_id, topic_id))
        return [TestResultEntity.from_db_row(row) for row in rows]
        
    def update(self, test_result: TestResultEntity) -> bool:
        """Update test result"""
        query = """
            UPDATE test_results
            SET user_id = %s, topic_id = %s, score = %s, 
                total_questions = %s, completion_time = %s
            WHERE id = %s
        """
        return self.execute(
            query,
            (test_result.user_id, test_result.topic_id, test_result.score,
             test_result.total_questions, test_result.completion_time, test_result.id)
        )
        
    def delete(self, result_id: int) -> bool:
        """Delete test result"""
        query = "DELETE FROM test_results WHERE id = %s"
        return self.execute(query, (result_id,)) 