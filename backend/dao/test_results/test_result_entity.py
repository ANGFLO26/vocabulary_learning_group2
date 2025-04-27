from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class TestResultEntity:
    """Entity representing a test result in the database"""
    id: Optional[int]
    user_id: int
    topic_id: int
    score: int
    total_questions: int
    completion_time: int
    created_at: datetime
    
    @staticmethod
    def from_db_row(row: tuple) -> 'TestResultEntity':
        """Create TestResultEntity from database row"""
        return TestResultEntity(
            id=row[0],
            user_id=row[1],
            topic_id=row[2],
            score=row[3],
            total_questions=row[4],
            completion_time=row[5],
            created_at=row[6]
        )
        
    def to_db_tuple(self) -> tuple:
        """Convert to database tuple for insertion/update"""
        return (
            self.user_id,
            self.topic_id,
            self.score,
            self.total_questions,
            self.completion_time
        ) 