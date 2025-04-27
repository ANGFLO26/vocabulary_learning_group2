from abc import ABC, abstractmethod
from typing import List, Optional
from .test_entity import TestEntity

class ITestDAO(ABC):
    """Interface for Test Data Access Object"""
    
    @abstractmethod
    def get_all(self) -> List[TestEntity]:
        """Get all tests"""
        pass
        
    @abstractmethod
    def get_by_id(self, test_id: int) -> Optional[TestEntity]:
        """Get test by ID"""
        pass
        
    @abstractmethod
    def get_by_topic(self, topic_id: int) -> List[TestEntity]:
        """Get all tests for a topic"""
        pass
        
    @abstractmethod
    def create(self, topic_id: int, question: str, correct_answer: str,
               option1: str, option2: str, option3: str) -> Optional[TestEntity]:
        """Create a new test"""
        pass
        
    @abstractmethod
    def update(self, test_id: int, topic_id: int, question: str, correct_answer: str,
               option1: str, option2: str, option3: str) -> bool:
        """Update an existing test"""
        pass
        
    @abstractmethod
    def delete(self, test_id: int) -> bool:
        """Delete a test"""
        pass 