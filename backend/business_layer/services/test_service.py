from typing import List, Optional, Dict
from backend.dao.tests.test_dao import TestDAO
from backend.business_layer.interfaces.test_service_interface import ITestService
from backend.business_layer.interfaces.test_result_service_interface import ITestResultService
from backend.business_layer.interfaces.leaderboard_service_interface import ILeaderboardService
from backend.dao.tests.test_class import Test

class TestService(ITestService):
    """Implementation of Test Service"""
    
    def __init__(self, test_dao: TestDAO, test_result_service: ITestResultService,
                 leaderboard_service: ILeaderboardService):
        self.test_dao = test_dao
        self.test_result_service = test_result_service
        self.leaderboard_service = leaderboard_service
        
    def get_tests_by_topic(self, topic_id: int) -> List[Test]:
        """Get all tests in a topic"""
        return self.test_dao.get_by_topic(topic_id)
        
    def get_test_by_id(self, test_id: int) -> Optional[Test]:
        """Get test by ID"""
        return self.test_dao.get_by_id(test_id)
        
    def create_test(self, topic_id: int, question: str, correct_answer: str,
                   option1: str, option2: str, option3: str) -> Optional[Test]:
        """Create a new test"""
        # Create test
        test = Test(
            id=None,
            topic_id=topic_id,
            question=question,
            correct_answer=correct_answer,
            option1=option1,
            option2=option2,
            option3=option3
        )
        
        # Validate test data
        if not test.validate():
            return None
            
        # Save to database
        return self.test_dao.create(test)
        
    def update_test(self, test_id: int, question: str, correct_answer: str,
                   option1: str, option2: str, option3: str) -> bool:
        """Update an existing test"""
        # Get test
        test = self.test_dao.get_by_id(test_id)
        if not test:
            return False
            
        # Update test
        test.question = question
        test.correct_answer = correct_answer
        test.option1 = option1
        test.option2 = option2
        test.option3 = option3
        
        # Validate test data
        if not test.validate():
            return False
            
        # Save to database
        return self.test_dao.update(test)
        
    def delete_test(self, test_id: int) -> bool:
        """Delete a test"""
        # Get test
        test = self.test_dao.get_by_id(test_id)
        if not test:
            return False
            
        # Delete test
        return self.test_dao.delete(test_id)
        
    def submit_test_result(self, user_id: int, topic_id: int, answers: Dict[int, str],
                          completion_time: int) -> Dict:
        """Submit test results and return score"""
        # Get all tests for topic
        tests = self.get_tests_by_topic(topic_id)
        if not tests:
            return {'error': 'No tests found for this topic'}
            
        # Calculate score
        total_questions = len(tests)
        correct_answers = 0
        
        for test in tests:
            if test.id in answers and test.check_answer(answers[test.id]):
                correct_answers += 1
                
        # Calculate percentage
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Save test result
        result = self.test_result_service.save_result(
            user_id=user_id,
            topic_id=topic_id,
            score=correct_answers,
            total_questions=total_questions,
            completion_time=completion_time
        )
        
        if not result:
            return {'error': 'Failed to save test result'}
            
        # Update leaderboard
        self.leaderboard_service.update_user_score(user_id, topic_id, score)
        
        return {
            'score': score,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'completion_time': completion_time
        } 