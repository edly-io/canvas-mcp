# Canvas MCP

A Model Context Protocol (MCP) server for interacting with Canvas LMS.

## Features

- Create and manage course sections and subsections
- Interact with Canvas LMS via official REST API
- Easy to use MCP tools for course structure management

## Installation

### Prerequisites

Make sure you have the MCP CLI installed:

```bash
pip install "mcp[cli]"
```

### Install Canvas MCP

```bash
# Install from source
pip install -e .

# Or install from PyPI when published
# pip install canvas-mcp
```

## Usage

You can run the Canvas MCP server in two ways:

### Using the package CLI

```bash
# Run in development mode
mcp dev src/canvas_mcp/server.py

# Install the MCP server in Claude Desktop
mcp install --env-file=.env --with-editable=. src/canvas_mcp/server.py
```

### Using the MCP CLI directly

```bash
# Run in development mode
mcp dev src/canvas_mcp/server.py

# Install the MCP server in Claude Desktop
mcp install src/canvas_mcp/server.py
```

## Configuration

You will need to provide your Canvas API credentials. You can do this in two ways:

### Option 1: Environment Variables

```bash
export CANVAS_API_URL=https://your-canvas-instance.instructure.com/api/v1
export CANVAS_API_TOKEN=your_api_token
```

### Option 2: .env File (Recommended)

Create a `.env` file in the project root, your home directory, or the current working directory:

```
CANVAS_API_URL=https://your-canvas-instance.instructure.com/api/v1
CANVAS_API_TOKEN=your_api_token
```

A template file `sample.env` is provided - you can copy it to `.env` and update the values:

```bash
cp sample.env .env
# Then edit .env with your credentials
```

## MCP Tools

The following MCP tools are available:

### Course Management
- `get_courses` - Get a list of all courses
- `get_course` - Get a specific course by ID
- `create_course` - Create a new course

### Section Management
- `create_section` - Create a new section in a course
- `list_sections` - List all sections in a course
- `update_section` - Update a section's details
- `delete_section` - Delete a section
- `cross_list_section` - Move a section to a different course

### Module Management
- `list_modules` - Get all modules in a course
- `get_module` - Get a specific module by ID
- `create_module` - Create a new module in a course
- `update_module` - Update a module's details
- `delete_module` - Delete a module from a course

### Module Item Management
- `list_module_items` - Get all items in a module
- `get_module_item` - Get a specific module item by ID
- `create_module_item` - Create a new item in a module
- `update_module_item` - Update a module item's details
- `delete_module_item` - Delete an item from a module

### Page Management
- `list_pages` - List all pages in a course
- `get_page` - Get a specific page by URL
- `create_page` - Create a new page in a course
- `update_page` - Update a page's details
- `delete_page` - Delete a page from a course
- `add_page_to_module` - Add an existing page to a module
- `create_page_and_add_to_module` - Create a new page and add it to a module in one operation

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT
