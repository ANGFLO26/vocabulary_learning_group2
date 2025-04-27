from abc import ABC, abstractmethod
from typing import List, Optional

class IVocabularyTopicDAO(ABC):
    """Interface defining data access methods for VocabularyTopic"""
    
    @abstractmethod
    def get_all(self) -> List['VocabularyTopicEntity']:
        """Get all vocabulary topics"""
        pass
        
    @abstractmethod
    def get_by_id(self, topic_id: int) -> Optional['VocabularyTopicEntity']:
        """Get vocabulary topic by ID"""
        pass
        
    @abstractmethod
    def create(self, name: str, description: str) -> int:
        """Create new vocabulary topic"""
        pass
        
    @abstractmethod
    def update(self, topic_id: int, data: dict) -> bool:
        """Update vocabulary topic"""
        pass
        
    @abstractmethod
    def delete(self, topic_id: int) -> bool:
        """Delete vocabulary topic"""
        pass 