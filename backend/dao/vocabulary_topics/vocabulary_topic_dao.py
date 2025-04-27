from typing import List, Optional
from backend.dao.base_dao import BaseDAO
from backend.dao.vocabulary_topics.vocabulary_topic_entity import VocabularyTopicEntity

class VocabularyTopicDAO(BaseDAO):
    """Data Access Object for vocabulary topic operations"""
    
    def get_all(self) -> List[VocabularyTopicEntity]:
        """Get all vocabulary topics"""
        query = "SELECT id, name, description FROM vocabulary_topics"
        rows = self.fetch_all(query)
        return [VocabularyTopicEntity.from_db_tuple(row) for row in rows]
        
    def get_by_id(self, topic_id: int) -> Optional[VocabularyTopicEntity]:
        """Get vocabulary topic by ID"""
        query = "SELECT id, name, description FROM vocabulary_topics WHERE id = %s"
        row = self.fetch_one(query, (topic_id,))
        return VocabularyTopicEntity.from_db_tuple(row) if row else None
        
    def create(self, name: str, description: str) -> int:
        """Create new vocabulary topic"""
        query = "INSERT INTO vocabulary_topics (name, description) VALUES (%s, %s)"
        return self.insert(query, (name, description))
        
    def update(self, topic_id: int, name: str, description: str) -> bool:
        """Update vocabulary topic"""
        query = """
            UPDATE vocabulary_topics
            SET name = %s, description = %s
            WHERE id = %s
        """
        return self.execute(query, (name, description, topic_id))
        
    def delete(self, topic_id: int) -> bool:
        """Delete vocabulary topic"""
        query = "DELETE FROM vocabulary_topics WHERE id = %s"
        return self.execute(query, (topic_id,)) 