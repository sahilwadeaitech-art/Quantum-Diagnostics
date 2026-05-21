"""
Helper Utilities
Common helper functions used across the application.
"""

import os
import sys
import platform
import threading


def get_project_root():
    """Get the project root directory path."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_assets_path(*parts):
    """Get path to an asset file."""
    return os.path.join(get_project_root(), "assets", *parts)


def is_windows():
    """Check if running on Windows."""
    return platform.system() == "Windows"


def is_linux():
    """Check if running on Linux."""
    return platform.system() == "Linux"


def is_mac():
    """Check if running on macOS."""
    return platform.system() == "Darwin"


def run_in_thread(func, *args, callback=None):
    """
    Run a function in a background thread to prevent UI freezing.

    Args:
        func: Function to run
        *args: Arguments to pass to the function
        callback: Optional callback to run with the result on completion
    """
    def wrapper():
        result = func(*args)
        if callback:
            callback(result)

    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()
    return thread


def format_uptime(seconds):
    """Format uptime in seconds to a readable string."""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")

    return " ".join(parts)


def truncate_text(text, max_length=50):
    """Truncate text with ellipsis if too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def safe_get(dictionary, *keys, default="N/A"):
    """Safely get nested dictionary values."""
    current = dictionary
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        else:
            return default
    return current
