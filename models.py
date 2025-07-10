"""
Data models for the blog management system
"""

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
import json

@dataclass
class BlogPost:
    """Blog post data model"""
    title: str
    content: str
    author: str = "Anonymous"
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert blog post to dictionary"""
        return {
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'BlogPost':
        """Create blog post from dictionary"""
        created_at = datetime.fromisoformat(data['created_at'])
        updated_at = None
        if data.get('updated_at'):
            updated_at = datetime.fromisoformat(data['updated_at'])
        
        return cls(
            title=data['title'],
            content=data['content'],
            author=data.get('author', 'Anonymous'),
            tags=data.get('tags', []),
            created_at=created_at,
            updated_at=updated_at
        )
    
    def to_json(self) -> str:
        """Convert blog post to JSON string"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BlogPost':
        """Create blog post from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def __str__(self) -> str:
        """String representation of blog post"""
        return f"BlogPost(title='{self.title}', author='{self.author}', tags={self.tags})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return self.__str__()
