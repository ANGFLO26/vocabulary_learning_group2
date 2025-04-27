from dataclasses import dataclass
from typing import Optional

@dataclass
class LeaderboardEntity:
    """Entity representing a leaderboard entry in the database"""
    user_id: int
    topic_id: int
    score: int
    rank: Optional[int] = None
    
    @staticmethod
    def from_db_row(row: tuple) -> 'LeaderboardEntity':
        """Create LeaderboardEntity from database row"""
        return LeaderboardEntity(
            user_id=row[0],
            topic_id=row[1],
            score=row[2],
            rank=row[3] if len(row) > 3 else None
        )
        
    def to_db_tuple(self) -> tuple:
        """Convert to database tuple for insertion/update"""
        return (
            self.user_id,
            self.topic_id,
            self.score
        ) 