from abc import ABC, abstractmethod
from typing import List, Optional
from .leaderboard_entity import LeaderboardEntity

class ILeaderboardDAO(ABC):
    """Interface for Leaderboard Data Access Object"""
    
    @abstractmethod
    def get_by_topic(self, topic_id: int) -> List[LeaderboardEntity]:
        """Get leaderboard for a specific topic"""
        pass
        
    @abstractmethod
    def update_score(self, user_id: int, topic_id: int, score: int) -> bool:
        """Update user's score in leaderboard"""
        pass
        
    @abstractmethod
    def get_user_rank(self, user_id: int, topic_id: int) -> Optional[int]:
        """Get user's rank in topic leaderboard"""
        pass
        
    @abstractmethod
    def get_top_users(self, topic_id: int, limit: int = 10) -> List[LeaderboardEntity]:
        """Get top users in topic leaderboard"""
        pass 