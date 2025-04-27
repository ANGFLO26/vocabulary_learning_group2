from dataclasses import dataclass
from typing import Optional

@dataclass
class VocabularyEntity:
    """Entity representing a vocabulary record in database"""
    id: int
    topic_id: int
    word: str
    meaning: str
    phonetic: Optional[str] = None
    
    @staticmethod
    def from_db_tuple(db_tuple: tuple) -> 'VocabularyEntity':
        """Create entity from database tuple"""
        return VocabularyEntity(
            id=db_tuple[0],
            topic_id=db_tuple[1],
            word=db_tuple[2],
            meaning=db_tuple[3],
            phonetic=db_tuple[4] if len(db_tuple) > 4 else None
        )
        
    def to_db_tuple(self) -> tuple:
        """Convert to database tuple for insertion/update"""
        return (
            self.topic_id,
            self.word,
            self.meaning,
            self.phonetic
        ) 