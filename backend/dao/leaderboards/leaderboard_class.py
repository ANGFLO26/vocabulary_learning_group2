from typing import Dict, List
from .leaderboard_entity import LeaderboardEntity

class Leaderboard:
    """Leaderboard class with behavior and business logic"""
    
    def __init__(self, user_id: int, topic_id: int, score: int, rank: int = None):
        self.user_id = user_id
        self.topic_id = topic_id
        self.score = score
        self.rank = rank
        
    @classmethod
    def from_entity(cls, entity: LeaderboardEntity) -> 'Leaderboard':
        """Create Leaderboard instance from LeaderboardEntity"""
        return cls(
            user_id=entity.user_id,
            topic_id=entity.topic_id,
            score=entity.score,
            rank=entity.rank
        )
        
    def to_entity(self) -> LeaderboardEntity:
        """Convert to LeaderboardEntity"""
        return LeaderboardEntity(
            user_id=self.user_id,
            topic_id=self.topic_id,
            score=self.score,
            rank=self.rank
        )
        
    def validate(self) -> bool:
        """Validate leaderboard data"""
        return bool(
            self.user_id > 0 and
            self.topic_id > 0 and
            self.score >= 0
        )
        
    def to_dict(self) -> Dict:
        """Convert to dictionary (for API responses)"""
        return {
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'score': self.score,
            'rank': self.rank
        }
        
    @staticmethod
    def calculate_percentile(rank: int, total_users: int) -> float:
        """Calculate percentile rank"""
        if total_users == 0:
            return 0.0
        return ((total_users - rank) / total_users) * 100
        
    @staticmethod
    def get_rank_label(rank: int) -> str:
        """Get rank label (e.g., 1st, 2nd, 3rd)"""
        if rank % 100 in [11, 12, 13]:
            return f"{rank}th"
        elif rank % 10 == 1:
            return f"{rank}st"
        elif rank % 10 == 2:
            return f"{rank}nd"
        elif rank % 10 == 3:
            return f"{rank}rd"
        else:
            return f"{rank}th"
            
    @staticmethod
    def get_medal(rank: int) -> str:
        """Get medal based on rank"""
        if rank == 1:
            return "🥇"
        elif rank == 2:
            return "🥈"
        elif rank == 3:
            return "��"
        return "" 