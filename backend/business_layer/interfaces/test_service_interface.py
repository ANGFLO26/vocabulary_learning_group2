from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from backend.dao.tests.test_class import Test

class ITestService(ABC):
    """Interface for Test Service"""
    
    @abstractmethod
    def get_tests_by_topic(self, topic_id: int) -> List[Test]:
        """Get all tests in a topic"""
        pass
        
    @abstractmethod
    def get_test_by_id(self, test_id: int) -> Optional[Test]:
        """Get test by ID"""
        pass
        
    @abstractmethod
    def create_test(self, topic_id: int, question: str, correct_answer: str,
                   option1: str, option2: str, option3: str) -> Optional[Test]:
        """Create a new test"""
        pass
        
    @abstractmethod
    def update_test(self, test_id: int, question: str, correct_answer: str,
                   option1: str, option2: str, option3: str) -> bool:
        """Update an existing test"""
        pass
        
    @abstractmethod
    def delete_test(self, test_id: int) -> bool:
        """Delete a test"""
        pass
        
    @abstractmethod
    def submit_test_result(self, user_id: int, topic_id: int, answers: Dict[int, str],
                          completion_time: int) -> Dict:
        """Submit test results and return score"""
        pass 