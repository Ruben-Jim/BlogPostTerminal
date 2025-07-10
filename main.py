#!/usr/bin/env python3
"""
Terminal-based Blog Management Application
Main entry point for the CLI interface
"""

import click
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
import json

from blog_manager import BlogManager
from models import BlogPost
from utils import validate_tags, format_date, truncate_text

console = Console()
blog_manager = BlogManager()

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    Terminal-based Blog Management System
    
    A command-line interface for creating, editing, and managing blog posts.
    """
    pass

@cli.command()
@click.option('--title', prompt='Post title', help='Title of the blog post')
@click.option('--content', help='Content of the blog post (use editor if not provided)')
@click.option('--tags', help='Comma-separated tags for the post')
@click.option('--author', help='Author name')
def create(title, content, tags, author):
    """Create a new blog post"""
    try:
        # Get content from editor if not provided
        if not content:
            content = click.edit('\n# Write your blog post content here...\n')
            if not content:
                console.print("[red]Error: No content provided[/red]")
                return
        
        # Parse tags
        tag_list = []
        if tags:
            tag_list = validate_tags(tags)
        
        # Create the blog post
        post = BlogPost(
            title=title,
            content=content.strip(),
            tags=tag_list,
            author=author or "Anonymous"
        )
        
        post_id = blog_manager.create_post(post)
        
        console.print(f"[green]✓ Blog post created successfully with ID: {post_id}[/green]")
        
        # Display the created post
        display_post_summary(post, post_id)
        
    except Exception as e:
        console.print(f"[red]Error creating post: {str(e)}[/red]")

@cli.command()
@click.argument('post_id')
def edit(post_id):
    """Edit an existing blog post"""
    try:
        post = blog_manager.get_post(post_id)
        if not post:
            console.print(f"[red]Error: Post with ID '{post_id}' not found[/red]")
            return
        
        console.print(f"[blue]Editing post: {post.title}[/blue]")
        
        # Edit title
        new_title = Prompt.ask("New title", default=post.title)
        
        # Edit content
        new_content = click.edit(post.content)
        if new_content is None:
            new_content = post.content
        
        # Edit tags
        current_tags = ", ".join(post.tags)
        new_tags_input = Prompt.ask("Tags (comma-separated)", default=current_tags)
        new_tags = validate_tags(new_tags_input) if new_tags_input else []
        
        # Edit author
        new_author = Prompt.ask("Author", default=post.author)
        
        # Update the post
        post.title = new_title
        post.content = new_content.strip()
        post.tags = new_tags
        post.author = new_author
        post.updated_at = datetime.now()
        
        blog_manager.update_post(post_id, post)
        
        console.print(f"[green]✓ Post '{post_id}' updated successfully[/green]")
        
    except Exception as e:
        console.print(f"[red]Error editing post: {str(e)}[/red]")

@cli.command()
@click.argument('post_id')
def view(post_id):
    """View a specific blog post"""
    try:
        post = blog_manager.get_post(post_id)
        if not post:
            console.print(f"[red]Error: Post with ID '{post_id}' not found[/red]")
            return
        
        display_full_post(post, post_id)
        
    except Exception as e:
        console.print(f"[red]Error viewing post: {str(e)}[/red]")

@cli.command()
@click.option('--limit', default=10, help='Number of posts to display')
@click.option('--tag', help='Filter by tag')
@click.option('--author', help='Filter by author')
def list(limit, tag, author):
    """List all blog posts"""
    try:
        posts = blog_manager.list_posts(limit=limit, tag=tag, author=author)
        
        if not posts:
            console.print("[yellow]No blog posts found[/yellow]")
            return
        
        table = Table(title="Blog Posts")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Author", style="green")
        table.add_column("Tags", style="blue")
        table.add_column("Created", style="yellow")
        table.add_column("Updated", style="yellow")
        
        for post_id, post in posts:
            tags_str = ", ".join(post.tags) if post.tags else "None"
            table.add_row(
                post_id,
                truncate_text(post.title, 30),
                post.author,
                truncate_text(tags_str, 20),
                format_date(post.created_at),
                format_date(post.updated_at) if post.updated_at else "Never"
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error listing posts: {str(e)}[/red]")

@cli.command()
@click.argument('query')
def search(query):
    """Search blog posts by title or content"""
    try:
        results = blog_manager.search_posts(query)
        
        if not results:
            console.print(f"[yellow]No posts found matching '{query}'[/yellow]")
            return
        
        console.print(f"[blue]Found {len(results)} post(s) matching '{query}':[/blue]")
        
        for post_id, post in results:
            display_post_summary(post, post_id)
            console.print("---")
        
    except Exception as e:
        console.print(f"[red]Error searching posts: {str(e)}[/red]")

@cli.command()
@click.argument('post_id')
def delete(post_id):
    """Delete a blog post"""
    try:
        post = blog_manager.get_post(post_id)
        if not post:
            console.print(f"[red]Error: Post with ID '{post_id}' not found[/red]")
            return
        
        console.print(f"[yellow]Post to delete: {post.title}[/yellow]")
        
        if Confirm.ask("Are you sure you want to delete this post?"):
            blog_manager.delete_post(post_id)
            console.print(f"[green]✓ Post '{post_id}' deleted successfully[/green]")
        else:
            console.print("[blue]Delete operation cancelled[/blue]")
        
    except Exception as e:
        console.print(f"[red]Error deleting post: {str(e)}[/red]")

@cli.command()
@click.option('--output-dir', default='./blog_export', help='Directory to export posts to')
@click.option('--format', type=click.Choice(['markdown', 'html', 'json']), default='markdown', help='Export format')
def export(output_dir, format):
    """Export all blog posts to static files"""
    try:
        exported_files = blog_manager.export_posts(output_dir, format)
        
        if not exported_files:
            console.print("[yellow]No posts to export[/yellow]")
            return
        
        console.print(f"[green]✓ Exported {len(exported_files)} post(s) to '{output_dir}'[/green]")
        
        for filename in exported_files:
            console.print(f"  - {filename}")
        
    except Exception as e:
        console.print(f"[red]Error exporting posts: {str(e)}[/red]")

@cli.command()
def stats():
    """Show blog statistics"""
    try:
        stats = blog_manager.get_statistics()
        
        panel_content = f"""
