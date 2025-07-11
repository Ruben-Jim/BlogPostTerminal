#!/bin/bash

# Blog Manager - Zsh Script
# A convenient wrapper for your terminal-based blog management system

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Function to check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        echo -e "${RED}Error: Python is not installed or not in PATH${NC}"
        echo -e "${YELLOW}Please install Python 3.7+ to use this blog manager${NC}"
        exit 1
    fi
}

# Function to check if dependencies are installed
check_dependencies() {
    local python_cmd
    if command -v python3 &> /dev/null; then
        python_cmd="python3"
    else
        python_cmd="python"
    fi
    
    # Check if click and rich are installed
    if ! $python_cmd -c "import click, rich" &> /dev/null; then
        echo -e "${YELLOW}Installing required dependencies...${NC}"
        $python_cmd -m pip install click rich
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Dependencies installed successfully!${NC}"
        else
            echo -e "${RED}Failed to install dependencies. Please install manually:${NC}"
            echo -e "${CYAN}pip install click rich${NC}"
            exit 1
        fi
    fi
}

# Function to get Python command
get_python_cmd() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    else
        echo "python"
    fi
}

# Function to display help
show_help() {
    echo -e "${CYAN}Blog Manager - Terminal-based Blog Management System${NC}"
    echo -e "${PURPLE}Usage: $0 [command] [options]${NC}"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  ${GREEN}gui${NC}                    Launch interactive GUI interface"
    echo -e "  ${GREEN}create${NC}                 Create a new blog post"
    echo -e "  ${GREEN}list${NC}                   List all blog posts"
    echo -e "  ${GREEN}view <post-id>${NC}        View a specific blog post"
    echo -e "  ${GREEN}search <term>${NC}         Search blog posts"
    echo -e "  ${GREEN}edit <post-id>${NC}        Edit an existing blog post"
    echo -e "  ${GREEN}delete <post-id>${NC}      Delete a blog post"
    echo -e "  ${GREEN}stats${NC}                 Show blog statistics"
    echo -e "  ${GREEN}export${NC}                Export all posts to files"
    echo -e "  ${GREEN}help${NC}                  Show this help message"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo -e "  ${CYAN}$0 gui${NC}                           # Launch GUI interface"
    echo -e "  ${CYAN}$0 create${NC}                        # Create a new post"
    echo -e "  ${CYAN}$0 view my-first-post${NC}            # View specific post"
    echo -e "  ${CYAN}$0 search python${NC}                 # Search for posts about python"
    echo -e "  ${CYAN}$0 export --format markdown${NC}      # Export posts as markdown"
    echo ""
    echo -e "${YELLOW}Quick Start:${NC}"
    echo -e "  1. Run '${GREEN}$0 gui${NC}' to launch the interactive interface"
    echo -e "  2. Use '${GREEN}$0 create${NC}' to add your first blog post"
    echo -e "  3. Press ${RED}Ctrl+C${NC} to exit the GUI anytime"
    echo ""
}

# Function to display banner
show_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    Blog Manager v1.0                        ║"
    echo "║              Terminal-based Blog Management                  ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Main script logic
main() {
    # Change to script directory
    cd "$SCRIPT_DIR"
    
    # Check dependencies
    check_python
    check_dependencies
    
    # Get Python command
    local python_cmd=$(get_python_cmd)
    
    # Handle commands
    case "${1:-gui}" in
        "gui"|"")
            show_banner
            echo -e "${GREEN}Launching Blog Manager GUI...${NC}"
            echo -e "${YELLOW}Press Ctrl+C to exit anytime${NC}"
            echo ""
            $python_cmd main.py gui
            ;;
        "create")
            show_banner
            echo -e "${GREEN}Creating new blog post...${NC}"
            $python_cmd main.py create "${@:2}"
            ;;
        "list")
            $python_cmd main.py list "${@:2}"
            ;;
        "view")
            if [ -z "$2" ]; then
                echo -e "${RED}Error: Post ID required${NC}"
                echo -e "${YELLOW}Usage: $0 view <post-id>${NC}"
                exit 1
            fi
            $python_cmd main.py view "$2"
            ;;
        "search")
            if [ -z "$2" ]; then
                echo -e "${RED}Error: Search term required${NC}"
                echo -e "${YELLOW}Usage: $0 search <term>${NC}"
                exit 1
            fi
            $python_cmd main.py search "$2"
            ;;
        "edit")
            if [ -z "$2" ]; then
                echo -e "${RED}Error: Post ID required${NC}"
                echo -e "${YELLOW}Usage: $0 edit <post-id>${NC}"
                exit 1
            fi
            $python_cmd main.py edit "$2"
            ;;
        "delete")
            if [ -z "$2" ]; then
                echo -e "${RED}Error: Post ID required${NC}"
                echo -e "${YELLOW}Usage: $0 delete <post-id>${NC}"
                exit 1
            fi
            $python_cmd main.py delete "$2"
            ;;
        "stats")
            $python_cmd main.py stats
            ;;
        "export")
            $python_cmd main.py export "${@:2}"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            echo -e "${RED}Error: Unknown command '$1'${NC}"
            echo -e "${YELLOW}Use '$0 help' for available commands${NC}"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"