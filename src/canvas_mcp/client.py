"""Canvas API client."""

import json
from typing import Dict, List, Optional, Any, Union

import requests


class CanvasAPIError(Exception):
    """Exception raised for Canvas API errors."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Canvas API Error ({status_code}): {message}")


class CanvasClient:
    """Client for interacting with the Canvas LMS API."""

    def __init__(self, api_url: str, api_token: str):
        """
        Initialize the Canvas client.

        Args:
            api_url: The Canvas API URL (e.g., https://canvas.instructure.com/api/v1)
            api_token: The Canvas API token
        """
        self.api_url = api_url.rstrip("/")
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_token}"})

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a request to the Canvas API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            data: Request body data

        Returns:
            Response data

        Raises:
            CanvasAPIError: If the API returns an error
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"

        # TODO debugging
        import sys
        sys.stderr.write(f"Canvas API request: url={url} method={method} params={params} data={data} header={self.session.headers}\n")

        try:
            if method == "GET":
                response = self.session.get(url, params=params)
            elif method == "POST":
                response = self.session.post(url, params=params, data=data)
            elif method == "PUT":
                response = self.session.put(url, params=params, data=data)
            elif method == "DELETE":
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            if response.content:
                return response.json()
            return {}

        except requests.exceptions.RequestException as e:
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    # Handle different error formats from Canvas API
                    if isinstance(error_data.get("errors"), dict):
                        error_message = error_data["errors"].get("message", str(e))
                    elif isinstance(error_data.get("errors"), list) and error_data["errors"]:
                        error_message = error_data["errors"][0]
                    else:
                        error_message = error_data.get("message", str(e))
                except (ValueError, json.JSONDecodeError):
                    error_message = str(e)

                raise CanvasAPIError(e.response.status_code, error_message)
            raise CanvasAPIError(500, str(e))

    # Course methods
    def get_courses(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all courses."""
        return self._request("GET", "courses", params=params)  # type: ignore

    def get_course(self, course_id: str) -> Dict[str, Any]:
        """Get a specific course by ID."""
        return self._request("GET", f"courses/{course_id}")  # type: ignore

    def create_course(
        self,
        account_id: str,
        name: str,
        course_code: Optional[str] = None,
        sis_course_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new course."""
        data: Dict[str, Any] = {
            "course[name]": name,
        }

        if course_code:
            data["course[course_code]"] = course_code

        if sis_course_id:
            data["course[sis_course_id]"] = sis_course_id

        return self._request("POST", f"accounts/{account_id}/courses", data=data)  # type: ignore

    # Section methods
    def list_sections(self, course_id: str) -> List[Dict[str, Any]]:
        """List all sections in a course."""
        return self._request("GET", f"courses/{course_id}/sections")  # type: ignore

    def create_section(
        self,
        course_id: str,
        section_name: str,
        sis_section_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new section in a course."""
        data: Dict[str, Any] = {
            "course_section[name]": section_name,
        }

        if sis_section_id:
            data["course_section[sis_section_id]"] = sis_section_id

        return self._request("POST", f"courses/{course_id}/sections", data=data)  # type: ignore

    def get_section(self, section_id: str) -> Dict[str, Any]:
        """Get a specific section by ID."""
        return self._request("GET", f"sections/{section_id}")  # type: ignore

    def update_section(
        self,
        section_id: str,
        section_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a section."""
        data: Dict[str, Any] = {}

        if section_name:
            data["course_section[name]"] = section_name

        return self._request("PUT", f"sections/{section_id}", data=data)  # type: ignore

    def delete_section(self, section_id: str) -> Dict[str, Any]:
        """Delete a section."""
        return self._request("DELETE", f"sections/{section_id}")  # type: ignore

    def cross_list_section(self, section_id: str, new_course_id: str) -> Dict[str, Any]:
        """Move a section to a different course."""
        return self._request("POST", f"sections/{section_id}/crosslist/{new_course_id}")  # type: ignore

    # Module methods
    def list_modules(self, course_id: str) -> List[Dict[str, Any]]:
        """
        List all modules in a course.

        Args:
            course_id: The Canvas course ID

        Returns:
            List of modules in the course
        """
        return self._request("GET", f"courses/{course_id}/modules")  # type: ignore

    def get_module(self, course_id: str, module_id: str) -> Dict[str, Any]:
        """
        Get a specific module by ID.

        Args:
            course_id: The Canvas course ID
            module_id: The Canvas module ID

        Returns:
            Module details
        """
        return self._request("GET", f"courses/{course_id}/modules/{module_id}")  # type: ignore

    def create_module(
        self,
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
            unlock_at: Optional date the module will unlock
            require_sequential_progress: Whether students must progress through the module sequentially
            prerequisite_module_ids: Optional list of module IDs that must be completed first
            publish_final_grade: Whether to publish the final grade for the module

        Returns:
            The created module details
        """
        data: Dict[str, Any] = {
            "module[name]": name,
        }

        if position is not None:
            data["module[position]"] = position

        if unlock_at is not None:
            data["module[unlock_at]"] = unlock_at

        if require_sequential_progress is not None:
            data["module[require_sequential_progress]"] = require_sequential_progress

        if prerequisite_module_ids:
            for i, module_id in enumerate(prerequisite_module_ids):
                data[f"module[prerequisite_module_ids][{i}]"] = module_id

        if publish_final_grade is not None:
            data["module[publish_final_grade]"] = publish_final_grade

        return self._request("POST", f"courses/{course_id}/modules", data=data)  # type: ignore

    def update_module(
        self,
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
            unlock_at: Optional new unlock date
            require_sequential_progress: Whether students must progress through the module sequentially
            prerequisite_module_ids: Optional list of module IDs that must be completed first
            publish_final_grade: Whether to publish the final grade for the module

        Returns:
            The updated module details
        """
        data: Dict[str, Any] = {}

        if name is not None:
            data["module[name]"] = name

        if position is not None:
            data["module[position]"] = position

        if unlock_at is not None:
            data["module[unlock_at]"] = unlock_at

        if require_sequential_progress is not None:
            data["module[require_sequential_progress]"] = require_sequential_progress

        if prerequisite_module_ids is not None:
            if not prerequisite_module_ids:
                data["module[prerequisite_module_ids][]"] = ""
            else:
                for i, module_id in enumerate(prerequisite_module_ids):
                    data[f"module[prerequisite_module_ids][{i}]"] = module_id

        if publish_final_grade is not None:
            data["module[publish_final_grade]"] = publish_final_grade

        return self._request("PUT", f"courses/{course_id}/modules/{module_id}", data=data)  # type: ignore

    def delete_module(self, course_id: str, module_id: str) -> Dict[str, Any]:
        """
        Delete a module from a course.

        Args:
            course_id: The Canvas course ID
            module_id: The Canvas module ID

        Returns:
            The deleted module details
        """
        return self._request("DELETE", f"courses/{course_id}/modules/{module_id}")  # type: ignore

    # Module item methods
    def list_module_items(self, course_id: str, module_id: str) -> List[Dict[str, Any]]:
        """
        List all items in a module.

        Args:
            course_id: The Canvas course ID
            module_id: The Canvas module ID

        Returns:
            List of items in the module
        """
        return self._request("GET", f"courses/{course_id}/modules/{module_id}/items")  # type: ignore

    def get_module_item(self, course_id: str, module_id: str, item_id: str) -> Dict[str, Any]:
        """
        Get a specific module item by ID.

        Args:
            course_id: The Canvas course ID
            module_id: The Canvas module ID
            item_id: The Canvas module item ID

        Returns:
            Module item details
        """
        return self._request(
            "GET", f"courses/{course_id}/modules/{module_id}/items/{item_id}"
        )  # type: ignore

    def create_module_item(
        self,
        course_id: str,
        module_id: str,
        title: str,
        type: str,
        content_id: str,
        position: Optional[int] = None,
        indent: Optional[int] = None,
        page_url: Optional[str] = None,
        external_url: Optional[str] = None,
        new_tab: Optional[bool] = None,
        completion_requirement: Optional[Dict[str, Any]] = None,
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
            completion_requirement: Optional requirements for item completion

        Returns:
            The created module item details
        """
        data: Dict[str, Any] = {
            "module_item[title]": title,
            "module_item[type]": type,
        }

        if type != "ExternalUrl":
            data["module_item[content_id]"] = content_id

        if position is not None:
            data["module_item[position]"] = position

        if indent is not None:
            data["module_item[indent]"] = indent

        if page_url is not None and type == "Page":
            data["module_item[page_url]"] = page_url

        if external_url is not None and type == "ExternalUrl":
            data["module_item[external_url]"] = external_url

        if new_tab is not None:
            data["module_item[new_tab]"] = new_tab

        if completion_requirement:
            data["module_item[completion_requirement][type]"] = completion_requirement.get(
                "type", ""
            )

            if "min_score" in completion_requirement:
                data["module_item[completion_requirement][min_score]"] = completion_requirement[
                    "min_score"
                ]

        return self._request(
            "POST", f"courses/{course_id}/modules/{module_id}/items", data=data
        )  # type: ignore

    def update_module_item(
        self,
        course_id: str,
        module_id: str,
        item_id: str,
        title: Optional[str] = None,
        position: Optional[int] = None,
        indent: Optional[int] = None,
        external_url: Optional[str] = None,
        new_tab: Optional[bool] = None,
        completion_requirement: Optional[Dict[str, Any]] = None,
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
            completion_requirement: Optional requirements for item completion

        Returns:
            The updated module item details
        """
        data: Dict[str, Any] = {}

        if title is not None:
            data["module_item[title]"] = title

        if position is not None:
            data["module_item[position]"] = position

        if indent is not None:
            data["module_item[indent]"] = indent

        if external_url is not None:
            data["module_item[external_url]"] = external_url

        if new_tab is not None:
            data["module_item[new_tab]"] = new_tab

        if completion_requirement:
            data["module_item[completion_requirement][type]"] = completion_requirement.get(
                "type", ""
            )

            if "min_score" in completion_requirement:
                data["module_item[completion_requirement][min_score]"] = completion_requirement[
                    "min_score"
                ]

        return self._request(
            "PUT", f"courses/{course_id}/modules/{module_id}/items/{item_id}", data=data
        )  # type: ignore

    def delete_module_item(self, course_id: str, module_id: str, item_id: str) -> Dict[str, Any]:
        """
        Delete a module item.

        Args:
            course_id: The Canvas course ID
            module_id: The Canvas module ID
            item_id: The Canvas module item ID

        Returns:
            The deleted module item details
        """
        return self._request(
            "DELETE", f"courses/{course_id}/modules/{module_id}/items/{item_id}"
        )  # type: ignore

    # Page methods
    def list_pages(self, course_id: str, search_term: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all pages in a course.

        Args:
            course_id: The Canvas course ID
            search_term: Optional term to search for in page titles

        Returns:
            List of pages in the course
        """
        params = {}
        if search_term:
            params["search_term"] = search_term

        return self._request("GET", f"courses/{course_id}/pages", params=params)  # type: ignore

    def get_page(self, course_id: str, page_url: str) -> Dict[str, Any]:
        """
        Get a specific page by URL.

        Args:
            course_id: The Canvas course ID
            page_url: The Canvas page URL

        Returns:
            Page details
        """
        return self._request("GET", f"courses/{course_id}/pages/{page_url}")  # type: ignore

    def create_page(
        self,
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
        data: Dict[str, Any] = {
            "wiki_page[title]": title,
            "wiki_page[body]": body,
        }

        if editing_roles is not None:
            data["wiki_page[editing_roles]"] = editing_roles

        if published is not None:
            data["wiki_page[published]"] = published

        if front_page is not None:
            data["wiki_page[front_page]"] = front_page

        return self._request("POST", f"courses/{course_id}/pages", data=data)  # type: ignore

    def update_page(
        self,
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
        data: Dict[str, Any] = {}

        if title is not None:
            data["wiki_page[title]"] = title

        if body is not None:
            data["wiki_page[body]"] = body

        if editing_roles is not None:
            data["wiki_page[editing_roles]"] = editing_roles

        if published is not None:
            data["wiki_page[published]"] = published

        if front_page is not None:
            data["wiki_page[front_page]"] = front_page

        return self._request("PUT", f"courses/{course_id}/pages/{page_url}", data=data)  # type: ignore

    def delete_page(self, course_id: str, page_url: str) -> Dict[str, Any]:
        """
        Delete a page from a course.

        Args:
            course_id: The Canvas course ID
            page_url: The Canvas page URL

        Returns:
            The deleted page details
        """
        return self._request("DELETE", f"courses/{course_id}/pages/{page_url}")  # type: ignore
        
    def add_page_to_module(
        self,
        course_id: str,
        module_id: str,
        page_url: str,
        title: Optional[str] = None,
        position: Optional[int] = None,
        indent: Optional[int] = None,
        new_tab: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Add a page to a module.

        This is a convenience method that combines creating a page and adding it to a module.
        
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
        # First, get the page details to get the page ID
        page = self.get_page(course_id, page_url)
        
        # Then create a module item for the page
        return self.create_module_item(
            course_id=course_id,
            module_id=module_id,
            title=title or page.get("title", ""),
            type="Page",
            content_id=str(page.get("id", "")),
            position=position,
            indent=indent,
            page_url=page_url,
            new_tab=new_tab,
        )
