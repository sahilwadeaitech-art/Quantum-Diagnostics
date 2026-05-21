"""
Temporary File Cleaner
Handles cleanup of temp files, cache, and recycle bin.
"""

import os
import shutil
import platform
import subprocess
import tempfile


def get_temp_directories():
    """Get list of common temporary file directories based on OS."""
    temp_dirs = []
    system = platform.system()

    if system == "Windows":
        # Windows temp locations
        temp_dirs = [
            os.environ.get("TEMP", ""),
            os.environ.get("TMP", ""),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp"),
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Temp"),
        ]
    else:
        # Linux/Mac temp locations
        temp_dirs = [
            "/tmp",
            "/var/tmp",
            tempfile.gettempdir(),
        ]

    # Filter out empty or non-existent paths
    return [d for d in temp_dirs if d and os.path.exists(d)]


def calculate_temp_size():
    """Calculate total size of temporary files."""
    total_size = 0
    file_count = 0

    for temp_dir in get_temp_directories():
        try:
            for dirpath, dirnames, filenames in os.walk(temp_dir):
                for filename in filenames:
                    try:
                        filepath = os.path.join(dirpath, filename)
                        total_size += os.path.getsize(filepath)
                        file_count += 1
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            continue

    return {
        "size_bytes": total_size,
        "size_formatted": _format_size(total_size),
        "file_count": file_count,
    }


def clean_temp_files():
    """
    Delete temporary files from system temp directories.
    Returns summary of cleanup operation.
    """
    deleted_count = 0
    failed_count = 0
    freed_bytes = 0

    for temp_dir in get_temp_directories():
        try:
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        os.remove(item_path)
                        freed_bytes += size
                        deleted_count += 1
                    elif os.path.isdir(item_path):
                        size = _get_dir_size(item_path)
                        shutil.rmtree(item_path, ignore_errors=True)
                        freed_bytes += size
                        deleted_count += 1
                except (PermissionError, OSError):
                    failed_count += 1
                    continue
        except (PermissionError, OSError):
            continue

    return {
        "deleted": deleted_count,
        "failed": failed_count,
        "freed": _format_size(freed_bytes),
        "freed_bytes": freed_bytes,
    }


def clean_recycle_bin():
    """
    Empty the recycle bin (Windows only).
    On other systems, returns a not-supported message.
    """
    system = platform.system()

    if system == "Windows":
        try:
            # Use PowerShell to clear recycle bin silently
            subprocess.run(
                ["powershell", "-Command", "Clear-RecycleBin", "-Force"],
                capture_output=True,
                timeout=30,
            )
            return {"success": True, "message": "Recycle bin emptied successfully."}
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            return {"success": False, "message": f"Failed to empty recycle bin: {str(e)}"}
    elif system == "Linux":
        trash_path = os.path.expanduser("~/.local/share/Trash")
        if os.path.exists(trash_path):
            try:
                shutil.rmtree(trash_path, ignore_errors=True)
                os.makedirs(os.path.join(trash_path, "files"), exist_ok=True)
                os.makedirs(os.path.join(trash_path, "info"), exist_ok=True)
                return {"success": True, "message": "Trash emptied successfully."}
            except OSError as e:
                return {"success": False, "message": f"Failed: {str(e)}"}
        return {"success": True, "message": "Trash is already empty."}
    else:
        return {"success": False, "message": "Not supported on this operating system."}


def clean_browser_cache():
    """
    Attempt to clear common browser cache directories.
    This is a best-effort operation - browsers should be closed first.
    """
    system = platform.system()
    cleared = []

    if system == "Windows":
        local_app = os.environ.get("LOCALAPPDATA", "")
        cache_paths = [
            os.path.join(local_app, "Google", "Chrome", "User Data", "Default", "Cache"),
            os.path.join(local_app, "Microsoft", "Edge", "User Data", "Default", "Cache"),
        ]
    else:
        home = os.path.expanduser("~")
        cache_paths = [
            os.path.join(home, ".cache", "google-chrome", "Default", "Cache"),
            os.path.join(home, ".cache", "mozilla", "firefox"),
        ]

    for path in cache_paths:
        if os.path.exists(path):
            try:
                shutil.rmtree(path, ignore_errors=True)
                cleared.append(os.path.basename(os.path.dirname(path)))
            except (PermissionError, OSError):
                continue

    if cleared:
        return {"success": True, "message": f"Cleared cache for: {', '.join(cleared)}"}
    return {"success": True, "message": "No browser cache found or already clean."}


# --- Helper Functions ---

def _format_size(bytes_val):
    """Convert bytes to human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} TB"


def _get_dir_size(path):
    """Calculate total size of a directory."""
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                try:
                    total += os.path.getsize(os.path.join(dirpath, f))
                except (OSError, PermissionError):
                    continue
    except (OSError, PermissionError):
        pass
    return total
