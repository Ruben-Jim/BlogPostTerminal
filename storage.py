"""
Storage layer for blog posts using JSON files
"""

import os
import json
from typing import List, Tuple, Optional
from datetime import datetime

from models import BlogPost

class JSONStorage:
    """JSON-based storage for blog posts"""
    
    def __init__(self, data_dir: str = "./blog_data"):
        self.data_dir = data_dir
        self.posts_dir = os.path.join(data_dir, "posts")
        self.index_file = os.path.join(data_dir, "index.json")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure storage directories exist"""
        os.makedirs(self.posts_dir, exist_ok=True)
    
    def save_post(self, post_id: str, post: BlogPost) -> bool:
        """Save a blog post to storage"""
        try:
            # Save post data
            post_file = os.path.join(self.posts_dir, f"{post_id}.json")
            with open(post_file, 'w', encoding='utf-8') as f:
                json.dump(post.to_dict(), f, indent=2, ensure_ascii=False)
            
            # Update index
            self._update_index(post_id, post)
            return True
            
        except Exception as e:
            print(f"Error saving post {post_id}: {e}")
            return False
    
    def load_post(self, post_id: str) -> Optional[BlogPost]:
        """Load a blog post from storage"""
        try:
            post_file = os.path.join(self.posts_dir, f"{post_id}.json")
            if not os.path.exists(post_file):
                return None
            
            with open(post_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return BlogPost.from_dict(data)
            
        except Exception as e:
            print(f"Error loading post {post_id}: {e}")
            return None
    
    def delete_post(self, post_id: str) -> bool:
        """Delete a blog post from storage"""
        try:
            post_file = os.path.join(self.posts_dir, f"{post_id}.json")
            if os.path.exists(post_file):
                os.remove(post_file)
            
            # Remove from index
            self._remove_from_index(post_id)
            return True
            
        except Exception as e:
            print(f"Error deleting post {post_id}: {e}")
            return False
    
    def post_exists(self, post_id: str) -> bool:
        """Check if a post exists in storage"""
        post_file = os.path.join(self.posts_dir, f"{post_id}.json")
        return os.path.exists(post_file)
    
    def load_all_posts(self) -> List[Tuple[str, BlogPost]]:
        """Load all blog posts from storage"""
        posts = []
        
        try:
            # Get all post files
            for filename in os.listdir(self.posts_dir):
                if filename.endswith('.json'):
                    post_id = filename[:-5]  # Remove .json extension
                    post = self.load_post(post_id)
                    if post:
                        posts.append((post_id, post))
        except Exception as e:
            print(f"Error loading posts: {e}")
        
        return posts
    
    def _update_index(self, post_id: str, post: BlogPost):
        """Update the posts index file"""
        try:
            index = self._load_index()
            
            index[post_id] = {
                'title': post.title,
                'author': post.author,
                'tags': post.tags,
                'created_at': post.created_at.isoformat(),
                'updated_at': post.updated_at.isoformat() if post.updated_at else None
            }
            
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error updating index: {e}")
    
    def _remove_from_index(self, post_id: str):
        """Remove a post from the index file"""
        try:
            index = self._load_index()
            
            if post_id in index:
                del index[post_id]
                
                with open(self.index_file, 'w', encoding='utf-8') as f:
                    json.dump(index, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            print(f"Error removing from index: {e}")
    
    def _load_index(self) -> dict:
        """Load the posts index file"""
        try:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading index: {e}")
        
        return {}
    
    def get_index(self) -> dict:
        """Get the current posts index"""
        return self._load_index()
