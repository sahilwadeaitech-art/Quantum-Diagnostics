"""
Dashboard Panel
Overview panel showing health score and quick system stats.
"""

import customtkinter as ctk
import threading

from src.services.health_score import calculate_health_score
from src.services.system_info import get_os_info, get_cpu_info, get_ram_info
from src.monitoring.performance import PerformanceMonitor


class DashboardPanel(ctk.CTkFrame):
    """Main dashboard with health score and quick stats."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self._monitor = PerformanceMonitor()
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        """Build the dashboard layout."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="System Dashboard",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Overview of your system's health and performance",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w",
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Health Score Card
        self.score_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#252540")
        self.score_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.score_frame.grid_columnconfigure(1, weight=1)

        self.score_label = ctk.CTkLabel(
            self.score_frame,
            text="--",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#4A9EFF",
        )
        self.score_label.grid(row=0, column=0, padx=25, pady=15, rowspan=2)

        self.rating_label = ctk.CTkLabel(
            self.score_frame,
            text="Calculating...",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        )
        self.rating_label.grid(row=0, column=1, padx=10, pady=(15, 0), sticky="sw")

        self.score_detail = ctk.CTkLabel(
            self.score_frame,
            text="Analyzing system health...",
            font=ctk.CTkFont(size=11),
            text_color="#AAAAAA",
            anchor="w",
        )
        self.score_detail.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="nw")

        # Quick Stats Row
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Stat cards
        self.cpu_card = self._create_stat_card(self.stats_frame, "CPU", "--", 0)
        self.ram_card = self._create_stat_card(self.stats_frame, "RAM", "--", 1)
        self.disk_card = self._create_stat_card(self.stats_frame, "Disk", "--", 2)
        self.battery_card = self._create_stat_card(self.stats_frame, "Battery", "--", 3)

        # System Info Summary
        self.info_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#252540")
        self.info_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        info_title = ctk.CTkLabel(
            self.info_frame,
            text="System Information",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )
        info_title.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w", columnspan=2)

        self.info_labels = {}
        info_items = ["OS", "Hostname", "Processor", "RAM"]
        for idx, item in enumerate(info_items):
            label = ctk.CTkLabel(
                self.info_frame,
                text=f"{item}:",
                font=ctk.CTkFont(size=12),
                text_color="#888888",
                anchor="w",
            )
            label.grid(row=idx + 1, column=0, padx=15, pady=2, sticky="w")

            value = ctk.CTkLabel(
                self.info_frame,
                text="Loading...",
                font=ctk.CTkFont(size=12),
                anchor="w",
            )
            value.grid(row=idx + 1, column=1, padx=10, pady=2, sticky="w")
            self.info_labels[item] = value

        # Add bottom padding
        spacer = ctk.CTkLabel(self.info_frame, text="")
        spacer.grid(row=len(info_items) + 1, column=0, pady=5)

        # Refresh button
        refresh_btn = ctk.CTkButton(
            self,
            text="Refresh",
            width=100,
            height=32,
            corner_radius=8,
            command=self._load_data,
        )
        refresh_btn.grid(row=5, column=0, padx=20, pady=10, sticky="w")

    def _create_stat_card(self, parent, title, value, col):
        """Create a small stat card widget."""
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color="#252540")
        card.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        title_lbl = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color="#888888",
        )
        title_lbl.grid(row=0, column=0, padx=15, pady=(10, 0))

        value_lbl = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        value_lbl.grid(row=1, column=0, padx=15, pady=(0, 10))

        return {"frame": card, "value_label": value_lbl}

    def _load_data(self):
        """Load all dashboard data in background thread."""
        thread = threading.Thread(target=self._fetch_data, daemon=True)
        thread.start()

    def _fetch_data(self):
        """Fetch data and update UI (runs in background thread)."""
        try:
            # Health score
            health = calculate_health_score()
            self.after(0, self._update_health_score, health)

            # Quick stats
            metrics = self._monitor.get_all_metrics()
            self.after(0, self._update_stats, metrics)

            # System info
            os_info = get_os_info()
            cpu_info = get_cpu_info()
            ram_info = get_ram_info()
            self.after(0, self._update_system_info, os_info, cpu_info, ram_info)

        except Exception as e:
            self.after(0, self._show_error, str(e))

    def _update_health_score(self, health):
        """Update health score display."""
        score = health["overall_score"]
        rating = health["rating"]

        # Color based on rating
        colors = {
            "Excellent": "#00E676",
            "Good": "#4A9EFF",
            "Moderate": "#FFA726",
            "Poor": "#EF5350",
        }
        color = colors.get(rating, "#4A9EFF")

        self.score_label.configure(text=str(int(score)), text_color=color)
        self.rating_label.configure(text=f"Health: {rating}", text_color=color)

        detail_text = health["details"][0] if health["details"] else ""
        self.score_detail.configure(text=detail_text)

    def _update_stats(self, metrics):
        """Update quick stat cards."""
        self.cpu_card["value_label"].configure(text=f"{metrics['cpu']:.0f}%")
        self.ram_card["value_label"].configure(text=f"{metrics['ram']['percent']:.0f}%")
        self.disk_card["value_label"].configure(text=f"{metrics['disk']['percent']:.0f}%")

        battery = metrics["battery"]
        if battery["available"]:
            self.battery_card["value_label"].configure(text=f"{battery['percent']}%")
        else:
            self.battery_card["value_label"].configure(text="N/A")

    def _update_system_info(self, os_info, cpu_info, ram_info):
        """Update system info section."""
        self.info_labels["OS"].configure(
            text=f"{os_info['system']} {os_info['release']}"
        )
        self.info_labels["Hostname"].configure(text=os_info["hostname"])
        self.info_labels["Processor"].configure(text=cpu_info["processor"][:45])
        self.info_labels["RAM"].configure(text=ram_info["total"])

    def _show_error(self, message):
        """Show error state."""
        self.rating_label.configure(text="Error loading data")
        self.score_detail.configure(text=message)
