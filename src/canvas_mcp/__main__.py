"""Command-line interface for the Canvas MCP server."""

import argparse
import logging
import sys
import subprocess
from pathlib import Path

# Import server and config
from canvas_mcp.config import load_config


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    """Run the Canvas MCP server."""
    parser = argparse.ArgumentParser(description="Canvas MCP Server")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--mode",
        choices=["dev", "install"],
        default="dev",
        help="Server mode: 'dev' for development, 'install' for installation",
    )
    args = parser.parse_args()

    setup_logging(args.verbose)

    # Check configuration
    config = load_config()
    if not config.is_configured:
        logging.error(
            "Canvas API URL and token are required. Please set CANVAS_API_URL and "
            "CANVAS_API_TOKEN environment variables or create a .env file with these values."
        )
        logging.info(
            "You can create a .env file in the current directory, your home directory, "
            "or the project root with the following content:\n"
            "CANVAS_API_URL=https://your-canvas-instance.instructure.com/api/v1\n"
            "CANVAS_API_TOKEN=your_api_token"
        )
        sys.exit(1)

    # Get server module path
    server_file = Path(__file__).parent / "server.py"
    server_path = str(server_file.resolve())

    # Start the server using the mcp CLI
    logging.info("Starting Canvas MCP server using %s", server_path)

    try:
        if args.mode == "dev":
            subprocess.run(["mcp", "dev", server_path], check=True)
        else:
            subprocess.run(["mcp", "install", server_path], check=True)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to start MCP server: %s", e)
        sys.exit(1)
    except FileNotFoundError:
        logging.error("MCP CLI not found. Make sure it's installed with 'pip install mcp[cli]'")
        sys.exit(1)


if __name__ == "__main__":
    main()
