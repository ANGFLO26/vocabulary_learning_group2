from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from backend.dao.test_results.test_result_class import TestResult

class ITestResultService(ABC):
    """Interface for Test Result Service"""
    
    @abstractmethod
    def get_user_results(self, user_id: int) -> List[TestResult]:
        """Get all test results for a user"""
        pass
        
    @abstractmethod
    def get_topic_results(self, topic_id: int) -> List[TestResult]:
        """Get all test results for a topic"""
        pass
        
    @abstractmethod
    def get_user_topic_results(self, user_id: int, topic_id: int) -> List[TestResult]:
        """Get all test results for a user in a specific topic"""
        pass
        
    @abstractmethod
    def save_result(self, user_id: int, topic_id: int, score: int,
                   total_questions: int, completion_time: int) -> Optional[TestResult]:
        """Save a test result"""
        pass
        
    @abstractmethod
    def get_user_statistics(self, user_id: int) -> Dict:
        """Get user's test statistics"""
        pass
        
    @abstractmethod
    def get_topic_statistics(self, topic_id: int) -> Dict:
        """Get topic's test statistics"""
        pass 