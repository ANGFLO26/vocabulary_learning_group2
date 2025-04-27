from typing import List, Optional, Dict
from backend.dao.leaderboards.leaderboard_dao import LeaderboardDAO
from backend.business_layer.interfaces.leaderboard_service_interface import ILeaderboardService
from backend.dao.leaderboards.leaderboard_class import Leaderboard

class LeaderboardService(ILeaderboardService):
    """Implementation of Leaderboard Service"""
    
    def __init__(self, leaderboard_dao: LeaderboardDAO):
        self.leaderboard_dao = leaderboard_dao
        
    def get_topic_leaderboard(self, topic_id: int) -> List[Leaderboard]:
        """Get leaderboard for a topic"""
        entities = self.leaderboard_dao.get_by_topic(topic_id)
        return [Leaderboard.from_entity(entity) for entity in entities]
        
    def update_user_score(self, user_id: int, topic_id: int, score: int) -> Optional[Leaderboard]:
        """Update user's score in leaderboard"""
        # Get existing entry
        entity = self.leaderboard_dao.get_by_user_and_topic(user_id, topic_id)
        
        if entity:
            # Update existing entry
            entity = self.leaderboard_dao.update(
                id=entity.id,
                user_id=user_id,
                topic_id=topic_id,
                score=score
            )
        else:
            # Create new entry
            entity = self.leaderboard_dao.create(
                user_id=user_id,
                topic_id=topic_id,
                score=score
            )
            
        if not entity:
            return None
            
        return Leaderboard.from_entity(entity)
        
    def get_user_rank(self, user_id: int, topic_id: int) -> Optional[int]:
        """Get user's rank in topic leaderboard"""
        leaderboard = self.get_topic_leaderboard(topic_id)
        if not leaderboard:
            return None
            
        # Sort by score descending
        leaderboard.sort(key=lambda x: x.score, reverse=True)
        
        # Find user's rank
        for i, entry in enumerate(leaderboard, 1):
            if entry.user_id == user_id:
                return i
                
        return None
        
    def get_top_users(self, topic_id: int, limit: int = 10) -> List[Leaderboard]:
        """Get top users in topic leaderboard"""
        leaderboard = self.get_topic_leaderboard(topic_id)
        if not leaderboard:
            return []
            
        # Sort by score descending
        leaderboard.sort(key=lambda x: x.score, reverse=True)
        
        # Return top users
        return leaderboard[:limit]
        
    def get_user_statistics(self, user_id: int) -> Dict:
        """Get user's leaderboard statistics"""
        entities = self.leaderboard_dao.get_by_user(user_id)
        if not entities:
            return {
                'total_topics': 0,
                'total_score': 0,
                'average_rank': 0,
                'top_rankings': []
            }
            
        total_topics = len(entities)
        total_score = sum(entity.score for entity in entities)
        top_rankings = []
        
        for entity in entities:
            rank = self.get_user_rank(user_id, entity.topic_id)
            if rank:
                top_rankings.append({
                    'topic_id': entity.topic_id,
                    'score': entity.score,
                    'rank': rank
                })
                
        # Sort by rank ascending
        top_rankings.sort(key=lambda x: x['rank'])
        
        return {
            'total_topics': total_topics,
            'total_score': total_score,
            'average_rank': sum(ranking['rank'] for ranking in top_rankings) / total_topics,
            'top_rankings': top_rankings[:5]  # Top 5 rankings
        }
        
    def get_topic_statistics(self, topic_id: int) -> Dict:
        """Get topic's leaderboard statistics"""
        leaderboard = self.get_topic_leaderboard(topic_id)
        if not leaderboard:
            return {
                'total_users': 0,
                'average_score': 0,
                'top_score': 0,
                'top_users': []
            }
            
        total_users = len(leaderboard)
        total_score = sum(entry.score for entry in leaderboard)
        
        # Sort by score descending
        leaderboard.sort(key=lambda x: x.score, reverse=True)
        
        return {
            'total_users': total_users,
            'average_score': total_score / total_users,
            'top_score': leaderboard[0].score if leaderboard else 0,
            'top_users': [entry.to_dict() for entry in leaderboard[:5]]  # Top 5 users
        } 