[bold blue]Blog Statistics[/bold blue]

[green]Total Posts:[/green] {stats['total_posts']}
[green]Total Authors:[/green] {stats['total_authors']}
[green]Total Tags:[/green] {stats['total_tags']}
[green]Most Active Author:[/green] {stats['most_active_author']}
[green]Most Used Tags:[/green] {', '.join(stats['most_used_tags'][:5])}
[green]Average Post Length:[/green] {stats['avg_post_length']} characters
        """
        
        console.print(Panel(panel_content, title="Blog Statistics", border_style="blue"))
        
    except Exception as e:
        console.print(f"[red]Error getting statistics: {str(e)}[/red]")

def display_post_summary(post, post_id):
    """Display a summary of a blog post"""
    tags_str = ", ".join(post.tags) if post.tags else "None"
    
    panel_content = f"""
[bold magenta]{post.title}[/bold magenta]
[blue]ID:[/blue] {post_id}
[blue]Author:[/blue] {post.author}
[blue]Tags:[/blue] {tags_str}
[blue]Created:[/blue] {format_date(post.created_at)}
[blue]Updated:[/blue] {format_date(post.updated_at) if post.updated_at else "Never"}

[dim]{truncate_text(post.content, 200)}[/dim]
    """
    
    console.print(Panel(panel_content, border_style="green"))

def display_full_post(post, post_id):
    """Display a full blog post"""
    tags_str = ", ".join(post.tags) if post.tags else "None"
    
    # Header
    header = f"""
[bold magenta]{post.title}[/bold magenta]
[blue]ID:[/blue] {post_id} | [blue]Author:[/blue] {post.author} | [blue]Tags:[/blue] {tags_str}
[blue]Created:[/blue] {format_date(post.created_at)} | [blue]Updated:[/blue] {format_date(post.updated_at) if post.updated_at else "Never"}
    """
    
    console.print(Panel(header, border_style="blue"))
    
    # Content
    console.print("\n[bold]Content:[/bold]")
    console.print(post.content)
    console.print("\n" + "="*50 + "\n")

if __name__ == '__main__':
    cli()
