"""
Live performance data — CPU, RAM, disk, battery, network speed.
Keeps previous network counters around for delta/speed calculation.
"""

import psutil
import time


class PerformanceMonitor:
    """
    Tracks system metrics. Keeps state for network speed calculation
    (need previous counters to compute delta).
    """

    def __init__(self):
        self._prev_net = psutil.net_io_counters()
        self._prev_time = time.time()

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=0.5)

    def get_cpu_per_core(self):
        return psutil.cpu_percent(interval=0.5, percpu=True)

    def get_ram_usage(self):
        ram = psutil.virtual_memory()
        return {
            "percent": ram.percent,
            "used_gb": ram.used / (1024 ** 3),
            "total_gb": ram.total / (1024 ** 3),
            "available_gb": ram.available / (1024 ** 3),
        }

    def get_disk_usage(self):
        for path in ["/", "C:\\"]:
            try:
                u = psutil.disk_usage(path)
                return {
                    "percent": u.percent,
                    "used_gb": u.used / (1024 ** 3),
                    "total_gb": u.total / (1024 ** 3),
                    "free_gb": u.free / (1024 ** 3),
                }
            except (FileNotFoundError, OSError):
                continue
        return {"percent": 0, "used_gb": 0, "total_gb": 0, "free_gb": 0}

    def get_battery_status(self):
        battery = psutil.sensors_battery()
        if battery is None:
            return {"available": False}
        return {
            "available": True,
            "percent": battery.percent,
            "plugged_in": battery.power_plugged,
            "time_left": self._fmt_secs(battery.secsleft) if battery.secsleft > 0 else "Calculating...",
        }

    def get_network_speed(self):
        """Computes download/upload speed since last call."""
        now_net = psutil.net_io_counters()
        now_time = time.time()

        elapsed = max(now_time - self._prev_time, 0.1)  # avoid div by zero

        dl = (now_net.bytes_recv - self._prev_net.bytes_recv) / elapsed
        ul = (now_net.bytes_sent - self._prev_net.bytes_sent) / elapsed

        self._prev_net = now_net
        self._prev_time = now_time

        return {
            "download": self._fmt_speed(dl),
            "upload": self._fmt_speed(ul),
            "download_raw": dl,
            "upload_raw": ul,
        }

    def get_all_metrics(self):
        return {
            "cpu": self.get_cpu_usage(),
            "ram": self.get_ram_usage(),
            "disk": self.get_disk_usage(),
            "battery": self.get_battery_status(),
            "network": self.get_network_speed(),
        }

    @staticmethod
    def _fmt_speed(bps):
        if bps < 1024:
            return f"{bps:.1f} B/s"
        elif bps < 1024 ** 2:
            return f"{bps / 1024:.1f} KB/s"
        return f"{bps / (1024**2):.1f} MB/s"

    @staticmethod
    def _fmt_secs(secs):
        if secs < 0:
            return "Unknown"
        h = secs // 3600
        m = (secs % 3600) // 60
        return f"{int(h)}h {int(m)}m"
