from typing import List, Optional
from datetime import datetime
import logging

from backend.dao.base_dao import BaseDAO
from backend.dao.vocabularies.vocabulary_entity import VocabularyEntity
from backend.utils.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class VocabularyDAO(BaseDAO):
    """Data Access Object for vocabularies table."""

    def create_vocabulary(self, topic_id: int, word: str, meaning: str, phonetic: str) -> Optional[VocabularyEntity]:
        """Creates a new vocabulary in the database."""
        try:
            query = """
                INSERT INTO vocabularies (topic_id, word, meaning, phonetic, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = (topic_id, word, meaning, phonetic, created_at)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                vocabulary_id = cursor.lastrowid
                return VocabularyEntity(vocabulary_id, topic_id, word, meaning, phonetic, created_at)
        except Exception as e:
            logger.error(f"Error creating vocabulary: {str(e)}")
            raise DatabaseError("Failed to create vocabulary")

    def get_vocabulary_by_id(self, vocabulary_id: int) -> Optional[VocabularyEntity]:
        """Retrieves a vocabulary by its ID."""
        try:
            query = "SELECT * FROM vocabularies WHERE id = %s"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (vocabulary_id,))
                row = cursor.fetchone()
                return VocabularyEntity.from_db_row(row) if row else None
        except Exception as e:
            logger.error(f"Error retrieving vocabulary {vocabulary_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve vocabulary {vocabulary_id}")

    def get_vocabularies_by_topic(self, topic_id: int) -> List[VocabularyEntity]:
        """Retrieves all vocabularies for a specific topic."""
        try:
            query = "SELECT * FROM vocabularies WHERE topic_id = %s ORDER BY created_at DESC"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (topic_id,))
                rows = cursor.fetchall()
                return [VocabularyEntity.from_db_row(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving vocabularies for topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve vocabularies for topic {topic_id}")

    def update_vocabulary(self, vocabulary_id: int, word: str, meaning: str, phonetic: str) -> bool:
        """Updates an existing vocabulary."""
        try:
            query = """
                UPDATE vocabularies
                SET word = %s, meaning = %s, phonetic = %s
                WHERE id = %s
            """
            params = (word, meaning, phonetic, vocabulary_id)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating vocabulary {vocabulary_id}: {str(e)}")
            raise DatabaseError(f"Failed to update vocabulary {vocabulary_id}")

    def delete_vocabulary(self, vocabulary_id: int) -> bool:
        """Deletes a vocabulary by its ID."""
        try:
            query = "DELETE FROM vocabularies WHERE id = %s"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (vocabulary_id,))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting vocabulary {vocabulary_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete vocabulary {vocabulary_id}")

    def search_vocabularies(self, keyword: str) -> List[VocabularyEntity]:
        """Searches vocabularies by keyword in word or meaning."""
        try:
            query = """
                SELECT * FROM vocabularies 
                WHERE word LIKE %s OR meaning LIKE %s 
                ORDER BY created_at DESC
            """
            search_pattern = f"%{keyword}%"
            params = (search_pattern, search_pattern)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [VocabularyEntity.from_db_row(row) for row in rows]
        except Exception as e:
            logger.error(f"Error searching vocabularies with keyword '{keyword}': {str(e)}")
            raise DatabaseError("Failed to search vocabularies") 