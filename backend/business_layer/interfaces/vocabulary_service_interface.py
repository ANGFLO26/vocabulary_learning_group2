from abc import ABC, abstractmethod
from typing import List, Optional
from backend.dao.vocabularies.vocabulary_class import Vocabulary

class IVocabularyService(ABC):
    """Interface for Vocabulary Service"""
    
    @abstractmethod
    def get_vocabularies_by_topic(self, topic_id: int) -> List[Vocabulary]:
        """Get all vocabularies in a topic"""
        pass
        
    @abstractmethod
    def get_vocabulary_by_id(self, vocabulary_id: int) -> Optional[Vocabulary]:
        """Get vocabulary by ID"""
        pass
        
    @abstractmethod
    def create_vocabulary(self, topic_id: int, word: str, meaning: str, 
                         example: str) -> Optional[Vocabulary]:
        """Create a new vocabulary"""
        pass
        
    @abstractmethod
    def update_vocabulary(self, vocabulary_id: int, word: str, meaning: str,
                         example: str) -> bool:
        """Update an existing vocabulary"""
        pass
        
    @abstractmethod
    def delete_vocabulary(self, vocabulary_id: int) -> bool:
        """Delete a vocabulary"""
        pass
        
    @abstractmethod
    def search_vocabularies(self, keyword: str) -> List[Vocabulary]:
        """Search vocabularies by keyword"""
        pass 