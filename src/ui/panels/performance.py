"""
Performance Monitoring Panel
Live system performance metrics with auto-refresh.
"""

import customtkinter as ctk

from src.monitoring.performance import PerformanceMonitor


class PerformancePanel(ctk.CTkFrame):
    """Panel showing live performance metrics."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self._monitor = PerformanceMonitor()
        self._update_job = None
        self._is_monitoring = False

        self._build_ui()
        self._start_monitoring()

    def _build_ui(self):
        """Build the performance monitoring layout."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="Performance Monitor",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Real-time system resource usage",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w",
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Metrics container
        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")
        self.metrics_frame.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)

        # CPU Usage Card
        self.cpu_bar, self.cpu_label = self._create_metric_card(
            self.metrics_frame, "CPU Usage", 0, 0
        )

        # RAM Usage Card
        self.ram_bar, self.ram_label = self._create_metric_card(
            self.metrics_frame, "RAM Usage", 0, 1
        )

        # Disk Usage Card
        self.disk_bar, self.disk_label = self._create_metric_card(
            self.metrics_frame, "Disk Usage", 1, 0
        )

        # Battery Card
        self.battery_bar, self.battery_label = self._create_metric_card(
            self.metrics_frame, "Battery", 1, 1
        )

        # Network Card
        self.network_card = ctk.CTkFrame(
            self.metrics_frame, corner_radius=10, fg_color="#252540"
        )
        self.network_card.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.network_card.grid_columnconfigure((0, 1), weight=1)

        net_title = ctk.CTkLabel(
            self.network_card,
            text="Network Activity",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4A9EFF",
            anchor="w",
        )
        net_title.grid(row=0, column=0, columnspan=2, padx=15, pady=(12, 5), sticky="w")

        self.download_label = ctk.CTkLabel(
            self.network_card,
            text="Download: --",
            font=ctk.CTkFont(size=12),
            anchor="w",
        )
        self.download_label.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="w")

        self.upload_label = ctk.CTkLabel(
            self.network_card,
            text="Upload: --",
            font=ctk.CTkFont(size=12),
            anchor="w",
        )
        self.upload_label.grid(row=1, column=1, padx=15, pady=(0, 12), sticky="w")

        # Status indicator
        self.status_label = ctk.CTkLabel(
            self,
            text="● Live monitoring active",
            font=ctk.CTkFont(size=11),
            text_color="#00E676",
            anchor="w",
        )
        self.status_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

    def _create_metric_card(self, parent, title, row, col):
        """Create a metric card with progress bar."""
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color="#252540")
        card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        title_lbl = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4A9EFF",
            anchor="w",
        )
        title_lbl.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

        value_lbl = ctk.CTkLabel(
            card,
            text="--%",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        value_lbl.grid(row=1, column=0, padx=15, pady=0, sticky="w")

        progress = ctk.CTkProgressBar(card, height=8, corner_radius=4)
        progress.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="ew")
        progress.set(0)

        return progress, value_lbl

    def _start_monitoring(self):
        """Start the periodic monitoring updates."""
        self._is_monitoring = True
        self._update_metrics()

    def _update_metrics(self):
        """Update all metrics (called periodically)."""
        if not self._is_monitoring:
            return

        try:
            # CPU
            cpu = self._monitor.get_cpu_usage()
            self.cpu_label.configure(text=f"{cpu:.1f}%")
            self.cpu_bar.set(cpu / 100)

            # RAM
            ram = self._monitor.get_ram_usage()
            self.ram_label.configure(text=f"{ram['percent']:.1f}%")
            self.ram_bar.set(ram["percent"] / 100)

            # Disk
            disk = self._monitor.get_disk_usage()
            self.disk_label.configure(text=f"{disk['percent']:.1f}%")
            self.disk_bar.set(disk["percent"] / 100)

            # Battery
            battery = self._monitor.get_battery_status()
            if battery["available"]:
                batt_pct = battery["percent"]
                plug_status = " (Charging)" if battery["plugged_in"] else ""
                self.battery_label.configure(text=f"{batt_pct}%{plug_status}")
                self.battery_bar.set(batt_pct / 100)
            else:
                self.battery_label.configure(text="No Battery")
                self.battery_bar.set(0)

            # Network
            net = self._monitor.get_network_speed()
            self.download_label.configure(text=f"Download: {net['download']}")
            self.upload_label.configure(text=f"Upload: {net['upload']}")

        except Exception:
            pass  # Silently handle monitoring errors

        # Schedule next update (2 seconds)
        self._update_job = self.after(2000, self._update_metrics)

    def destroy(self):
        """Clean up monitoring when panel is destroyed."""
        self._is_monitoring = False
        if self._update_job:
            self.after_cancel(self._update_job)
        super().destroy()
