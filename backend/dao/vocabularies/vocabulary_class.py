from dataclasses import dataclass
from typing import Optional
from backend.dao.vocabularies.vocabulary_entity import VocabularyEntity

@dataclass
class Vocabulary:
    """Class representing a vocabulary with validation"""
    id: Optional[int] = None
    topic_id: Optional[int] = None
    word: Optional[str] = None
    meaning: Optional[str] = None
    phonetic: Optional[str] = None
    
    def validate(self) -> None:
        """Validate vocabulary data"""
        if not self.topic_id:
            raise ValueError("Topic ID is required")
        if not self.word:
            raise ValueError("Word is required")
        if not self.meaning:
            raise ValueError("Meaning is required")
            
    def to_entity(self) -> VocabularyEntity:
        """Convert to entity"""
        self.validate()
        return VocabularyEntity(
            id=self.id or 0,
            topic_id=self.topic_id,
            word=self.word,
            meaning=self.meaning,
            phonetic=self.phonetic
        )
        
    @classmethod
    def from_entity(cls, entity: VocabularyEntity) -> 'Vocabulary':
        """Create from entity"""
        return cls(
            id=entity.id,
            topic_id=entity.topic_id,
            word=entity.word,
            meaning=entity.meaning,
            phonetic=entity.phonetic
        )
        
    def format_example(self) -> str:
        """Format example with word highlighted"""
        if not self.phonetic:
            return ""
        return self.phonetic.replace(self.word, f"**{self.word}**")
        
    def to_dict(self) -> dict:
        """Convert to dictionary (for API responses)"""
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'word': self.word,
            'meaning': self.meaning,
            'phonetic': self.phonetic,
            'formatted_example': self.format_example()
        } 