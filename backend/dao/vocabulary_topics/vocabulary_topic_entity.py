from dataclasses import dataclass

@dataclass
class VocabularyTopicEntity:
    """Entity representing a vocabulary topic record in database"""
    id: int
    name: str
    description: str
    
    @staticmethod
    def from_db_tuple(db_tuple: tuple) -> 'VocabularyTopicEntity':
        """Create entity from database tuple"""
        return VocabularyTopicEntity(
            id=db_tuple[0],
            name=db_tuple[1],
            description=db_tuple[2]
        )
        
    def to_db_tuple(self) -> tuple:
        """Convert to database tuple for insertion/update"""
        return (
            self.name,
            self.description
        ) 