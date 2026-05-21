"""
Small utility functions used in various places.
Nothing complicated — just convenience stuff.
"""

import os
import platform
import threading


def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_assets_path(*parts):
    return os.path.join(get_project_root(), "assets", *parts)


def is_windows():
    return platform.system() == "Windows"


def run_threaded(func, *args, callback=None):
    """Run func in a daemon thread. Optionally call callback with the result."""
    def _wrapper():
        result = func(*args)
        if callback:
            callback(result)

    t = threading.Thread(target=_wrapper, daemon=True)
    t.start()
    return t


def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)


def truncate(text, length=50):
    """Shorten text with '...' if it's too long."""
    if len(text) <= length:
        return text
    return text[:length - 3] + "..."
