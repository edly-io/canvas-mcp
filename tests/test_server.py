"""Tests for the Canvas MCP server."""

import unittest
import sys
from unittest.mock import patch, MagicMock

# We need to patch the load_config before importing server
with patch("canvas_mcp.config.load_config") as mock_load_config:
    mock_config = MagicMock()
    mock_config.api_url = "https://example.instructure.com/api/v1"
    mock_config.api_token = "test_token"
    mock_load_config.return_value = mock_config
    
    # Also patch the FastMCP class to avoid actual MCP initialization
    with patch("mcp.server.fastmcp.FastMCP") as mock_fastmcp:
        mock_mcp = MagicMock()
        mock_fastmcp.return_value = mock_mcp
        
        # Resource and tool decorators should return the function unchanged
        mock_mcp.resource.side_effect = lambda uri: lambda f: f
        mock_mcp.tool.side_effect = lambda: lambda f: f
        
        from canvas_mcp.server import (
            mcp,
            create_section,
            list_sections,
            get_courses,
        )


class TestCanvasMCPServer(unittest.TestCase):
    """Test Canvas MCP server functionality."""
    
    @patch("canvas_mcp.client.CanvasClient.create_section")
    def test_create_section_tool(self, mock_create_section):
        """Test the create_section MCP tool."""
        # Setup mock
        mock_create_section.return_value = {"id": 1, "name": "Test Section"}
        
        # Call the MCP tool function
        result = create_section(
            course_id="123",
            section_name="Test Section",
        )
        
        # Assertions
        mock_create_section.assert_called_once_with(
            course_id="123",
            section_name="Test Section",
            sis_section_id=None,
        )
        self.assertEqual(result, {"id": 1, "name": "Test Section"})
    
    @patch("canvas_mcp.client.CanvasClient.list_sections")
    def test_list_sections_tool(self, mock_list_sections):
        """Test the list_sections MCP tool."""
        # Setup mock
        mock_list_sections.return_value = [{"id": 1, "name": "Test Section"}]
        
        # Call the MCP tool function
        result = list_sections(course_id="123")
        
        # Assertions
        mock_list_sections.assert_called_once_with("123")
        self.assertEqual(result, [{"id": 1, "name": "Test Section"}])
    
    @patch("canvas_mcp.client.CanvasClient.get_courses")
    def test_get_courses_resource(self, mock_get_courses):
        """Test the courses MCP resource."""
        # Setup mock
        mock_get_courses.return_value = [{"id": 1, "name": "Test Course"}]
        
        # Call the MCP resource function
        result = get_courses()
        
        # Assertions
        mock_get_courses.assert_called_once()
        self.assertEqual(result, [{"id": 1, "name": "Test Course"}])