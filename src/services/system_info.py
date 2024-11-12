"""
Pulls system hardware and OS info using psutil + platform.
Basically wraps everything into nice dicts for the UI to consume.
"""

import os
import platform
import socket
import psutil
from datetime import datetime


def get_cpu_info():
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
    ram = psutil.virtual_memory()
    return {
        "total": _fmt_bytes(ram.total),
        "available": _fmt_bytes(ram.available),
        "used": _fmt_bytes(ram.used),
        "percent_used": ram.percent,
    }


def get_os_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "hostname": socket.gethostname(),
        "username": _get_username(),
    }


def get_storage_info():
    """Returns list of partition dicts. Skips ones we can't access."""
    partitions = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "filesystem": part.fstype,
                "total": _fmt_bytes(usage.total),
                "used": _fmt_bytes(usage.used),
                "free": _fmt_bytes(usage.free),
                "percent_used": usage.percent,
            })
        except PermissionError:
            continue
    return partitions


def get_boot_time():
    boot = datetime.fromtimestamp(psutil.boot_time())
    return boot.strftime("%Y-%m-%d %H:%M:%S")


def get_full_system_info():
    """One-shot getter for all system info sections."""
    return {
        "cpu": get_cpu_info(),
        "ram": get_ram_info(),
        "os": get_os_info(),
        "storage": get_storage_info(),
        "boot_time": get_boot_time(),
    }


# ---- helpers ----

def _fmt_bytes(b):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if b < 1024:
            return f"{b:.2f} {unit}"
        b /= 1024
    return f"{b:.2f} PB"


def _get_username():
    try:
        return os.getlogin()
    except OSError:
        # fallback for environments where getlogin() fails (e.g. containers)
        return os.environ.get("USER", os.environ.get("USERNAME", "Unknown"))
