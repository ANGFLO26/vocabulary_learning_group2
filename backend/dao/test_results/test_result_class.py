from typing import Dict, List, Optional
from datetime import datetime
from .test_result_entity import TestResultEntity
from dataclasses import dataclass

@dataclass
class TestResult:
    """Class representing a test result"""
    
    id: Optional[int]
    user_id: int
    topic_id: int
    score: int
    completion_time: int
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
            
    def validate(self) -> bool:
        """
        Validate test result data
        
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(self.user_id, int) or self.user_id <= 0:
            return False
            
        if not isinstance(self.topic_id, int) or self.topic_id <= 0:
            return False
            
        if not isinstance(self.score, int) or self.score < 0 or self.score > 100:
            return False
            
        if not isinstance(self.completion_time, int) or self.completion_time <= 0:
            return False
            
        return True
        
    def to_dict(self) -> Dict:
        """
        Convert to dictionary for API responses
        
        Returns:
            Dictionary representation of test result
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "topic_id": self.topic_id,
            "score": self.score,
            "completion_time": self.completion_time,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
    @classmethod
    def from_entity(cls, entity: TestResultEntity) -> 'TestResult':
        """Create TestResult instance from TestResultEntity"""
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            topic_id=entity.topic_id,
            score=entity.score,
            completion_time=entity.completion_time,
            created_at=entity.created_at
        )
        
    def to_entity(self) -> TestResultEntity:
        """Convert to TestResultEntity"""
        return TestResultEntity(
            id=self.id,
            user_id=self.user_id,
            topic_id=self.topic_id,
            score=self.score,
            completion_time=self.completion_time,
            created_at=self.created_at
        )
        
    def calculate_percentage(self) -> float:
        """Calculate the percentage score"""
        if self.total_questions == 0:
            return 0.0
        return (self.score / self.total_questions) * 100
        
    def get_grade(self) -> str:
        """Get letter grade based on percentage"""
        percentage = self.calculate_percentage()
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"
            
    def get_completion_time_minutes(self) -> float:
        """Get completion time in minutes"""
        return self.completion_time / 60.0
        
    @staticmethod
    def calculate_average_score(results: List['TestResult']) -> float:
        """Calculate average score from a list of test results"""
        if not results:
            return 0.0
        total_score = sum(result.score for result in results)
        total_questions = sum(result.total_questions for result in results)
        if total_questions == 0:
            return 0.0
        return (total_score / total_questions) * 100
        
    @staticmethod
    def calculate_average_completion_time(results: List['TestResult']) -> float:
        """Calculate average completion time from a list of test results"""
        if not results:
            return 0.0
        total_time = sum(result.completion_time for result in results)
        return total_time / len(results) 