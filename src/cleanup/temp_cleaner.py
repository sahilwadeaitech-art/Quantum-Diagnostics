"""
Temp file cleanup utilities.
Handles clearing temp dirs, recycle bin, and browser caches.

Note: Some files will be locked/in-use and can't be deleted — that's normal.
The cleaner just skips those and reports what it managed to remove.
"""

import os
import shutil
import platform
import subprocess
import tempfile


def get_temp_directories():
    """Figure out where temp files live on this OS."""
    system = platform.system()
    if system == "Windows":
        dirs = [
            os.environ.get("TEMP", ""),
            os.environ.get("TMP", ""),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp"),
            os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Temp"),
        ]
    else:
        dirs = ["/tmp", "/var/tmp", tempfile.gettempdir()]

    return [d for d in dirs if d and os.path.exists(d)]


def calculate_temp_size():
    """Walk temp dirs and sum up total size + file count."""
    total_size = 0
    count = 0

    for d in get_temp_directories():
        try:
            for root, _, files in os.walk(d):
                for f in files:
                    try:
                        total_size += os.path.getsize(os.path.join(root, f))
                        count += 1
                    except (OSError, PermissionError):
                        pass
        except (OSError, PermissionError):
            pass

    return {
        "size_bytes": total_size,
        "size_formatted": _fmt_size(total_size),
        "file_count": count,
    }


def clean_temp_files():
    """Delete what we can from temp directories. Returns stats."""
    deleted = 0
    failed = 0
    freed = 0

    for temp_dir in get_temp_directories():
        try:
            for item in os.listdir(temp_dir):
                path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(path):
                        freed += os.path.getsize(path)
                        os.remove(path)
                        deleted += 1
                    elif os.path.isdir(path):
                        freed += _dir_size(path)
                        shutil.rmtree(path, ignore_errors=True)
                        deleted += 1
                except (PermissionError, OSError):
                    failed += 1
        except (PermissionError, OSError):
            pass

    return {"deleted": deleted, "failed": failed, "freed": _fmt_size(freed), "freed_bytes": freed}


def clean_recycle_bin():
    """Empty recycle bin / trash. Windows uses PowerShell, Linux clears ~/.local/share/Trash."""
    system = platform.system()

    if system == "Windows":
        try:
            subprocess.run(
                ["powershell", "-Command", "Clear-RecycleBin", "-Force"],
                capture_output=True, timeout=30
            )
            return {"success": True, "message": "Recycle bin emptied."}
        except Exception as e:
            return {"success": False, "message": f"Failed: {e}"}

    elif system == "Linux":
        trash = os.path.expanduser("~/.local/share/Trash")
        if os.path.exists(trash):
            try:
                shutil.rmtree(trash, ignore_errors=True)
                os.makedirs(os.path.join(trash, "files"), exist_ok=True)
                os.makedirs(os.path.join(trash, "info"), exist_ok=True)
                return {"success": True, "message": "Trash emptied."}
            except OSError as e:
                return {"success": False, "message": f"Failed: {e}"}
        return {"success": True, "message": "Trash already empty."}

    return {"success": False, "message": "Not supported on this OS."}


def clean_browser_cache():
    """
    Best-effort cache clearing for Chrome/Edge.
    Browsers should be closed first or this won't fully work.
    """
    system = platform.system()
    cleared = []

    if system == "Windows":
        local = os.environ.get("LOCALAPPDATA", "")
        paths = [
            os.path.join(local, "Google", "Chrome", "User Data", "Default", "Cache"),
            os.path.join(local, "Microsoft", "Edge", "User Data", "Default", "Cache"),
        ]
    else:
        home = os.path.expanduser("~")
        paths = [
            os.path.join(home, ".cache", "google-chrome", "Default", "Cache"),
            os.path.join(home, ".cache", "mozilla", "firefox"),
        ]

    for p in paths:
        if os.path.exists(p):
            try:
                shutil.rmtree(p, ignore_errors=True)
                cleared.append(os.path.basename(os.path.dirname(p)))
            except (PermissionError, OSError):
                pass

    if cleared:
        return {"success": True, "message": f"Cleared cache for: {', '.join(cleared)}"}
    return {"success": True, "message": "No browser cache found or already clean."}


# ---- helpers ----

def _fmt_size(b):
    for unit in ["B", "KB", "MB", "GB"]:
        if b < 1024:
            return f"{b:.2f} {unit}"
        b /= 1024
    return f"{b:.2f} TB"


def _dir_size(path):
    total = 0
    try:
        for root, _, files in os.walk(path):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return total
