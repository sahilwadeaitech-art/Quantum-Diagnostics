"""
System Information Service
Gathers hardware and OS details using psutil and platform modules.
"""

import platform
import socket
import psutil
from datetime import datetime


def get_cpu_info():
    """Get CPU details including cores, frequency, and architecture."""
    freq = psutil.cpu_freq()
    return {
        "processor": platform.processor() or "Unknown",
        "architecture": platform.machine(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "max_frequency": f"{freq.max:.0f} MHz" if freq else "N/A",
        "current_frequency": f"{freq.current:.0f} MHz" if freq else "N/A",
    }


def get_ram_info():
    """Get RAM usage and capacity details."""
    ram = psutil.virtual_memory()
    return {
        "total": _format_bytes(ram.total),
        "available": _format_bytes(ram.available),
        "used": _format_bytes(ram.used),
        "percent_used": ram.percent,
    }


def get_os_info():
    """Get operating system details."""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "hostname": socket.gethostname(),
        "username": _get_username(),
    }


def get_storage_info():
    """Get disk partition and usage information."""
    partitions = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "filesystem": part.fstype,
                "total": _format_bytes(usage.total),
                "used": _format_bytes(usage.used),
                "free": _format_bytes(usage.free),
                "percent_used": usage.percent,
            })
        except PermissionError:
            # Skip partitions we can't access
            continue
    return partitions


def get_boot_time():
    """Get system boot time as formatted string."""
    boot = datetime.fromtimestamp(psutil.boot_time())
    return boot.strftime("%Y-%m-%d %H:%M:%S")


def get_full_system_info():
    """Gather all system information into a single dictionary."""
    return {
        "cpu": get_cpu_info(),
        "ram": get_ram_info(),
        "os": get_os_info(),
        "storage": get_storage_info(),
        "boot_time": get_boot_time(),
    }


# --- Helper Functions ---

def _format_bytes(bytes_val):
    """Convert bytes to human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} PB"


def _get_username():
    """Get current username safely."""
    import os
    try:
        return os.getlogin()
    except OSError:
        return os.environ.get("USER", os.environ.get("USERNAME", "Unknown"))
