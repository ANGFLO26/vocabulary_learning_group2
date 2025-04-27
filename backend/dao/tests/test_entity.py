from dataclasses import dataclass
from typing import Optional

@dataclass
class TestEntity:
    """Entity representing a test in the database"""
    id: Optional[int]
    topic_id: int
    question: str
    correct_answer: str
    option1: str
    option2: str
    option3: str
    
    @staticmethod
    def from_db_row(row: tuple) -> 'TestEntity':
        """Create TestEntity from database row"""
        return TestEntity(
            id=row[0],
            topic_id=row[1],
            question=row[2],
            correct_answer=row[3],
            option1=row[4],
            option2=row[5],
            option3=row[6]
        )
        
    def to_db_tuple(self) -> tuple:
        """Convert to database tuple for insertion/update"""
        return (
            self.topic_id,
            self.question,
            self.correct_answer,
            self.option1,
            self.option2,
            self.option3
        ) 