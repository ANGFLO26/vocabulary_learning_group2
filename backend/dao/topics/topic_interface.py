from abc import ABC, abstractmethod
from typing import List, Optional
from backend.dao.topics.topic_class import Topic

class ITopicDAO(ABC):
    """Interface for Topic Data Access Object"""
    
    @abstractmethod
    def get_all(self) -> List[Topic]:
        """Get all topics"""
        pass
        
    @abstractmethod
    def get_by_id(self, topic_id: int) -> Optional[Topic]:
        """Get topic by ID"""
        pass
        
    @abstractmethod
    def create(self, topic: Topic) -> Optional[Topic]:
        """Create new topic"""
        pass
        
    @abstractmethod
    def update(self, topic: Topic) -> bool:
        """Update topic"""
        pass
        
    @abstractmethod
    def delete(self, topic_id: int) -> bool:
        """Delete topic"""
        pass
        
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Topic]:
        """Get topics by user ID"""
        pass 