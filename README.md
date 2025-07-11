# Blog Manager - Terminal-based Blog Management System

A beautiful, interactive terminal-based blog management system with a GUI interface built using Python, Click, and Rich.

## Features

- **Interactive GUI Interface**: Beautiful terminal-based GUI with sidebar, main content area, and navigation
- **Blog Post Management**: Create, edit, view, delete, and search blog posts
- **Rich Terminal Output**: Colorful, formatted output with tables, panels, and layouts
- **Cross-platform**: Works on Linux, macOS, and Windows
- **File-based Storage**: Simple JSON-based storage system
- **Export Functionality**: Export posts to Markdown, HTML, or JSON formats
- **Statistics Dashboard**: View blog analytics and statistics
- **Zsh Integration**: Easy-to-use Zsh script for seamless terminal experience

## Quick Start

### Option 1: Manual Setup
```bash
# Install dependencies
pip install click rich

# Run the blog manager
python main.py gui
```

### Option 2: Automated Zsh Installation
```bash
# Run the installation script
./install.sh

# After installation, reload your shell
source ~/.zshrc

# Launch the blog manager
blog gui
```

## Commands

### Using Python directly:
```bash
python main.py gui                    # Launch interactive GUI
python main.py create                 # Create new blog post
python main.py list                   # List all posts
python main.py view <post-id>         # View specific post
python main.py search <term>          # Search posts
python main.py edit <post-id>         # Edit existing post
python main.py delete <post-id>       # Delete post
python main.py stats                  # Show statistics
python main.py export                 # Export posts
```

### Using the Zsh script:
```bash
blog gui                              # Launch interactive GUI
blog create                           # Create new blog post
blog list                             # List all posts
blog view <post-id>                   # View specific post
blog search <term>                    # Search posts
blog edit <post-id>                   # Edit existing post
blog delete <post-id>                 # Delete post
blog stats                            # Show statistics
blog export                           # Export posts
```

### Quick aliases (after installation):
```bash
blog-gui                              # Launch GUI
blog-create                           # Create new post
blog-list                             # List all posts
```

## GUI Interface Features

- **Sidebar**: Tree view of all blog posts with details
- **Main Content Area**: Previews of recent posts
- **Interactive Menu**: Navigate with numbered options (1-7)
- **Search Integration**: Search and select posts from results
- **Statistics Dashboard**: Visual analytics display
- **Seamless Navigation**: Stay in GUI, exit with Ctrl+C

## File Structure

```
blog-manager/
├── main.py                 # Main CLI application
├── blog_manager.py         # Core business logic
├── models.py              # Data models
├── storage.py             # Storage layer
├── utils.py               # Utility functions
├── blog.sh                # Zsh script wrapper
├── install.sh             # Installation script
├── templates/
│   └── post_template.md   # Post template
└── blog_data/             # Data storage (created automatically)
    ├── posts/             # Individual post files
    │   ├── post-1.json
    │   └── post-2.json
    └── index.json         # Posts index
```

## Requirements

- Python 3.7+
- click library
- rich library
- Zsh (for the enhanced script experience)

## Installation

### For Zsh Users (Recommended)

1. **Clone or download all files to a directory**
2. **Run the installation script:**
   ```bash
   ./install.sh
   ```
3. **Reload your shell:**
   ```bash
   source ~/.zshrc
   ```
4. **Start blogging:**
   ```bash
   blog gui
   ```

### Manual Installation

1. **Install dependencies:**
   ```bash
   pip install click rich
   ```
2. **Make scripts executable:**
   ```bash
   chmod +x blog.sh main.py
   ```
3. **Run the blog manager:**
   ```bash
   ./blog.sh gui
   ```

## Usage Examples

### Creating Your First Post
```bash
blog create
# Follow the prompts to create your post
```

### Viewing All Posts in GUI
```bash
blog gui
# Use the interactive menu to navigate
```

### Searching Posts
```bash
blog search "python"
# Shows all posts containing "python"
```

### Exporting Posts
```bash
blog export --format markdown --output-dir ./my-blog
# Exports all posts as markdown files
```

## Customization

### Zsh Configuration
The installation script adds these aliases to your `~/.zshrc`:
```bash
alias blog='~/.local/bin/blog'
alias blog-gui='~/.local/bin/blog gui'
alias blog-create='~/.local/bin/blog create'
alias blog-list='~/.local/bin/blog list'
```

### Color Themes
The GUI automatically adapts to your terminal's color scheme and capabilities.

## Data Storage

- **Location**: `./blog_data/` directory
- **Format**: JSON files for easy backup and portability
- **Structure**: Individual files per post + index file
- **Backup**: Simply copy the `blog_data` directory

## Cross-Platform Compatibility

- **Linux**: Full support with all features
- **macOS**: Full support with all features
- **Windows**: Works with Command Prompt, PowerShell, Git Bash
- **SSH/Remote**: Perfect for managing blogs on remote servers

## Troubleshooting

### Dependencies Not Found
```bash
pip install --user click rich
```

### Permission Denied
```bash
chmod +x blog.sh install.sh
```

### Python Not Found
Make sure Python 3.7+ is installed and in your PATH.

### Zsh Not Default Shell
Switch to Zsh or use the Python commands directly.

## Contributing

This is a personal blog management tool. Feel free to modify and customize it for your needs.

## License

Open source - modify and use as needed.