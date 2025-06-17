"""Example script for creating pages and adding them to modules in Canvas LMS."""

import os
import sys
from typing import Dict, List, Any

# Add the parent directory to path to allow importing canvas_mcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.canvas_mcp.client import CanvasClient, CanvasAPIError


def create_course_pages():
    """Create sample pages and add them to modules in a Canvas course."""
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
            name="Introduction to HTML and CSS",
            course_code="WEB101",
        )
        course_id = course["id"]
        print(f"Course created with ID: {course_id}")
        
        # Create modules
        print("\nCreating course modules...")
        
        # Module 1: HTML Basics
        html_module = client.create_module(
            course_id=course_id,
            name="Module 1: HTML Basics",
            position=1,
        )
        print(f"Created module: {html_module['name']} (ID: {html_module['id']})")
        
        # Module 2: CSS Fundamentals
        css_module = client.create_module(
            course_id=course_id,
            name="Module 2: CSS Fundamentals",
            position=2,
        )
        print(f"Created module: {css_module['name']} (ID: {css_module['id']})")
        
        # Create a standalone page
        print("\nCreating a standalone course page...")
        welcome_page = client.create_page(
            course_id=course_id,
            title="Welcome to Web Development",
            body="""
            <h1>Welcome to Web Development!</h1>
            <p>In this course, you will learn the fundamentals of HTML and CSS.</p>
            <ul>
                <li>How to structure web content with HTML</li>
                <li>How to style web pages with CSS</li>
                <li>Best practices for web development</li>
            </ul>
            """,
            published=True,
            front_page=True,  # Set as the course home page
        )
        print(f"Created welcome page: {welcome_page['title']}")
        
        # Create pages and add them to the HTML module
        print("\nCreating pages for HTML module...")
        
        # Page 1: HTML Introduction
        html_intro_page = client.create_page(
            course_id=course_id,
            title="Introduction to HTML",
            body="""
            <h1>Introduction to HTML</h1>
            <p>HTML (HyperText Markup Language) is the standard markup language for creating web pages.</p>
            <h2>What is HTML?</h2>
            <p>HTML consists of a series of elements that tell the browser how to display content.</p>
            <h2>Basic Structure</h2>
            <pre><code>
            &lt;!DOCTYPE html&gt;
            &lt;html&gt;
              &lt;head&gt;
                &lt;title&gt;Page Title&lt;/title&gt;
              &lt;/head&gt;
              &lt;body&gt;
                &lt;h1&gt;My First Heading&lt;/h1&gt;
                &lt;p&gt;My first paragraph.&lt;/p&gt;
              &lt;/body&gt;
            &lt;/html&gt;
            </code></pre>
            """,
            published=True,
        )
        
        # Add the HTML introduction page to the HTML module
        html_intro_item = client.add_page_to_module(
            course_id=course_id,
            module_id=html_module["id"],
            page_url=html_intro_page["url"].split("/")[-1],
            position=1,
        )
        print(f"Added page to module: {html_intro_item['title']}")
        
        # Create a page and add it to the HTML module in one operation
        print("\nCreating and adding HTML Elements page to module...")
        html_elements_item = client.create_module_item(
            course_id=course_id,
            module_id=html_module["id"],
            title="HTML Elements",
            type="Page",
            content_id="1",  # Will be ignored for new pages
            position=2,
            page_url="html-elements",  # This will be the URL for the new page
        )
        
        # Now create the actual page with the matching URL
        html_elements_page = client.create_page(
            course_id=course_id,
            title="HTML Elements",
            body="""
            <h1>HTML Elements</h1>
            <p>HTML elements are the building blocks of HTML pages.</p>
            <h2>Common HTML Elements</h2>
            <ul>
                <li><strong>&lt;h1&gt; to &lt;h6&gt;</strong> - Headings</li>
                <li><strong>&lt;p&gt;</strong> - Paragraph</li>
                <li><strong>&lt;a&gt;</strong> - Link</li>
                <li><strong>&lt;img&gt;</strong> - Image</li>
                <li><strong>&lt;ul&gt; and &lt;ol&gt;</strong> - Lists</li>
                <li><strong>&lt;div&gt;</strong> - Division</li>
                <li><strong>&lt;span&gt;</strong> - Inline container</li>
            </ul>
            """,
            published=True,
        )
        print(f"Created and added HTML Elements page to module")
        
        # Create and add a page to the CSS module in one step using our helper method
        print("\nCreating and adding CSS Introduction page to module...")
        css_intro = client.add_page_to_module(
            course_id=course_id,
            module_id=css_module["id"],
            page_url="introduction-to-css",  # This must match the actual page URL
            position=1,
        )
        
        # Now create the actual page with the matching URL
        css_intro_page = client.create_page(
            course_id=course_id,
            title="Introduction to CSS",
            body="""
            <h1>Introduction to CSS</h1>
            <p>CSS (Cascading Style Sheets) is used to style HTML elements.</p>
            <h2>What is CSS?</h2>
            <p>CSS describes how HTML elements should be displayed on screen.</p>
            <h2>CSS Syntax</h2>
            <pre><code>
            selector {
              property: value;
              property: value;
            }
            </code></pre>
            """,
            published=True,
        )
        print(f"Created and added CSS Introduction page to module")
        
        # List all pages in the course
        print("\nAll pages in the course:")
        all_pages = client.list_pages(course_id)
        for page in all_pages:
            print(f"- {page['title']} (URL: {page['url']})")
        
        print("\nCourse with pages and modules created successfully!")
        
    except CanvasAPIError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_course_pages()