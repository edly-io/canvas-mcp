"""Canvas MCP server main module."""

from typing import Dict, List, Optional, Any

from mcp.server.fastmcp import FastMCP

from canvas_mcp.client import CanvasClient
from canvas_mcp.config import load_config

# Initialize MCP server
mcp = FastMCP("CanvasMCP")

# Load configuration
config = load_config()

# Initialize Canvas client
canvas_client = CanvasClient(
    api_url=config.api_url,
    api_token=config.api_token,
)


# MCP tools for Canvas courses
@mcp.tool()
def get_courses() -> List[Dict[str, Any]]:
    """
    Get all available courses.

    Returns:
        List of courses
    """
    return canvas_client.get_courses()


@mcp.tool()
def get_course(course_id: str) -> Dict[str, Any]:
    """
    Get a specific course by ID.

    Args:
        course_id: The Canvas course ID

    Returns:
        Course details
    """
    return canvas_client.get_course(course_id)


# MCP tools for managing course sections
@mcp.tool()
def create_section(
    course_id: str, section_name: str, sis_section_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new section in a course.

    Args:
        course_id: The Canvas course ID
        section_name: The name of the section
        sis_section_id: Optional SIS ID for the section

    Returns:
        The created section details
    """
    return canvas_client.create_section(
        course_id=course_id,
        section_name=section_name,
        sis_section_id=sis_section_id,
    )


@mcp.tool()
def list_sections(course_id: str) -> List[Dict[str, Any]]:
    """
    List all sections in a course.

    Args:
        course_id: The Canvas course ID

    Returns:
        List of sections in the course
    """
    return canvas_client.list_sections(course_id)


@mcp.tool()
def update_section(section_id: str, section_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Update a section.

    Args:
        section_id: The Canvas section ID
        section_name: New name for the section

    Returns:
        The updated section details
    """
    return canvas_client.update_section(section_id, section_name)


@mcp.tool()
def delete_section(section_id: str) -> Dict[str, Any]:
    """
    Delete a section.

    Args:
        section_id: The Canvas section ID

    Returns:
        The deleted section details
    """
    return canvas_client.delete_section(section_id)


@mcp.tool()
def cross_list_section(section_id: str, new_course_id: str) -> Dict[str, Any]:
    """
    Move a section to a different course.

    Args:
        section_id: The Canvas section ID
        new_course_id: The destination course ID

    Returns:
        The updated section details
    """
    return canvas_client.cross_list_section(section_id, new_course_id)


# Course creation tool
@mcp.tool()
def create_course(
    account_id: str,
    name: str,
    course_code: Optional[str] = None,
    sis_course_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new course.

    Args:
        account_id: The Canvas account ID
        name: The name of the course
        course_code: Optional course code
        sis_course_id: Optional SIS ID for the course

    Returns:
        The created course details
    """
    return canvas_client.create_course(
        account_id=account_id,
        name=name,
        course_code=course_code,
        sis_course_id=sis_course_id,
    )


# Additional module management tools
@mcp.tool()
def list_modules(course_id: str) -> List[Dict[str, Any]]:
    """
    Get all modules in a course.

    Args:
        course_id: The Canvas course ID

    Returns:
        List of modules in the course
    """
    return canvas_client.list_modules(course_id)


@mcp.tool()
def get_module(course_id: str, module_id: str) -> Dict[str, Any]:
    """
    Get a specific module by ID.

    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID

    Returns:
        Module details
    """
    return canvas_client.get_module(course_id, module_id)


@mcp.tool()
def list_module_items(course_id: str, module_id: str) -> List[Dict[str, Any]]:
    """
    Get all items in a module.

    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID

    Returns:
        List of items in the module
    """
    return canvas_client.list_module_items(course_id, module_id)


@mcp.tool()
def get_module_item(course_id: str, module_id: str, item_id: str) -> Dict[str, Any]:
    """
    Get a specific module item by ID.

    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID
        item_id: The Canvas module item ID

    Returns:
        Module item details
    """
    return canvas_client.get_module_item(course_id, module_id, item_id)


# Module management tools
@mcp.tool()
def create_module(
    course_id: str,
    name: str,
    position: Optional[int] = None,
    unlock_at: Optional[str] = None,
    require_sequential_progress: Optional[bool] = None,
    prerequisite_module_ids: Optional[List[str]] = None,
    publish_final_grade: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Create a new module in a course.

    Args:
        course_id: The Canvas course ID
        name: The name of the module
        position: Optional position of the module in the course
        unlock_at: Optional date the module will unlock (ISO 8601 format)
        require_sequential_progress: Whether students must progress through the module sequentially
        prerequisite_module_ids: Optional list of module IDs that must be completed first
        publish_final_grade: Whether to publish the final grade for the module

    Returns:
        The created module details
    """
    return canvas_client.create_module(
        course_id=course_id,
        name=name,
        position=position,
        unlock_at=unlock_at,
        require_sequential_progress=require_sequential_progress,
        prerequisite_module_ids=prerequisite_module_ids,
        publish_final_grade=publish_final_grade,
    )


@mcp.tool()
def update_module(
    course_id: str,
    module_id: str,
    name: Optional[str] = None,
    position: Optional[int] = None,
    unlock_at: Optional[str] = None,
    require_sequential_progress: Optional[bool] = None,
    prerequisite_module_ids: Optional[List[str]] = None,
    publish_final_grade: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Update a module in a course.

    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID
        name: Optional new name for the module
        position: Optional new position
        unlock_at: Optional new unlock date (ISO 8601 format)
        require_sequential_progress: Whether students must progress through the module sequentially
        prerequisite_module_ids: Optional list of module IDs that must be completed first
        publish_final_grade: Whether to publish the final grade for the module

    Returns:
        The updated module details
    """
    return canvas_client.update_module(
        course_id=course_id,
        module_id=module_id,
        name=name,
        position=position,
        unlock_at=unlock_at,
        require_sequential_progress=require_sequential_progress,
        prerequisite_module_ids=prerequisite_module_ids,
        publish_final_grade=publish_final_grade,
    )


@mcp.tool()
def delete_module(
    course_id: str,
    module_id: str,
) -> Dict[str, Any]:
    """
    Delete a module from a course.

    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID

    Returns:
        The deleted module details
    """
    return canvas_client.delete_module(course_id, module_id)


# Module item management tools
@mcp.tool()
def create_module_item(
    course_id: str,
    module_id: str,
    title: str,
    type: str,
    content_id: Optional[str] = None,
    position: Optional[int] = None,
    indent: Optional[int] = None,
    page_url: Optional[str] = None,
    external_url: Optional[str] = None,
    new_tab: Optional[bool] = None,
    completion_requirement_type: Optional[str] = None,
    min_score: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Create a new item in a module.

    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID
        title: The title of the item
        type: The type of item (File, Page, Assignment, Discussion, Quiz, ExternalUrl, etc.)
        content_id: The ID of the content (required except for ExternalUrl or Page)
        position: Optional position of the item in the module
        indent: Optional indentation level
        page_url: Optional URL for Page type items
        external_url: Optional URL for ExternalUrl type items
        new_tab: Whether the item should open in a new tab
        completion_requirement_type: Optional completion requirement type
                                    (must_view, must_submit, must_contribute, min_score)
        min_score: Optional minimum score required (used with min_score requirement type)

    Returns:
        The created module item details
    """
    completion_requirement = None
    if completion_requirement_type:
        completion_requirement = {"type": completion_requirement_type}
        if completion_requirement_type == "min_score" and min_score is not None:
            completion_requirement["min_score"] = min_score

    return canvas_client.create_module_item(
        course_id=course_id,
        module_id=module_id,
        title=title,
        type=type,
        content_id=content_id or "",
        position=position,
        indent=indent,
        page_url=page_url,
        external_url=external_url,
        new_tab=new_tab,
        completion_requirement=completion_requirement,
    )


@mcp.tool()
def update_module_item(
    course_id: str,
    module_id: str,
    item_id: str,
    title: Optional[str] = None,
    position: Optional[int] = None,
    indent: Optional[int] = None,
    external_url: Optional[str] = None,
    new_tab: Optional[bool] = None,
    completion_requirement_type: Optional[str] = None,
    min_score: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Update a module item.

    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID
        item_id: The Canvas module item ID
        title: Optional new title for the item
        position: Optional new position
        indent: Optional new indentation level
        external_url: Optional new URL for ExternalUrl type items
        new_tab: Whether the item should open in a new tab
        completion_requirement_type: Optional completion requirement type
                                    (must_view, must_submit, must_contribute, min_score)
        min_score: Optional minimum score required (used with min_score requirement type)

    Returns:
        The updated module item details
    """
    completion_requirement = None
    if completion_requirement_type:
        completion_requirement = {"type": completion_requirement_type}
        if completion_requirement_type == "min_score" and min_score is not None:
            completion_requirement["min_score"] = min_score

    return canvas_client.update_module_item(
        course_id=course_id,
        module_id=module_id,
        item_id=item_id,
        title=title,
        position=position,
        indent=indent,
        external_url=external_url,
        new_tab=new_tab,
        completion_requirement=completion_requirement,
    )


@mcp.tool()
def delete_module_item(
    course_id: str,
    module_id: str,
    item_id: str,
) -> Dict[str, Any]:
    """
    Delete a module item.

    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID
        item_id: The Canvas module item ID

    Returns:
        The deleted module item details
    """
    return canvas_client.delete_module_item(course_id, module_id, item_id)


# Page management tools
@mcp.tool()
def list_pages(course_id: str, search_term: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all pages in a course.
    
    Args:
        course_id: The Canvas course ID
        search_term: Optional term to search for in page titles
        
    Returns:
        List of pages in the course
    """
    return canvas_client.list_pages(course_id, search_term)


@mcp.tool()
def get_page(course_id: str, page_url: str) -> Dict[str, Any]:
    """
    Get a specific page by URL.
    
    Args:
        course_id: The Canvas course ID
        page_url: The Canvas page URL
        
    Returns:
        Page details
    """
    return canvas_client.get_page(course_id, page_url)


@mcp.tool()
def create_page(
    course_id: str,
    title: str,
    body: str,
    editing_roles: Optional[str] = None,
    published: Optional[bool] = None,
    front_page: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Create a new page in a course.
    
    Args:
        course_id: The Canvas course ID
        title: The title of the page
        body: The content of the page in HTML format
        editing_roles: Optional comma-separated list of roles allowed to edit
                       (e.g., "teachers,students,public")
        published: Whether the page is published
        front_page: Whether this page is the front page
        
    Returns:
        The created page details
    """
    return canvas_client.create_page(
        course_id=course_id,
        title=title,
        body=body,
        editing_roles=editing_roles,
        published=published,
        front_page=front_page,
    )


@mcp.tool()
def update_page(
    course_id: str,
    page_url: str,
    title: Optional[str] = None,
    body: Optional[str] = None,
    editing_roles: Optional[str] = None,
    published: Optional[bool] = None,
    front_page: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Update a page in a course.
    
    Args:
        course_id: The Canvas course ID
        page_url: The Canvas page URL
        title: Optional new title for the page
        body: Optional new content for the page in HTML format
        editing_roles: Optional comma-separated list of roles allowed to edit
        published: Whether the page is published
        front_page: Whether this page is the front page
        
    Returns:
        The updated page details
    """
    return canvas_client.update_page(
        course_id=course_id,
        page_url=page_url,
        title=title,
        body=body,
        editing_roles=editing_roles,
        published=published,
        front_page=front_page,
    )


@mcp.tool()
def delete_page(course_id: str, page_url: str) -> Dict[str, Any]:
    """
    Delete a page from a course.
    
    Args:
        course_id: The Canvas course ID
        page_url: The Canvas page URL
        
    Returns:
        The deleted page details
    """
    return canvas_client.delete_page(course_id, page_url)


@mcp.tool()
def add_page_to_module(
    course_id: str,
    module_id: str,
    page_url: str,
    title: Optional[str] = None,
    position: Optional[int] = None,
    indent: Optional[int] = None,
    new_tab: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Add an existing page to a module.
    
    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID
        page_url: The Canvas page URL
        title: Optional title for the module item (defaults to page title)
        position: Optional position in the module
        indent: Optional indentation level
        new_tab: Whether the page should open in a new tab
        
    Returns:
        The created module item details
    """
    return canvas_client.add_page_to_module(
        course_id=course_id,
        module_id=module_id,
        page_url=page_url,
        title=title,
        position=position,
        indent=indent,
        new_tab=new_tab,
    )


@mcp.tool()
def create_page_and_add_to_module(
    course_id: str,
    module_id: str,
    title: str,
    body: str,
    editing_roles: Optional[str] = None,
    published: Optional[bool] = True,
    front_page: Optional[bool] = None,
    module_item_position: Optional[int] = None,
    module_item_indent: Optional[int] = None,
    new_tab: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Create a new page and add it to a module in one operation.
    
    Args:
        course_id: The Canvas course ID
        module_id: The Canvas module ID
        title: The title of the page
        body: The content of the page in HTML format
        editing_roles: Optional comma-separated list of roles allowed to edit
        published: Whether the page is published (defaults to True)
        front_page: Whether this page is the front page
        module_item_position: Optional position in the module
        module_item_indent: Optional indentation level
        new_tab: Whether the page should open in a new tab
        
    Returns:
        The created module item details
    """
    # First create the page
    page = canvas_client.create_page(
        course_id=course_id,
        title=title,
        body=body,
        editing_roles=editing_roles,
        published=published,
        front_page=front_page,
    )
    
    # Then add it to the module
    # The URL is typically the title with spaces replaced by hyphens and lowercased
    page_url = page.get("url", "").split("/")[-1]
    
    return canvas_client.add_page_to_module(
        course_id=course_id,
        module_id=module_id,
        page_url=page_url,
        title=title,
        position=module_item_position,
        indent=module_item_indent,
        new_tab=new_tab,
    )
