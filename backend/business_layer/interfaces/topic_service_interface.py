from abc import ABC, abstractmethod
from typing import List, Optional
from backend.dao.topics.topic_class import Topic

class ITopicService(ABC):
    """Interface for Topic Service"""
    
    @abstractmethod
    def get_all_topics(self) -> List[Topic]:
        """Get all topics"""
        pass
        
    @abstractmethod
    def get_topic_by_id(self, topic_id: int) -> Optional[Topic]:
        """Get topic by ID"""
        pass
        
    @abstractmethod
    def create_topic(self, name: str, description: str) -> Optional[Topic]:
        """Create a new topic"""
        pass
        
    @abstractmethod
    def update_topic(self, topic_id: int, name: str, description: str) -> bool:
        """Update an existing topic"""
        pass
        
    @abstractmethod
    def delete_topic(self, topic_id: int) -> bool:
        """Delete a topic"""
        pass
        
    @abstractmethod
    def get_topics_by_user(self, user_id: int) -> List[Topic]:
        """Get topics created by a user"""
        pass 