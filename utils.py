"""
Utility functions for the blog management system
"""

import re
import os
from datetime import datetime
from typing import List
import unicodedata

def generate_post_id(title: str) -> str:
    """Generate a URL-friendly post ID from title"""
    # Convert to lowercase and replace spaces with hyphens
    post_id = title.lower().strip()
    
    # Remove special characters and keep only alphanumeric, hyphens, and underscores
    post_id = re.sub(r'[^\w\s-]', '', post_id)
    post_id = re.sub(r'[-\s]+', '-', post_id)
    
    # Remove leading/trailing hyphens
    post_id = post_id.strip('-')
    
    # Ensure it's not empty
    if not post_id:
        post_id = f"post-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return post_id

def validate_tags(tags_input: str) -> List[str]:
    """Validate and clean up tags input"""
    if not tags_input:
        return []
    
    tags = []
    for tag in tags_input.split(','):
        tag = tag.strip()
        if tag:
            # Remove special characters from tags
            clean_tag = re.sub(r'[^\w\s-]', '', tag)
            clean_tag = re.sub(r'\s+', ' ', clean_tag).strip()
            if clean_tag:
                tags.append(clean_tag)
    
    return list(set(tags))  # Remove duplicates

def sanitize_filename(filename: str) -> str:
    """Create a safe filename from a string"""
    # Normalize unicode characters
    filename = unicodedata.normalize('NFKD', filename)
    
    # Remove non-ASCII characters
    filename = filename.encode('ascii', 'ignore').decode('ascii')
    
    # Replace spaces and special characters with hyphens
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    
    # Remove leading/trailing hyphens
    filename = filename.strip('-')
    
    # Ensure it's not empty and not too long
    if not filename:
        filename = 'untitled'
    
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def format_date(date_obj: datetime) -> str:
    """Format datetime object for display"""
    if not date_obj:
        return "Never"
    
    now = datetime.now()
    diff = now - date_obj
    
    if diff.days == 0:
        if diff.seconds < 3600:  # Less than 1 hour
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:  # Less than 1 day
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.days == 1:
        return "Yesterday"
    elif diff.days < 7:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.days < 30:
        weeks = diff.days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        return date_obj.strftime('%Y-%m-%d')

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to specified length with ellipsis"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."

def word_count(text: str) -> int:
    """Count words in text"""
    return len(text.split())

def reading_time(text: str, words_per_minute: int = 200) -> int:
    """Estimate reading time in minutes"""
    word_count_val = word_count(text)
    return max(1, word_count_val // words_per_minute)

def validate_post_title(title: str) -> bool:
    """Validate post title"""
    if not title or not title.strip():
        return False
    
    if len(title.strip()) < 3:
        return False
    
    if len(title.strip()) > 200:
        return False
    
    return True

def validate_post_content(content: str) -> bool:
    """Validate post content"""
    if not content or not content.strip():
        return False
    
    if len(content.strip()) < 10:
        return False
    
    return True

def extract_summary(content: str, max_length: int = 200) -> str:
    """Extract summary from content"""
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content.strip())
    
    # Try to break at sentence boundary
    if len(content) <= max_length:
        return content
    
    # Find the last sentence that fits
    sentences = content.split('.')
    summary = ""
    
    for sentence in sentences:
        if len(summary + sentence + '.') <= max_length:
            summary += sentence + '.'
        else:
            break
    
    # If no complete sentence fits, truncate
    if not summary:
        summary = content[:max_length - 3] + "..."
    
    return summary.strip()
