from typing import List, Optional, Dict
from datetime import datetime
import logging

from backend.dao.base_dao import BaseDAO
from backend.dao.leaderboards.leaderboard_entity import LeaderboardEntity
from backend.utils.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class LeaderboardDAO(BaseDAO):
    """Data Access Object for leaderboards table."""

    def create_entry(self, user_id: int, topic_id: int, score: float) -> Optional[LeaderboardEntity]:
        """Creates a new leaderboard entry in the database."""
        try:
            query = """
                INSERT INTO leaderboards (user_id, topic_id, score, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = (user_id, topic_id, score, current_time, current_time)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                entry_id = cursor.lastrowid
                return LeaderboardEntity(entry_id, user_id, topic_id, score, current_time, current_time)
        except Exception as e:
            logger.error(f"Error creating leaderboard entry: {str(e)}")
            raise DatabaseError("Failed to create leaderboard entry")

    def get_entry_by_id(self, entry_id: int) -> Optional[LeaderboardEntity]:
        """Retrieves a leaderboard entry by its ID."""
        try:
            query = "SELECT * FROM leaderboards WHERE id = %s"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (entry_id,))
                row = cursor.fetchone()
                return LeaderboardEntity.from_db_row(row) if row else None
        except Exception as e:
            logger.error(f"Error retrieving leaderboard entry {entry_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve leaderboard entry {entry_id}")

    def get_entries_by_topic(self, topic_id: int) -> List[LeaderboardEntity]:
        """Retrieves all leaderboard entries for a specific topic."""
        try:
            query = "SELECT * FROM leaderboards WHERE topic_id = %s ORDER BY score DESC"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (topic_id,))
                rows = cursor.fetchall()
                return [LeaderboardEntity.from_db_row(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving leaderboard entries for topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve leaderboard entries for topic {topic_id}")

    def get_entries_by_user(self, user_id: int) -> List[LeaderboardEntity]:
        """Retrieves all leaderboard entries for a specific user."""
        try:
            query = "SELECT * FROM leaderboards WHERE user_id = %s ORDER BY score DESC"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, (user_id,))
                rows = cursor.fetchall()
                return [LeaderboardEntity.from_db_row(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving leaderboard entries for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve leaderboard entries for user {user_id}")

    def get_entry_by_user_and_topic(self, user_id: int, topic_id: int) -> Optional[LeaderboardEntity]:
        """Retrieves a leaderboard entry for a specific user in a specific topic."""
        try:
            query = "SELECT * FROM leaderboards WHERE user_id = %s AND topic_id = %s"
            params = (user_id, topic_id)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                return LeaderboardEntity.from_db_row(row) if row else None
        except Exception as e:
            logger.error(f"Error retrieving leaderboard entry for user {user_id} in topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve leaderboard entry for user {user_id} in topic {topic_id}")

    def update_score(self, entry_id: int, new_score: float) -> bool:
        """Updates the score of a leaderboard entry."""
        try:
            query = """
                UPDATE leaderboards
                SET score = %s, updated_at = %s
                WHERE id = %s
            """
            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = (new_score, updated_at, entry_id)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating score for leaderboard entry {entry_id}: {str(e)}")
            raise DatabaseError(f"Failed to update score for leaderboard entry {entry_id}")

    def get_top_scores(self, topic_id: int, limit: int = 10) -> List[Dict]:
        """Retrieves top scores for a specific topic."""
        try:
            query = """
                SELECT l.*, u.username
                FROM leaderboards l
                JOIN users u ON l.user_id = u.id
                WHERE l.topic_id = %s
                ORDER BY l.score DESC
                LIMIT %s
            """
            params = (topic_id, limit)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [{
                    'rank': idx + 1,
                    'user_id': row[1],
                    'username': row[6],
                    'score': float(row[3]),
                    'updated_at': row[5]
                } for idx, row in enumerate(rows)]
        except Exception as e:
            logger.error(f"Error retrieving top scores for topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve top scores for topic {topic_id}")

    def get_user_rank(self, user_id: int, topic_id: int) -> Optional[int]:
        """Retrieves the rank of a user in a specific topic."""
        try:
            query = """
                SELECT user_rank
                FROM (
                    SELECT user_id, RANK() OVER (ORDER BY score DESC) as user_rank
                    FROM leaderboards
                    WHERE topic_id = %s
                ) ranked
                WHERE user_id = %s
            """
            params = (topic_id, user_id)
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                return int(row[0]) if row else None
        except Exception as e:
            logger.error(f"Error retrieving rank for user {user_id} in topic {topic_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve rank for user {user_id} in topic {topic_id}") 