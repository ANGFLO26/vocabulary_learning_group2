from abc import ABC, abstractmethod
from typing import List, Optional
from .test_result_entity import TestResultEntity

class ITestResultDAO(ABC):
    """Interface for Test Result Data Access Object"""
    
    @abstractmethod
    def get_all(self) -> List[TestResultEntity]:
        """Get all test results"""
        pass
        
    @abstractmethod
    def get_by_id(self, result_id: int) -> Optional[TestResultEntity]:
        """Get test result by ID"""
        pass
        
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[TestResultEntity]:
        """Get all test results for a user"""
        pass
        
    @abstractmethod
    def get_by_topic(self, topic_id: int) -> List[TestResultEntity]:
        """Get all test results for a topic"""
        pass
        
    @abstractmethod
    def get_by_user_and_topic(self, user_id: int, topic_id: int) -> List[TestResultEntity]:
        """Get all test results for a user in a specific topic"""
        pass
        
    @abstractmethod
    def create(self, user_id: int, topic_id: int, score: int, 
               total_questions: int, completion_time: int) -> Optional[TestResultEntity]:
        """Create a new test result"""
        pass
        
    @abstractmethod
    def update(self, result_id: int, user_id: int, topic_id: int, score: int,
              total_questions: int, completion_time: int) -> bool:
        """Update an existing test result"""
        pass
        
    @abstractmethod
    def delete(self, result_id: int) -> bool:
        """Delete a test result"""
        pass 