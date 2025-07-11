#!/bin/zsh

# Blog Manager Installation Script for Zsh
# This script helps you set up the blog manager in your Zsh environment

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Installation directory
INSTALL_DIR="$HOME/.blog-manager"
BIN_DIR="$HOME/.local/bin"

print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                Blog Manager Installation                     ║"
    echo "║              Terminal-based Blog Management                  ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

check_zsh() {
    if [[ ! "$SHELL" =~ "zsh" ]]; then
        print_warning "You're not currently using Zsh shell"
        print_warning "Current shell: $SHELL"
        read -q "?Continue with installation anyway? [y/N] "
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

install_blog_manager() {
    print_step "Creating installation directory..."
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    
    print_step "Copying blog manager files..."
    cp -r ./* "$INSTALL_DIR/"
    
    print_step "Making scripts executable..."
    chmod +x "$INSTALL_DIR/blog.sh"
    chmod +x "$INSTALL_DIR/main.py"
    
    print_step "Creating symbolic link..."
    ln -sf "$INSTALL_DIR/blog.sh" "$BIN_DIR/blog"
    
    print_success "Blog manager installed to $INSTALL_DIR"
}

setup_zsh_alias() {
    local zshrc="$HOME/.zshrc"
    
    print_step "Setting up Zsh aliases..."
    
    # Check if alias already exists
    if grep -q "alias blog=" "$zshrc" 2>/dev/null; then
        print_warning "Blog alias already exists in $zshrc"
    else
        echo "" >> "$zshrc"
        echo "# Blog Manager aliases" >> "$zshrc"
        echo "alias blog='$BIN_DIR/blog'" >> "$zshrc"
        echo "alias blog-gui='$BIN_DIR/blog gui'" >> "$zshrc"
        echo "alias blog-create='$BIN_DIR/blog create'" >> "$zshrc"
        echo "alias blog-list='$BIN_DIR/blog list'" >> "$zshrc"
        print_success "Added blog aliases to $zshrc"
    fi
}

setup_path() {
    local zshrc="$HOME/.zshrc"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        print_step "Adding $BIN_DIR to PATH..."
        echo "" >> "$zshrc"
        echo "# Add ~/.local/bin to PATH for blog manager" >> "$zshrc"
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$zshrc"
        print_success "Added $BIN_DIR to PATH in $zshrc"
    else
        print_step "$BIN_DIR is already in PATH"
    fi
}

install_dependencies() {
    print_step "Installing Python dependencies..."
    
    if command -v python3 &> /dev/null; then
        python3 -m pip install --user click rich
    elif command -v python &> /dev/null; then
        python -m pip install --user click rich
    else
        print_error "Python is not installed. Please install Python 3.7+ first."
        exit 1
    fi
    
    print_success "Dependencies installed successfully"
}

create_desktop_entry() {
    local desktop_dir="$HOME/.local/share/applications"
    local desktop_file="$desktop_dir/blog-manager.desktop"
    
    print_step "Creating desktop entry..."
    mkdir -p "$desktop_dir"
    
    cat > "$desktop_file" << EOF
[Desktop Entry]
Name=Blog Manager
Comment=Terminal-based Blog Management System
Exec=gnome-terminal -- $BIN_DIR/blog gui
Icon=applications-office
Type=Application
Categories=Office;TextEditor;
Terminal=false
StartupNotify=true
EOF
    
    chmod +x "$desktop_file"
    print_success "Desktop entry created"
}

show_usage() {
    echo -e "${CYAN}Installation complete!${NC}"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo -e "  ${GREEN}blog gui${NC}                    # Launch GUI interface"
    echo -e "  ${GREEN}blog create${NC}                 # Create new post"
    echo -e "  ${GREEN}blog list${NC}                   # List all posts"
    echo -e "  ${GREEN}blog view <post-id>${NC}        # View specific post"
    echo -e "  ${GREEN}blog search <term>${NC}         # Search posts"
    echo ""
    echo -e "${YELLOW}Quick aliases:${NC}"
    echo -e "  ${GREEN}blog-gui${NC}                    # Same as 'blog gui'"
    echo -e "  ${GREEN}blog-create${NC}                 # Same as 'blog create'"
    echo -e "  ${GREEN}blog-list${NC}                   # Same as 'blog list'"
    echo ""
    echo -e "${YELLOW}To get started:${NC}"
    echo -e "  1. Reload your shell: ${CYAN}source ~/.zshrc${NC}"
    echo -e "  2. Run: ${CYAN}blog gui${NC}"
    echo -e "  3. Create your first post: ${CYAN}blog create${NC}"
    echo ""
}

main() {
    print_banner
    
    check_zsh
    
    print_step "Starting Blog Manager installation..."
    
    install_dependencies
    install_blog_manager
    setup_path
    setup_zsh_alias
    create_desktop_entry
    
    show_usage
    
    print_success "Blog Manager installation completed!"
    print_step "Please run 'source ~/.zshrc' to reload your shell configuration"
}

# Run installation
main "$@"