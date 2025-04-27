from typing import List
import random
from .test_entity import TestEntity

class Test:
    """Test class with behavior and business logic"""
    
    def __init__(self, id: int, topic_id: int, question: str, 
                 correct_answer: str, option1: str, option2: str, option3: str):
        self.id = id
        self.topic_id = topic_id
        self.question = question
        self.correct_answer = correct_answer
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        
    @classmethod
    def from_entity(cls, entity: TestEntity) -> 'Test':
        """Create Test instance from TestEntity"""
        return cls(
            id=entity.id,
            topic_id=entity.topic_id,
            question=entity.question,
            correct_answer=entity.correct_answer,
            option1=entity.option1,
            option2=entity.option2,
            option3=entity.option3
        )
        
    def to_entity(self) -> TestEntity:
        """Convert to TestEntity"""
        return TestEntity(
            id=self.id,
            topic_id=self.topic_id,
            question=self.question,
            correct_answer=self.correct_answer,
            option1=self.option1,
            option2=self.option2,
            option3=self.option3
        )
        
    def get_shuffled_options(self) -> List[str]:
        """Get all options in random order"""
        options = [self.correct_answer, self.option1, self.option2, self.option3]
        random.shuffle(options)
        return options
        
    def check_answer(self, answer: str) -> bool:
        """Check if the answer is correct"""
        return answer.strip().lower() == self.correct_answer.strip().lower()
        
    def validate(self) -> bool:
        """Validate test data"""
        return bool(
            self.question and len(self.question.strip()) > 0 and
            self.correct_answer and len(self.correct_answer.strip()) > 0 and
            self.option1 and len(self.option1.strip()) > 0 and
            self.option2 and len(self.option2.strip()) > 0 and
            self.option3 and len(self.option3.strip()) > 0
        )
        
    def to_dict(self, include_answer: bool = False) -> dict:
        """Convert to dictionary (for API responses)"""
        data = {
            'id': self.id,
            'topic_id': self.topic_id,
            'question': self.question,
            'options': self.get_shuffled_options()
        }
        if include_answer:
            data['correct_answer'] = self.correct_answer
        return data 