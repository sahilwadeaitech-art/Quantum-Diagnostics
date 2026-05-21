"""
Dashboard panel — the main "home" screen.
Shows the health score, quick resource stats, and basic system info.
"""

import customtkinter as ctk
import threading

from src.services.health_score import calculate_health_score
from src.services.system_info import get_os_info, get_cpu_info, get_ram_info
from src.monitoring.performance import PerformanceMonitor


class DashboardPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._monitor = PerformanceMonitor()
        self._build_ui()
        self._refresh_data()

    def _build_ui(self):
        # header
        ctk.CTkLabel(
            self, text="System Dashboard",
            font=ctk.CTkFont(size=22, weight="bold"), anchor="w"
        ).grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        ctk.CTkLabel(
            self, text="Quick overview of your system's health",
            font=ctk.CTkFont(size=12), text_color="#888888", anchor="w"
        ).grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # health score card
        self.score_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#252540")
        self.score_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.score_frame.grid_columnconfigure(1, weight=1)

        self.score_label = ctk.CTkLabel(
            self.score_frame, text="--",
            font=ctk.CTkFont(size=48, weight="bold"), text_color="#4A9EFF"
        )
        self.score_label.grid(row=0, column=0, padx=25, pady=15, rowspan=2)

        self.rating_label = ctk.CTkLabel(
            self.score_frame, text="Calculating...",
            font=ctk.CTkFont(size=16, weight="bold"), anchor="w"
        )
        self.rating_label.grid(row=0, column=1, padx=10, pady=(15, 0), sticky="sw")

        self.detail_label = ctk.CTkLabel(
            self.score_frame, text="Analyzing system...",
            font=ctk.CTkFont(size=11), text_color="#AAAAAA", anchor="w"
        )
        self.detail_label.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="nw")

        # quick stats row
        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        stats.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.cpu_card = self._stat_card(stats, "CPU", "--", 0)
        self.ram_card = self._stat_card(stats, "RAM", "--", 1)
        self.disk_card = self._stat_card(stats, "Disk", "--", 2)
        self.batt_card = self._stat_card(stats, "Battery", "--", 3)

        # system info summary
        self.info_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#252540")
        self.info_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(
            self.info_frame, text="System Info",
            font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
        ).grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w", columnspan=2)

        self.info_values = {}
        for i, key in enumerate(["OS", "Hostname", "Processor", "RAM"]):
            ctk.CTkLabel(
                self.info_frame, text=f"{key}:",
                font=ctk.CTkFont(size=12), text_color="#888888", anchor="w"
            ).grid(row=i+1, column=0, padx=15, pady=2, sticky="w")

            lbl = ctk.CTkLabel(
                self.info_frame, text="...",
                font=ctk.CTkFont(size=12), anchor="w"
            )
            lbl.grid(row=i+1, column=1, padx=10, pady=2, sticky="w")
            self.info_values[key] = lbl

        ctk.CTkLabel(self.info_frame, text="").grid(row=5, column=0, pady=5)

        # refresh button
        ctk.CTkButton(
            self, text="Refresh", width=100, height=32,
            corner_radius=8, command=self._refresh_data
        ).grid(row=5, column=0, padx=20, pady=10, sticky="w")

    def _stat_card(self, parent, title, value, col):
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color="#252540")
        card.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=11), text_color="#888888").grid(row=0, column=0, padx=15, pady=(10, 0))
        val_lbl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=18, weight="bold"))
        val_lbl.grid(row=1, column=0, padx=15, pady=(0, 10))
        return val_lbl

    def _refresh_data(self):
        threading.Thread(target=self._load_data, daemon=True).start()

    def _load_data(self):
        try:
            health = calculate_health_score()
            self.after(0, self._show_health, health)

            metrics = self._monitor.get_all_metrics()
            self.after(0, self._show_stats, metrics)

            os_info = get_os_info()
            cpu_info = get_cpu_info()
            ram_info = get_ram_info()
            self.after(0, self._show_info, os_info, cpu_info, ram_info)
        except Exception as e:
            self.after(0, lambda: self.rating_label.configure(text=f"Error: {e}"))

    def _show_health(self, h):
        score = h["overall_score"]
        rating = h["rating"]
        colors = {"Excellent": "#00E676", "Good": "#4A9EFF", "Moderate": "#FFA726", "Poor": "#EF5350"}
        color = colors.get(rating, "#4A9EFF")

        self.score_label.configure(text=str(int(score)), text_color=color)
        self.rating_label.configure(text=f"Health: {rating}", text_color=color)
        self.detail_label.configure(text=h["details"][0] if h["details"] else "")

    def _show_stats(self, m):
        self.cpu_card.configure(text=f"{m['cpu']:.0f}%")
        self.ram_card.configure(text=f"{m['ram']['percent']:.0f}%")
        self.disk_card.configure(text=f"{m['disk']['percent']:.0f}%")
        batt = m["battery"]
        self.batt_card.configure(text=f"{batt['percent']}%" if batt["available"] else "N/A")

    def _show_info(self, os_info, cpu_info, ram_info):
        self.info_values["OS"].configure(text=f"{os_info['system']} {os_info['release']}")
        self.info_values["Hostname"].configure(text=os_info["hostname"])
        self.info_values["Processor"].configure(text=cpu_info["processor"][:45])
        self.info_values["RAM"].configure(text=ram_info["total"])
