"""
CMD Utilities
Quick access to common system command-line utilities.
"""

import subprocess
import platform


def flush_dns():
    """Flush the DNS resolver cache."""
    system = platform.system()

    if system == "Windows":
        cmd = ["ipconfig", "/flushdns"]
    elif system == "Linux":
        # Try systemd-resolve first, then fall back
        cmd = ["systemd-resolve", "--flush-caches"]
    elif system == "Darwin":
        cmd = ["dscacheutil", "-flushcache"]
    else:
        return {"success": False, "output": "Unsupported operating system."}

    return _run_command(cmd)


def get_ipconfig():
    """Get network adapter configuration."""
    system = platform.system()

    if system == "Windows":
        cmd = ["ipconfig", "/all"]
    else:
        cmd = ["ip", "addr"]

    return _run_command(cmd)


def get_system_info_cmd():
    """Get detailed system information via command line."""
    system = platform.system()

    if system == "Windows":
        cmd = ["systeminfo"]
    else:
        cmd = ["uname", "-a"]

    return _run_command(cmd, timeout=30)


def get_tasklist():
    """Get list of running processes."""
    system = platform.system()

    if system == "Windows":
        cmd = ["tasklist"]
    else:
        cmd = ["ps", "aux"]

    return _run_command(cmd)


def run_custom_command(command_str):
    """
    Run a custom command string.
    Only allows safe, read-only commands.

    Args:
        command_str: Command to execute (will be validated)
    """
    # Safety: only allow known safe commands
    allowed_prefixes = [
        "ipconfig", "ping", "nslookup", "tracert", "netstat",
        "systeminfo", "tasklist", "hostname", "whoami",
        "uname", "ip addr", "ifconfig", "ps", "df", "free",
    ]

    command_lower = command_str.lower().strip()
    is_safe = any(command_lower.startswith(prefix) for prefix in allowed_prefixes)

    if not is_safe:
        return {
            "success": False,
            "output": "Command not allowed. Only diagnostic commands are permitted.",
        }

    # Split command for subprocess
    parts = command_str.split()
    return _run_command(parts)


# --- Helper Functions ---

def _run_command(cmd, timeout=15):
    """Execute a system command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        output = result.stdout if result.returncode == 0 else (result.stderr or result.stdout)

        return {
            "success": result.returncode == 0,
            "output": output.strip() if output else "No output.",
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "Command timed out."}
    except FileNotFoundError:
        return {"success": False, "output": f"Command not found: {cmd[0]}"}
    except OSError as e:
        return {"success": False, "output": f"Error: {str(e)}"}
