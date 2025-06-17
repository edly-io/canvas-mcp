"""Tests for the Canvas client."""

import unittest
import requests
from unittest.mock import patch, MagicMock

from canvas_mcp.client import CanvasClient, CanvasAPIError


class TestCanvasClient(unittest.TestCase):
    """Test Canvas client functionality."""
    
    def setUp(self):
        """Set up test client."""
        self.client = CanvasClient(
            api_url="https://example.instructure.com/api/v1",
            api_token="test_token",
        )
    
    def test_init(self):
        """Test client initialization."""
        self.assertEqual(self.client.api_url, "https://example.instructure.com/api/v1")
        self.assertEqual(self.client.api_token, "test_token")
        self.assertEqual(
            self.client.session.headers["Authorization"],
            "Bearer test_token",
        )
    
    @patch("requests.Session.get")
    def test_get_courses(self, mock_get):
        """Test getting courses."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1, "name": "Test Course"}]
        mock_response.content = True
        mock_get.return_value = mock_response
        
        # Call method
        courses = self.client.get_courses()
        
        # Assertions
        mock_get.assert_called_once_with(
            "https://example.instructure.com/api/v1/courses",
            params=None,
        )
        self.assertEqual(courses, [{"id": 1, "name": "Test Course"}])
    
    @patch("requests.Session.post")
    def test_create_section(self, mock_post):
        """Test creating a section."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "name": "Test Section"}
        mock_response.content = True
        mock_post.return_value = mock_response
        
        # Call method
        section = self.client.create_section(
            course_id="123",
            section_name="Test Section",
        )
        
        # Assertions
        mock_post.assert_called_once_with(
            "https://example.instructure.com/api/v1/courses/123/sections",
            params=None,
            json={"course_section[name]": "Test Section"},
        )
        self.assertEqual(section, {"id": 1, "name": "Test Section"})
    
    @patch("requests.Session.get")
    def test_api_error(self, mock_get):
        """Test handling API errors."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"errors": {"message": "Unauthorized"}}
        
        # Create a requests.exceptions.RequestException with response attribute
        mock_exception = requests.exceptions.RequestException("API Error")
        mock_exception.response = mock_response
        
        # Configure the mock to raise the exception
        mock_get.side_effect = mock_exception
        
        # Call method and check exception
        with self.assertRaises(CanvasAPIError) as context:
            self.client.get_courses()
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.message, "Unauthorized")