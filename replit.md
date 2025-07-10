# Blog Management System

## Overview

This is a command-line blog management system built in Python that allows users to create, edit, and manage blog posts through a terminal interface. The system uses JSON files for data storage and provides a rich CLI experience with the Rich library.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a layered architecture pattern with clear separation of concerns:

1. **Presentation Layer**: CLI interface using Click and Rich for user interaction
2. **Business Logic Layer**: Core blog management functionality
3. **Data Access Layer**: JSON-based storage system
4. **Models Layer**: Data structures and serialization logic

## Key Components

### CLI Interface (`main.py`)
- **Purpose**: Provides the command-line interface for user interaction
- **Technology**: Click framework for command parsing, Rich library for enhanced terminal output
- **Features**: Interactive prompts, formatted tables, colorized output

### Blog Manager (`blog_manager.py`)
- **Purpose**: Core business logic for managing blog posts
- **Responsibilities**: 
  - Post creation with unique ID generation
  - Post retrieval and updates
  - Data directory management
- **Design Pattern**: Facade pattern to simplify complex operations

### Storage Layer (`storage.py`)
- **Purpose**: Handles data persistence using JSON files
- **Storage Strategy**: 
  - Individual JSON files per blog post
  - Index file for metadata and quick lookups
  - File-based storage in `blog_data/posts/` directory
- **Rationale**: Chosen for simplicity and human-readable format, no database dependencies

### Data Models (`models.py`)
- **Purpose**: Defines the BlogPost data structure
- **Implementation**: Python dataclasses with JSON serialization
- **Features**: 
  - Automatic timestamp generation
  - Bi-directional JSON conversion
  - Type safety with dataclasses

### Utilities (`utils.py`)
- **Purpose**: Common helper functions
- **Functions**:
  - URL-friendly ID generation from titles
  - Tag validation and cleaning
  - Filename sanitization

## Data Flow

1. **Post Creation**: User input → CLI validation → BlogManager → Storage → JSON file
2. **Post Retrieval**: Post ID → Storage → JSON file → BlogPost model → CLI display
3. **Post Updates**: Existing post → Modifications → Storage → Updated JSON file

## External Dependencies

- **Click**: Command-line interface framework
- **Rich**: Terminal formatting and enhanced output
- **Python Standard Library**: JSON, datetime, os, re, collections

## Deployment Strategy

The application is designed as a standalone Python CLI tool:

1. **No Database Required**: Uses JSON file storage for simplicity
2. **Portable**: Can run on any system with Python 3.7+
3. **Self-contained**: All dependencies are common Python packages
4. **Data Directory**: Creates and manages `blog_data/` directory automatically

### Storage Structure
```
blog_data/
├── posts/
│   ├── post-id-1.json
│   ├── post-id-2.json
│   └── ...
└── index.json
```

The system prioritizes simplicity and ease of use over complex features, making it ideal for personal blog management or small-scale content creation workflows.