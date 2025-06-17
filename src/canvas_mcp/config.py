"""Configuration module for Canvas MCP."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class CanvasConfig(BaseModel):
    """Canvas LMS configuration."""

    api_url: str = Field(
        default_factory=lambda: os.environ.get("CANVAS_API_URL", ""),
        description="Canvas API URL",
    )
    api_token: str = Field(
        default_factory=lambda: os.environ.get("CANVAS_API_TOKEN", ""),
        description="Canvas API token",
    )

    @property
    def is_configured(self) -> bool:
        """Check if the Canvas client is configured."""
        return bool(self.api_url and self.api_token)


def load_config() -> CanvasConfig:
    """
    Load configuration from environment variables.

    This function looks for a .env file in the following locations:
    1. Current working directory
    2. User's home directory
    3. Directory where the config module is located

    Returns:
        CanvasConfig: Configuration object with Canvas API settings
    """
    # Try to load from potential .env file locations if not already loaded
    env_locations = [
        Path.cwd() / ".env",  # Current directory
        Path.home() / ".env",  # Home directory
        Path(__file__).parent.parent.parent / ".env",  # Project root
    ]

    for env_path in env_locations:
        if env_path.exists():
            load_dotenv(env_path)
            break

    return CanvasConfig()
