from typing import List, Optional
from backend.dao.vocabularies.vocabulary_dao import VocabularyDAO
from backend.business_layer.interfaces.vocabulary_service_interface import IVocabularyService
from backend.dao.vocabularies.vocabulary_class import Vocabulary

class VocabularyService(IVocabularyService):
    """Implementation of Vocabulary Service"""
    
    def __init__(self, vocabulary_dao: VocabularyDAO):
        self.vocabulary_dao = vocabulary_dao
        
    def get_vocabularies_by_topic(self, topic_id: int) -> List[Vocabulary]:
        """Get all vocabularies in a topic"""
        return self.vocabulary_dao.get_by_topic(topic_id)
        
    def get_vocabulary_by_id(self, vocabulary_id: int) -> Optional[Vocabulary]:
        """Get vocabulary by ID"""
        return self.vocabulary_dao.get_by_id(vocabulary_id)
        
    def create_vocabulary(self, topic_id: int, word: str, meaning: str,
                         example: str) -> Optional[Vocabulary]:
        """Create a new vocabulary"""
        # Create vocabulary
        vocabulary = Vocabulary(
            id=None,
            topic_id=topic_id,
            word=word,
            meaning=meaning,
            example=example
        )
        
        # Validate vocabulary data
        if not vocabulary.validate():
            return None
            
        # Save to database
        return self.vocabulary_dao.create(vocabulary)
        
    def update_vocabulary(self, vocabulary_id: int, word: str, meaning: str,
                         example: str) -> bool:
        """Update an existing vocabulary"""
        # Get vocabulary
        vocabulary = self.vocabulary_dao.get_by_id(vocabulary_id)
        if not vocabulary:
            return False
            
        # Update vocabulary
        vocabulary.word = word
        vocabulary.meaning = meaning
        vocabulary.example = example
        
        # Validate vocabulary data
        if not vocabulary.validate():
            return False
            
        # Save to database
        return self.vocabulary_dao.update(vocabulary)
        
    def delete_vocabulary(self, vocabulary_id: int) -> bool:
        """Delete a vocabulary"""
        # Get vocabulary
        vocabulary = self.vocabulary_dao.get_by_id(vocabulary_id)
        if not vocabulary:
            return False
            
        # Delete vocabulary
        return self.vocabulary_dao.delete(vocabulary_id)
        
    def search_vocabularies(self, keyword: str) -> List[Vocabulary]:
        """Search vocabularies by keyword"""
        return self.vocabulary_dao.search(keyword) 