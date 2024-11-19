"""
Wrappers around common system commands (ipconfig, systeminfo, etc).
Only runs safe read-only commands — nothing destructive.
"""

import subprocess
import platform


def flush_dns():
    system = platform.system()
    if system == "Windows":
        return _run(["ipconfig", "/flushdns"])
    elif system == "Linux":
        return _run(["systemd-resolve", "--flush-caches"])
    elif system == "Darwin":
        return _run(["dscacheutil", "-flushcache"])
    return {"success": False, "output": "Unsupported OS"}


def get_ipconfig():
    if platform.system() == "Windows":
        return _run(["ipconfig", "/all"])
    return _run(["ip", "addr"])


def get_system_info_cmd():
    if platform.system() == "Windows":
        return _run(["systeminfo"], timeout=30)
    return _run(["uname", "-a"])


def get_tasklist():
    if platform.system() == "Windows":
        return _run(["tasklist"])
    return _run(["ps", "aux"])


def run_custom_command(cmd_str):
    """
    Run a user-typed command, but only if it matches our allowlist.
    We don't want users accidentally doing anything destructive.
    """
    allowed = [
        "ipconfig", "ping", "nslookup", "tracert", "netstat",
        "systeminfo", "tasklist", "hostname", "whoami",
        "uname", "ip addr", "ifconfig", "ps", "df", "free",
    ]
    cmd_lower = cmd_str.lower().strip()
    if not any(cmd_lower.startswith(a) for a in allowed):
        return {"success": False, "output": "Command not allowed. Only diagnostic commands permitted."}

    return _run(cmd_str.split())


def _run(cmd, timeout=15):
    """Execute command and return result dict."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = r.stdout if r.returncode == 0 else (r.stderr or r.stdout)
        return {"success": r.returncode == 0, "output": output.strip() or "No output."}
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "Command timed out."}
    except FileNotFoundError:
        return {"success": False, "output": f"Command not found: {cmd[0]}"}
    except OSError as e:
        return {"success": False, "output": f"Error: {e}"}
