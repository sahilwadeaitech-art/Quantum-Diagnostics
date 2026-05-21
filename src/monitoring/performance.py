"""
Performance Monitoring Service
Provides real-time system performance metrics.
"""

import psutil
import time


class PerformanceMonitor:
    """Monitors system performance metrics in real-time."""

    def __init__(self):
        self._prev_net_io = psutil.net_io_counters()
        self._prev_time = time.time()

    def get_cpu_usage(self):
        """Get current CPU usage percentage."""
        return psutil.cpu_percent(interval=0.5)

    def get_cpu_per_core(self):
        """Get CPU usage per core."""
        return psutil.cpu_percent(interval=0.5, percpu=True)

    def get_ram_usage(self):
        """Get current RAM usage percentage and details."""
        ram = psutil.virtual_memory()
        return {
            "percent": ram.percent,
            "used_gb": ram.used / (1024 ** 3),
            "total_gb": ram.total / (1024 ** 3),
            "available_gb": ram.available / (1024 ** 3),
        }

    def get_disk_usage(self):
        """Get primary disk usage percentage."""
        try:
            # Try common mount points
            for path in ["/", "C:\\"]:
                try:
                    usage = psutil.disk_usage(path)
                    return {
                        "percent": usage.percent,
                        "used_gb": usage.used / (1024 ** 3),
                        "total_gb": usage.total / (1024 ** 3),
                        "free_gb": usage.free / (1024 ** 3),
                    }
                except (FileNotFoundError, OSError):
                    continue
        except Exception:
            pass
        return {"percent": 0, "used_gb": 0, "total_gb": 0, "free_gb": 0}

    def get_battery_status(self):
        """Get battery status if available."""
        battery = psutil.sensors_battery()
        if battery is None:
            return {"available": False}
        return {
            "available": True,
            "percent": battery.percent,
            "plugged_in": battery.power_plugged,
            "time_left": self._format_seconds(battery.secsleft) if battery.secsleft > 0 else "Calculating...",
        }

    def get_network_speed(self):
        """Calculate current network upload/download speed."""
        current_net = psutil.net_io_counters()
        current_time = time.time()

        elapsed = current_time - self._prev_time
        if elapsed == 0:
            elapsed = 1

        download_speed = (current_net.bytes_recv - self._prev_net_io.bytes_recv) / elapsed
        upload_speed = (current_net.bytes_sent - self._prev_net_io.bytes_sent) / elapsed

        # Update previous values
        self._prev_net_io = current_net
        self._prev_time = current_time

        return {
            "download": self._format_speed(download_speed),
            "upload": self._format_speed(upload_speed),
            "download_raw": download_speed,
            "upload_raw": upload_speed,
        }

    def get_all_metrics(self):
        """Get all performance metrics at once."""
        return {
            "cpu": self.get_cpu_usage(),
            "ram": self.get_ram_usage(),
            "disk": self.get_disk_usage(),
            "battery": self.get_battery_status(),
            "network": self.get_network_speed(),
        }

    # --- Helper Methods ---

    @staticmethod
    def _format_speed(bytes_per_sec):
        """Format network speed to human-readable string."""
        if bytes_per_sec < 1024:
            return f"{bytes_per_sec:.1f} B/s"
        elif bytes_per_sec < 1024 ** 2:
            return f"{bytes_per_sec / 1024:.1f} KB/s"
        else:
            return f"{bytes_per_sec / (1024 ** 2):.1f} MB/s"

    @staticmethod
    def _format_seconds(seconds):
        """Format seconds into hours:minutes string."""
        if seconds < 0:
            return "Unknown"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"
