"""Example script for creating course modules in Canvas LMS."""

import os
import sys
import time
from typing import Dict, List, Any

# Add the parent directory to path to allow importing canvas_mcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.canvas_mcp.client import CanvasClient, CanvasAPIError


def create_course_modules():
    """Create a sample course with modules and module items in Canvas LMS."""
    # Get API credentials from environment variables
    api_url = os.environ.get("CANVAS_API_URL")
    api_token = os.environ.get("CANVAS_API_TOKEN")
    
    if not api_url or not api_token:
        print("Error: CANVAS_API_URL and CANVAS_API_TOKEN environment variables are required.")
        sys.exit(1)
    
    # Initialize the Canvas client
    client = CanvasClient(api_url=api_url, api_token=api_token)
    
    try:
        # Get the account ID (usually "self" for the current user's account)
        account_id = "self"
        
        # Create a new course
        print("Creating a new course...")
        course = client.create_course(
            account_id=account_id,
            name="Python Programming Course",
            course_code="PY101",
        )
        course_id = course["id"]
        print(f"Course created with ID: {course_id}")
        
        # Create modules
        print("\nCreating course modules...")
        modules = []
        
        # Module 1: Introduction to Python
        intro_module = client.create_module(
            course_id=course_id,
            name="Module 1: Introduction to Python",
            position=1,
        )
        modules.append(intro_module)
        print(f"Created module: {intro_module['name']} (ID: {intro_module['id']})")
        
        # Module 2: Basic Python Syntax
        syntax_module = client.create_module(
            course_id=course_id,
            name="Module 2: Basic Python Syntax",
            position=2,
            require_sequential_progress=True,  # Students must complete items in order
            prerequisite_module_ids=[intro_module["id"]],  # Must complete intro module first
        )
        modules.append(syntax_module)
        print(f"Created module: {syntax_module['name']} (ID: {syntax_module['id']})")
        
        # Module 3: Python Data Structures
        data_module = client.create_module(
            course_id=course_id,
            name="Module 3: Python Data Structures",
            position=3,
            prerequisite_module_ids=[syntax_module["id"]],  # Must complete syntax module first
        )
        modules.append(data_module)
        print(f"Created module: {data_module['name']} (ID: {data_module['id']})")
        
        # Add module items
        print("\nAdding items to modules...")
        
        # Items for Module 1
        intro_items = [
            {
                "title": "What is Python?",
                "type": "Page",
                "page_url": "what-is-python",
            },
            {
                "title": "Setting Up Your Development Environment",
                "type": "Page",
                "page_url": "python-setup",
            },
            {
                "title": "Python Documentation",
                "type": "ExternalUrl",
                "external_url": "https://docs.python.org/3/",
                "new_tab": True,
            },
        ]
        
        for i, item in enumerate(intro_items, 1):
            module_item = client.create_module_item(
                course_id=course_id,
                module_id=intro_module["id"],
                title=item["title"],
                type=item["type"],
                content_id="1",  # Dummy ID for example
                position=i,
                page_url=item.get("page_url"),
                external_url=item.get("external_url"),
                new_tab=item.get("new_tab"),
                completion_requirement={"type": "must_view"} if "page_url" in item else None,
            )
            print(f"Added item: {module_item['title']} to {intro_module['name']}")
        
        # List all modules in the course
        print("\nAll modules in the course:")
        all_modules = client.list_modules(course_id)
        for module in all_modules:
            print(f"- {module['name']} (ID: {module['id']})")
            
            # List items in each module
            items = client.list_module_items(course_id, module["id"])
            for item in items:
                print(f"  * {item['title']} (Type: {item['type']})")
                
        # Note: When using the MCP server, you would use these tool names instead:
        # - list_modules(course_id)
        # - get_module(course_id, module_id)
        # - list_module_items(course_id, module_id)
        # - get_module_item(course_id, module_id, item_id)
        
        print("\nCourse structure with modules created successfully!")
        
    except CanvasAPIError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_course_modules()