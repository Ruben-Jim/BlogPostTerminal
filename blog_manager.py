"""
Blog Manager - Core business logic for managing blog posts
"""

import os
import json
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
from collections import Counter
import re

from models import BlogPost
from storage import JSONStorage
from utils import generate_post_id, sanitize_filename

class BlogManager:
    """Main class for managing blog posts"""
    
    def __init__(self, data_dir: str = "./blog_data"):
        self.data_dir = data_dir
        self.storage = JSONStorage(data_dir)
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def create_post(self, post: BlogPost) -> str:
        """Create a new blog post and return its ID"""
        post_id = generate_post_id(post.title)
        
        # Ensure unique ID
        counter = 1
        original_id = post_id
        while self.storage.post_exists(post_id):
            post_id = f"{original_id}-{counter}"
            counter += 1
        
        self.storage.save_post(post_id, post)
        return post_id
    
    def get_post(self, post_id: str) -> Optional[BlogPost]:
        """Get a blog post by ID"""
        return self.storage.load_post(post_id)
    
    def update_post(self, post_id: str, post: BlogPost) -> bool:
        """Update an existing blog post"""
        if not self.storage.post_exists(post_id):
            return False
        
        self.storage.save_post(post_id, post)
        return True
    
    def delete_post(self, post_id: str) -> bool:
        """Delete a blog post"""
        return self.storage.delete_post(post_id)
    
    def list_posts(self, limit: int = 10, tag: Optional[str] = None, 
                   author: Optional[str] = None) -> List[Tuple[str, BlogPost]]:
        """List blog posts with optional filtering"""
        all_posts = self.storage.load_all_posts()
        
        # Apply filters
        filtered_posts = []
        for post_id, post in all_posts:
            if tag and tag not in post.tags:
                continue
            if author and post.author.lower() != author.lower():
                continue
            filtered_posts.append((post_id, post))
        
        # Sort by creation date (newest first)
        filtered_posts.sort(key=lambda x: x[1].created_at, reverse=True)
        
        # Apply limit
        return filtered_posts[:limit]
    
    def search_posts(self, query: str) -> List[Tuple[str, BlogPost]]:
        """Search for blog posts by title or content"""
        all_posts = self.storage.load_all_posts()
        results = []
        
        query_lower = query.lower()
        
        for post_id, post in all_posts:
            # Search in title and content
            if (query_lower in post.title.lower() or 
                query_lower in post.content.lower() or
                any(query_lower in tag.lower() for tag in post.tags)):
                results.append((post_id, post))
        
        # Sort by relevance (title matches first, then content matches)
        def relevance_score(item):
            post_id, post = item
            score = 0
            if query_lower in post.title.lower():
                score += 10
            if query_lower in post.content.lower():
                score += 5
            if any(query_lower in tag.lower() for tag in post.tags):
                score += 3
            return score
        
        results.sort(key=relevance_score, reverse=True)
        return results
    
    def export_posts(self, output_dir: str, format: str = 'markdown') -> List[str]:
        """Export all blog posts to static files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        all_posts = self.storage.load_all_posts()
        exported_files = []
        
        for post_id, post in all_posts:
            filename = self._generate_export_filename(post_id, post, format)
            filepath = os.path.join(output_dir, filename)
            
            if format == 'markdown':
                content = self._export_as_markdown(post)
            elif format == 'html':
                content = self._export_as_html(post)
            elif format == 'json':
                content = self._export_as_json(post)
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            exported_files.append(filename)
        
        return exported_files
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get blog statistics"""
        all_posts = self.storage.load_all_posts()
        
        if not all_posts:
            return {
                'total_posts': 0,
                'total_authors': 0,
                'total_tags': 0,
                'most_active_author': 'None',
                'most_used_tags': [],
                'avg_post_length': 0
            }
        
        authors = [post.author for _, post in all_posts]
        all_tags = []
        total_content_length = 0
        
        for _, post in all_posts:
            all_tags.extend(post.tags)
            total_content_length += len(post.content)
        
        author_counter = Counter(authors)
        tag_counter = Counter(all_tags)
        
        return {
            'total_posts': len(all_posts),
            'total_authors': len(set(authors)),
            'total_tags': len(set(all_tags)),
            'most_active_author': author_counter.most_common(1)[0][0] if author_counter else 'None',
            'most_used_tags': [tag for tag, _ in tag_counter.most_common(10)],
            'avg_post_length': total_content_length // len(all_posts) if all_posts else 0
        }
    
    def _generate_export_filename(self, post_id: str, post: BlogPost, format: str) -> str:
        """Generate filename for exported post"""
        safe_title = sanitize_filename(post.title)
        date_str = post.created_at.strftime('%Y-%m-%d')
        extension = {'markdown': 'md', 'html': 'html', 'json': 'json'}[format]
        
        return f"{date_str}-{safe_title}.{extension}"
    
    def _export_as_markdown(self, post: BlogPost) -> str:
        """Export post as markdown"""
        tags_str = ", ".join(post.tags) if post.tags else "None"
        
        content = f"""---
title: {post.title}
author: {post.author}
tags: [{tags_str}]
created: {post.created_at.isoformat()}
updated: {post.updated_at.isoformat() if post.updated_at else 'Never'}
---

# {post.title}

**Author:** {post.author}  
**Tags:** {tags_str}  
**Created:** {post.created_at.strftime('%Y-%m-%d %H:%M:%S')}  
**Updated:** {post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else 'Never'}

---

{post.content}
"""
        return content
    
    def _export_as_html(self, post: BlogPost) -> str:
        """Export post as HTML"""
        tags_str = ", ".join(post.tags) if post.tags else "None"
        
        # Simple markdown-like formatting
        content_html = post.content.replace('\n', '<br>\n')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .meta {{ color: #666; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }}
        .content {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <h1>{post.title}</h1>
    <div class="meta">
        <p><strong>Author:</strong> {post.author}</p>
        <p><strong>Tags:</strong> {tags_str}</p>
        <p><strong>Created:</strong> {post.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Updated:</strong> {post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else 'Never'}</p>
    </div>
    <div class="content">
        {content_html}
    </div>
</body>
</html>"""
        return html
    
    def _export_as_json(self, post: BlogPost) -> str:
        """Export post as JSON"""
        post_dict = {
            'title': post.title,
            'content': post.content,
            'author': post.author,
            'tags': post.tags,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat() if post.updated_at else None
        }
        
        return json.dumps(post_dict, indent=2, ensure_ascii=False)
