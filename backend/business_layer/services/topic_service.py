from typing import List, Optional
from backend.dao.topics.topic_dao import TopicDAO
from backend.business_layer.interfaces.topic_service_interface import ITopicService
from backend.dao.topics.topic_class import Topic

class TopicService(ITopicService):
    """Implementation of Topic Service"""
    
    def __init__(self, topic_dao: TopicDAO):
        self.topic_dao = topic_dao
        
    def get_all_topics(self) -> List[Topic]:
        """Get all topics"""
        return self.topic_dao.get_all()
        
    def get_topic_by_id(self, topic_id: int) -> Optional[Topic]:
        """Get topic by ID"""
        return self.topic_dao.get_by_id(topic_id)
        
    def create_topic(self, name: str, description: str) -> Optional[Topic]:
        """Create a new topic"""
        # Create topic
        topic = Topic(
            id=None,
            name=name,
            description=description,
            created_at=None
        )
        
        # Validate topic data
        if not topic.validate():
            return None
            
        # Save to database
        return self.topic_dao.create(topic)
        
    def update_topic(self, topic_id: int, name: str, description: str) -> bool:
        """Update an existing topic"""
        # Get topic
        topic = self.topic_dao.get_by_id(topic_id)
        if not topic:
            return False
            
        # Update topic
        topic.name = name
        topic.description = description
        
        # Validate topic data
        if not topic.validate():
            return False
            
        # Save to database
        return self.topic_dao.update(topic)
        
    def delete_topic(self, topic_id: int) -> bool:
        """Delete a topic"""
        # Get topic
        topic = self.topic_dao.get_by_id(topic_id)
        if not topic:
            return False
            
        # Delete topic
        return self.topic_dao.delete(topic_id)
        
    def get_topics_by_user(self, user_id: int) -> List[Topic]:
        """Get topics created by a user"""
        return self.topic_dao.get_by_user(user_id) 