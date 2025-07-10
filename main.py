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
from rich.layout import Layout
from rich.align import Align
from rich.columns import Columns
from rich.live import Live
from rich.rule import Rule
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime
import json
import time

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
        
        # Ask if user wants to view in GUI
        try:
            if Confirm.ask("View all posts in GUI interface?", default=True):
                display_blog_gui()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[green]Post created successfully! Use 'python main.py gui' to view all posts.[/green]")
        
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

@cli.command()
def gui():
    """Launch interactive GUI interface for viewing blog posts"""
    display_blog_gui()

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

def display_blog_gui():
    """Display an interactive GUI interface for viewing blog posts"""
    console.clear()
    
    # Get all posts
    posts = blog_manager.list_posts(limit=50)
    
    if not posts:
        console.print(Panel("[yellow]No blog posts found. Create your first post with:[/yellow]\n[cyan]python main.py create[/cyan]", 
                          title="🔍 Empty Blog", border_style="yellow"))
        return
    
    # Create header
    header = Panel(
        "[bold blue]🌟 Blog Management System - GUI Interface 🌟[/bold blue]\n" +
        f"[dim]Total Posts: {len(posts)} | Press Ctrl+C to exit[/dim]",
        border_style="blue"
    )
    
    console.print(header)
    console.print()
    
    # Show animated loading
    with console.status("[bold green]Loading your blog posts...", spinner="dots"):
        time.sleep(1)
    
    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    
    # Split body into sidebar and main content
    layout["body"].split_row(
        Layout(name="sidebar", minimum_size=30),
        Layout(name="main", ratio=2)
    )
    
    # Create sidebar with post list
    sidebar_content = create_sidebar_content(posts)
    layout["sidebar"].update(sidebar_content)
    
    # Create main content area
    main_content = create_main_content(posts)
    layout["main"].update(main_content)
    
    # Create footer
    footer_content = Panel(
        "[bold cyan]Navigation:[/bold cyan] Use [yellow]'python main.py view <post-id>'[/yellow] to read full posts | " +
        "[green]'python main.py create'[/green] to add new posts",
        border_style="cyan"
    )
    layout["footer"].update(footer_content)
    
    # Display the layout
    console.print(layout)
    
    # Interactive menu loop
    console.print("\n[bold green]🎛️  Interactive Menu:[/bold green]")
    console.print("[dim]Press Ctrl+C to exit anytime[/dim]")
    
    while True:
        try:
            console.print("\n[bold cyan]Choose an option:[/bold cyan]")
            console.print("[cyan]1.[/cyan] View a specific post")
            console.print("[cyan]2.[/cyan] Create a new post")
            console.print("[cyan]3.[/cyan] Search posts")
            console.print("[cyan]4.[/cyan] Show statistics")
            console.print("[cyan]5.[/cyan] Refresh GUI")
            console.print("[cyan]6.[/cyan] List all posts (table view)")
            console.print("[cyan]7.[/cyan] Exit")
            
            choice = Prompt.ask("[yellow]Enter your choice (1-7)[/yellow]", choices=["1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "1":
                # View specific post
                post_id = Prompt.ask("[blue]Enter post ID to view[/blue]")
                post = blog_manager.get_post(post_id)
                if post:
                    console.clear()
                    display_full_post(post, post_id)
                    Prompt.ask("[dim]Press Enter to return to GUI...[/dim]", default="")
                    console.clear()
                    return display_blog_gui()  # Refresh GUI
                else:
                    console.print(f"[red]Post '{post_id}' not found[/red]")
            
            elif choice == "2":
                # Create new post
                console.clear()
                console.print("[green]Creating new post...[/green]")
                title = Prompt.ask("[blue]Post title[/blue]")
                content = click.edit('\n# Write your blog post content here...\n')
                if content:
                    tags_input = Prompt.ask("[blue]Tags (comma-separated)[/blue]", default="")
                    author = Prompt.ask("[blue]Author name[/blue]", default="Anonymous")
                    
                    # Create the post
                    tag_list = validate_tags(tags_input) if tags_input else []
                    post = BlogPost(
                        title=title,
                        content=content.strip(),
                        tags=tag_list,
                        author=author
                    )
                    
                    post_id = blog_manager.create_post(post)
                    console.print(f"[green]✓ Blog post created successfully with ID: {post_id}[/green]")
                    display_post_summary(post, post_id)
                    
                    Prompt.ask("[dim]Press Enter to return to GUI...[/dim]", default="")
                    console.clear()
                    return display_blog_gui()  # Refresh GUI
                else:
                    console.print("[red]No content provided[/red]")
            
            elif choice == "3":
                # Search posts
                query = Prompt.ask("[blue]Enter search term[/blue]")
                results = blog_manager.search_posts(query)
                console.clear()
                
                if results:
                    console.print(f"[green]Found {len(results)} posts matching '{query}':[/green]\n")
                    for i, (post_id, post) in enumerate(results, 1):
                        console.print(f"[cyan]{i}.[/cyan] {post.title} ([dim]{post_id}[/dim])")
                    
                    console.print("\n[yellow]Enter post number to view, or press Enter to return:[/yellow]")
                    try:
                        post_choice = Prompt.ask("Choice", default="")
                        if post_choice.isdigit():
                            idx = int(post_choice) - 1
                            if 0 <= idx < len(results):
                                post_id, post = results[idx]
                                console.clear()
                                display_full_post(post, post_id)
                                Prompt.ask("[dim]Press Enter to return to GUI...[/dim]", default="")
                    except (ValueError, IndexError):
                        pass
                else:
                    console.print(f"[yellow]No posts found matching '{query}'[/yellow]")
                    Prompt.ask("[dim]Press Enter to return to GUI...[/dim]", default="")
                
                console.clear()
                return display_blog_gui()  # Refresh GUI
            
            elif choice == "4":
                # Show statistics
                console.clear()
                stats = blog_manager.get_statistics()
                display_stats_gui(stats)
                Prompt.ask("[dim]Press Enter to return to GUI...[/dim]", default="")
                console.clear()
                return display_blog_gui()  # Refresh GUI
            
            elif choice == "5":
                # Refresh GUI
                console.clear()
                return display_blog_gui()
            
            elif choice == "6":
                # List all posts in table view
                console.clear()
                posts = blog_manager.list_posts(limit=50)
                
                if posts:
                    table = Table(title="All Blog Posts")
                    table.add_column("ID", style="cyan", no_wrap=True)
                    table.add_column("Title", style="magenta")
                    table.add_column("Author", style="green")
                    table.add_column("Tags", style="blue")
                    table.add_column("Created", style="yellow")
                    
                    for post_id, post in posts:
                        tags_str = ", ".join(post.tags) if post.tags else "None"
                        table.add_row(
                            post_id,
                            truncate_text(post.title, 30),
                            post.author,
                            truncate_text(tags_str, 20),
                            format_date(post.created_at)
                        )
                    
                    console.print(table)
                else:
                    console.print("[yellow]No posts found[/yellow]")
                
                Prompt.ask("[dim]Press Enter to return to GUI...[/dim]", default="")
                console.clear()
                return display_blog_gui()  # Refresh GUI
            
            elif choice == "7":
                # Exit
                console.print("[green]Goodbye![/green]")
                break
                
        except KeyboardInterrupt:
            console.print("\n[green]Goodbye![/green]")
            break
        except EOFError:
            console.print("\n[green]Goodbye![/green]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            Prompt.ask("[dim]Press Enter to continue...[/dim]", default="")

def create_sidebar_content(posts):
    """Create sidebar content showing list of posts"""
    tree = Tree("📚 [bold blue]Your Blog Posts[/bold blue]")
    
    for post_id, post in posts[:10]:  # Show first 10 posts
        # Create a branch for each post
        post_branch = tree.add(f"[green]{post.title}[/green]")
        post_branch.add(f"[dim]ID:[/dim] [cyan]{post_id}[/cyan]")
        post_branch.add(f"[dim]Author:[/dim] [yellow]{post.author}[/yellow]")
        post_branch.add(f"[dim]Created:[/dim] [magenta]{format_date(post.created_at)}[/magenta]")
        
        if post.tags:
            tags_str = ", ".join(post.tags[:3])  # Show first 3 tags
            post_branch.add(f"[dim]Tags:[/dim] [blue]{tags_str}[/blue]")
    
    if len(posts) > 10:
        tree.add(f"[dim]... and {len(posts) - 10} more posts[/dim]")
    
    return Panel(tree, title="📋 Posts Overview", border_style="green")

def create_main_content(posts):
    """Create main content area with recent posts"""
    if not posts:
        return Panel("[yellow]No posts to display[/yellow]", title="📝 Recent Posts", border_style="yellow")
    
    # Show the 3 most recent posts
    recent_posts = posts[:3]
    
    content_panels = []
    for post_id, post in recent_posts:
        tags_str = ", ".join(post.tags) if post.tags else "None"
        
        post_content = f"""
[bold magenta]{post.title}[/bold magenta]
[blue]By:[/blue] {post.author} | [blue]Created:[/blue] {format_date(post.created_at)}
[blue]Tags:[/blue] {tags_str}
[blue]ID:[/blue] {post_id}

[dim]{truncate_text(post.content, 200)}[/dim]
        """
        
        content_panels.append(Panel(post_content, border_style="magenta"))
    
    if len(posts) > 3:
        content_panels.append(Panel(
            f"[dim]... and {len(posts) - 3} more posts available[/dim]",
            border_style="blue"
        ))
    
    return Columns(content_panels, equal=True)

def display_stats_gui(stats):
    """Display statistics in a GUI format"""
    console.print(Panel(
        f"""
[bold cyan]📊 Blog Analytics Dashboard[/bold cyan]

[green]📝 Total Posts:[/green] {stats['total_posts']}
[green]👥 Total Authors:[/green] {stats['total_authors']}
[green]🏷️  Total Tags:[/green] {stats['total_tags']}
[green]⭐ Most Active Author:[/green] {stats['most_active_author']}
[green]🔥 Popular Tags:[/green] {', '.join(stats['most_used_tags'][:5])}
[green]📏 Average Post Length:[/green] {stats['avg_post_length']} characters

[dim]Keep writing to grow your blog![/dim]
        """,
        title="📈 Statistics",
        border_style="cyan"
    ))

if __name__ == '__main__':
    cli()
