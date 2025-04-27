from typing import List, Optional
from datetime import datetime
from backend.dao.base_dao import BaseDAO
from backend.dao.topics.topic_interface import ITopicDAO
from backend.dao.topics.topic_class import Topic
from backend.utils.exceptions import DatabaseError
import logging

logger = logging.getLogger(__name__)

class TopicDAO(BaseDAO, ITopicDAO):
    """Implementation of Topic Data Access Object"""
    
    def __init__(self):
        super().__init__()
        self.table = 'vocabulary_topics'
        
    def get_all(self) -> List[Topic]:
        """Get all topics"""
        try:
            query = f"SELECT id, name, description, created_at FROM {self.table}"
            rows = self.fetch_all(query)
            return [Topic(
                id=row[0],
                name=row[1],
                description=row[2],
                created_at=row[3]
            ) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get topics: {str(e)}")
            raise DatabaseError(f"Failed to get topics: {str(e)}")
            
    def get_by_id(self, topic_id: int) -> Optional[Topic]:
        """Get topic by ID"""
        try:
            query = f"SELECT id, name, description, created_at FROM {self.table} WHERE id = %s"
            row = self.fetch_one(query, (topic_id,))
            if not row:
                return None
            return Topic(
                id=row[0],
                name=row[1],
                description=row[2],
                created_at=row[3]
            )
        except Exception as e:
            logger.error(f"Failed to get topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to get topic {topic_id}: {str(e)}")
            
    def create(self, topic: Topic) -> Optional[Topic]:
        """Create new topic"""
        try:
            query = f"INSERT INTO {self.table} (name, description, created_at) VALUES (%s, %s, %s)"
            params = (topic.name, topic.description, datetime.now())
            topic.id = self.insert(query, params)
            return topic
        except Exception as e:
            logger.error(f"Failed to create topic: {str(e)}")
            raise DatabaseError(f"Failed to create topic: {str(e)}")
            
    def update(self, topic: Topic) -> bool:
        """Update topic"""
        try:
            query = f"UPDATE {self.table} SET name = %s, description = %s WHERE id = %s"
            params = (topic.name, topic.description, topic.id)
            return self.execute(query, params)
        except Exception as e:
            logger.error(f"Failed to update topic {topic.id}: {str(e)}")
            raise DatabaseError(f"Failed to update topic {topic.id}: {str(e)}")
            
    def delete(self, topic_id: int) -> bool:
        """Delete topic"""
        try:
            query = f"DELETE FROM {self.table} WHERE id = %s"
            params = (topic_id,)
            return self.execute(query, params)
        except Exception as e:
            logger.error(f"Failed to delete topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete topic {topic_id}: {str(e)}")
            
    def get_by_user(self, user_id: int) -> List[Topic]:
        """Get topics by user ID (not supported, return empty)"""
        return [] 