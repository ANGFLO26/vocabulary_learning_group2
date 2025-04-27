from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class TopicEntity:
    """Represents a topic in the database."""
    id: Optional[int]
    name: str
    description: str
    created_by: int
    created_at: str

    @staticmethod
    def from_db_row(row: Tuple) -> 'TopicEntity':
        """Creates a TopicEntity from a database row."""
        return TopicEntity(
            id=row[0],
            name=row[1],
            description=row[2],
            created_by=row[3],
            created_at=row[4]
        ) 