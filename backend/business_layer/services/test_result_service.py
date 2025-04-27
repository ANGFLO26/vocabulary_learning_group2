from typing import List, Optional, Dict
from backend.dao.test_results.test_result_dao import TestResultDAO
from backend.business_layer.interfaces.test_result_service_interface import ITestResultService
from backend.dao.test_results.test_result_class import TestResult

class TestResultService(ITestResultService):
    """Implementation of Test Result Service"""
    
    def __init__(self, test_result_dao: TestResultDAO):
        self.test_result_dao = test_result_dao
        
    def get_user_results(self, user_id: int) -> List[TestResult]:
        """Get all test results for a user"""
        entities = self.test_result_dao.get_by_user(user_id)
        return [TestResult.from_entity(entity) for entity in entities]
        
    def get_topic_results(self, topic_id: int) -> List[TestResult]:
        """Get all test results for a topic"""
        entities = self.test_result_dao.get_by_topic(topic_id)
        return [TestResult.from_entity(entity) for entity in entities]
        
    def get_user_topic_results(self, user_id: int, topic_id: int) -> List[TestResult]:
        """Get all test results for a user in a specific topic"""
        entities = self.test_result_dao.get_by_user_and_topic(user_id, topic_id)
        return [TestResult.from_entity(entity) for entity in entities]
        
    def save_result(self, user_id: int, topic_id: int, score: int,
                   total_questions: int, completion_time: int) -> Optional[TestResult]:
        """Save a test result"""
        # Create test result entity
        entity = self.test_result_dao.create(
            user_id=user_id,
            topic_id=topic_id,
            score=score,
            total_questions=total_questions,
            completion_time=completion_time
        )
        
        if not entity:
            return None
            
        return TestResult.from_entity(entity)
        
    def get_user_statistics(self, user_id: int) -> Dict:
        """Get user's test statistics"""
        results = self.get_user_results(user_id)
        if not results:
            return {
                'total_tests': 0,
                'average_score': 0,
                'total_correct_answers': 0,
                'total_questions': 0,
                'average_completion_time': 0
            }
            
        total_tests = len(results)
        total_correct_answers = sum(result.score for result in results)
        total_questions = sum(result.total_questions for result in results)
        total_completion_time = sum(result.completion_time for result in results)
        
        return {
            'total_tests': total_tests,
            'average_score': TestResult.calculate_average_score(results),
            'total_correct_answers': total_correct_answers,
            'total_questions': total_questions,
            'average_completion_time': TestResult.calculate_average_completion_time(results)
        }
        
    def get_topic_statistics(self, topic_id: int) -> Dict:
        """Get topic's test statistics"""
        results = self.get_topic_results(topic_id)
        if not results:
            return {
                'total_tests': 0,
                'average_score': 0,
                'total_correct_answers': 0,
                'total_questions': 0,
                'average_completion_time': 0
            }
            
        total_tests = len(results)
        total_correct_answers = sum(result.score for result in results)
        total_questions = sum(result.total_questions for result in results)
        total_completion_time = sum(result.completion_time for result in results)
        
        return {
            'total_tests': total_tests,
            'average_score': TestResult.calculate_average_score(results),
            'total_correct_answers': total_correct_answers,
            'total_questions': total_questions,
            'average_completion_time': TestResult.calculate_average_completion_time(results)
        } 