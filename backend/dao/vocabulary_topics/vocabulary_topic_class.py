from .vocabulary_topic_entity import VocabularyTopicEntity

class VocabularyTopic:
    """VocabularyTopic class with behavior and business logic"""
    
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description
        
    @classmethod
    def from_entity(cls, entity: VocabularyTopicEntity) -> 'VocabularyTopic':
        """Create VocabularyTopic instance from VocabularyTopicEntity"""
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description
        )
        
    def to_entity(self) -> VocabularyTopicEntity:
        """Convert to VocabularyTopicEntity"""
        return VocabularyTopicEntity(
            id=self.id,
            name=self.name,
            description=self.description
        )
        
    def validate_name(self) -> bool:
        """Validate topic name"""
        return bool(self.name and len(self.name.strip()) > 0)
        
    def to_dict(self) -> dict:
        """Convert to dictionary (for API responses)"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        } 