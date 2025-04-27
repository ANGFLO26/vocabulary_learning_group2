from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from backend.dao.leaderboards.leaderboard_class import Leaderboard

class ILeaderboardService(ABC):
    """Interface for Leaderboard Service"""
    
    @abstractmethod
    def get_topic_leaderboard(self, topic_id: int) -> List[Leaderboard]:
        """Get leaderboard for a specific topic"""
        pass
        
    @abstractmethod
    def update_user_score(self, user_id: int, topic_id: int, score: int) -> bool:
        """Update user's score in leaderboard"""
        pass
        
    @abstractmethod
    def get_user_rank(self, user_id: int, topic_id: int) -> Optional[int]:
        """Get user's rank in topic leaderboard"""
        pass
        
    @abstractmethod
    def get_top_users(self, topic_id: int, limit: int = 10) -> List[Leaderboard]:
        """Get top users in topic leaderboard"""
        pass
        
    @abstractmethod
    def get_user_statistics(self, user_id: int, topic_id: int) -> Dict:
        """Get user's leaderboard statistics"""
        pass
        
    @abstractmethod
    def get_topic_statistics(self, topic_id: int) -> Dict:
        """Get topic's leaderboard statistics"""
        pass 