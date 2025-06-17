"""Example script for creating a course structure in Canvas LMS."""

import os
import sys
from typing import Dict, List, Any

# Add the parent directory to path to allow importing canvas_mcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.canvas_mcp.client import CanvasClient, CanvasAPIError


def create_course_structure():
    """Create a sample course structure in Canvas LMS."""
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
            name="Example Course",
            course_code="EX101",
        )
        course_id = course["id"]
        print(f"Course created with ID: {course_id}")
        
        # Create main sections
        print("Creating course sections...")
        sections = []
        for section_name in ["Introduction", "Week 1", "Week 2", "Final Project"]:
            section = client.create_section(
                course_id=course_id,
                section_name=section_name,
            )
            sections.append(section)
            print(f"Created section: {section['name']} (ID: {section['id']})")
        
        # List all sections
        print("\nAll sections in the course:")
        all_sections = client.list_sections(course_id)
        for section in all_sections:
            print(f"- {section['name']} (ID: {section['id']})")
        
        print("\nCourse structure created successfully!")
        
    except CanvasAPIError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_course_structure()