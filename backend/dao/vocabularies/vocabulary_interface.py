from abc import ABC, abstractmethod
from typing import List, Optional

class IVocabularyDAO(ABC):
    """Interface defining data access methods for Vocabulary"""
    
    @abstractmethod
    def get_all(self) -> List['VocabularyEntity']:
        """Get all vocabularies"""
        pass
        
    @abstractmethod
    def get_by_id(self, vocabulary_id: int) -> Optional['VocabularyEntity']:
        """Get vocabulary by ID"""
        pass
        
    @abstractmethod
    def get_by_topic(self, topic_id: int) -> List['VocabularyEntity']:
        """Get all vocabularies by topic ID"""
        pass
        
    @abstractmethod
    def create(self, topic_id: int, word: str, meaning: str, example: str = None) -> int:
        """Create new vocabulary"""
        pass
        
    @abstractmethod
    def update(self, vocabulary_id: int, data: dict) -> bool:
        """Update vocabulary"""
        pass
        
    @abstractmethod
    def delete(self, vocabulary_id: int) -> bool:
        """Delete vocabulary"""
        pass 