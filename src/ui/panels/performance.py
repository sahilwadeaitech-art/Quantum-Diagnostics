"""
Performance panel — live resource meters.
Refreshes every 2 seconds with color-coded progress bars and network activity.
"""

import customtkinter as ctk

from src.ui.theme import COLORS, FONT, SPACING, CARD_STYLE, usage_color
from src.monitoring.performance import PerformanceMonitor


class PerformancePanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self._monitor = PerformanceMonitor()
        self._job = None
        self._running = False

        self._build_ui()
        self._start()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="Performance Monitor",
            font=ctk.CTkFont(size=FONT["heading_lg"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=SPACING["xl"], pady=(SPACING["xl"], 2), sticky="w")

        ctk.CTkLabel(
            self, text="Real-time resource usage · auto-refreshes every 2s",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        ).grid(row=1, column=0, padx=SPACING["xl"], pady=(0, SPACING["lg"]), sticky="w")

        # 2x2 metrics grid
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.grid(row=2, column=0, padx=SPACING["lg"], pady=0, sticky="nsew")
        grid.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.cpu_bar, self.cpu_lbl = self._metric_card(grid, "CPU Usage", 0, 0)
        self.ram_bar, self.ram_lbl = self._metric_card(grid, "Memory Usage", 0, 1)
        self.disk_bar, self.disk_lbl = self._metric_card(grid, "Disk Usage", 1, 0)
        self.batt_bar, self.batt_lbl = self._metric_card(grid, "Battery", 1, 1)

        # network activity card (full width)
        net_card = ctk.CTkFrame(grid, **CARD_STYLE)
        net_card.grid(row=2, column=0, columnspan=2, padx=SPACING["xs"], pady=SPACING["xs"], sticky="ew")
        net_card.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            net_card, text="Network Activity",
            font=ctk.CTkFont(size=FONT["heading_sm"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, columnspan=3, padx=16, pady=(14, 8), sticky="w")

        self.dl_label = ctk.CTkLabel(
            net_card, text="↓  --",
            font=ctk.CTkFont(size=FONT["body"]),
            text_color=COLORS["success"], anchor="w"
        )
        self.dl_label.grid(row=1, column=0, padx=16, pady=(0, 14), sticky="w")

        self.ul_label = ctk.CTkLabel(
            net_card, text="↑  --",
            font=ctk.CTkFont(size=FONT["body"]),
            text_color=COLORS["secondary"], anchor="w"
        )
        self.ul_label.grid(row=1, column=1, padx=16, pady=(0, 14), sticky="w")

        # process count
        self.proc_label = ctk.CTkLabel(
            net_card, text="Processes: --",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_muted"], anchor="e"
        )
        self.proc_label.grid(row=1, column=2, padx=16, pady=(0, 14), sticky="e")

        # status indicator
        self.status_lbl = ctk.CTkLabel(
            self, text="●  Live monitoring",
            font=ctk.CTkFont(size=FONT["caption"]),
            text_color=COLORS["success"], anchor="w"
        )
        self.status_lbl.grid(row=3, column=0, padx=SPACING["xl"], pady=(SPACING["sm"], SPACING["lg"]), sticky="w")

    def _metric_card(self, parent, title, row, col):
        """Card with title, big value, and progress bar."""
        card = ctk.CTkFrame(parent, **CARD_STYLE)
        card.grid(row=row, column=col, padx=SPACING["xs"], pady=SPACING["xs"], sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        ).grid(row=0, column=0, padx=16, pady=(14, 4), sticky="w")

        val = ctk.CTkLabel(
            card, text="--%",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        )
        val.grid(row=1, column=0, padx=16, pady=0, sticky="w")

        bar = ctk.CTkProgressBar(
            card, height=6, corner_radius=3,
            fg_color=COLORS["progress_bg"],
            progress_color=COLORS["accent"],
        )
        bar.grid(row=2, column=0, padx=16, pady=(8, 16), sticky="ew")
        bar.set(0)

        return bar, val

    # ------------------------------------------------------------------- loop

    def _start(self):
        self._running = True
        self._tick()

    def _tick(self):
        if not self._running:
            return
        try:
            cpu = self._monitor.get_cpu_usage()
            self.cpu_lbl.configure(text=f"{cpu:.1f}%")
            self.cpu_bar.set(cpu / 100)
            self.cpu_bar.configure(progress_color=usage_color(cpu))

            ram = self._monitor.get_ram_usage()
            self.ram_lbl.configure(text=f"{ram['percent']:.1f}%")
            self.ram_bar.set(ram["percent"] / 100)
            self.ram_bar.configure(progress_color=usage_color(ram["percent"]))

            disk = self._monitor.get_disk_usage()
            self.disk_lbl.configure(text=f"{disk['percent']:.1f}%")
            self.disk_bar.set(disk["percent"] / 100)
            self.disk_bar.configure(progress_color=usage_color(disk["percent"]))

            batt = self._monitor.get_battery_status()
            if batt["available"]:
                plug = " ⚡" if batt["plugged_in"] else ""
                self.batt_lbl.configure(text=f"{batt['percent']}%{plug}")
                self.batt_bar.set(batt["percent"] / 100)
                # for battery, low = bad
                self.batt_bar.configure(
                    progress_color=COLORS["danger"] if batt["percent"] < 20 else COLORS["success"]
                )
            else:
                self.batt_lbl.configure(text="N/A")
                self.batt_bar.set(0)

            net = self._monitor.get_network_speed()
            self.dl_label.configure(text=f"↓  {net['download']}")
            self.ul_label.configure(text=f"↑  {net['upload']}")

            # running process count
            try:
                import psutil
                self.proc_label.configure(text=f"Processes: {len(psutil.pids())}")
            except Exception:
                pass

        except Exception:
            pass

        self._job = self.after(2000, self._tick)

    def destroy(self):
        self._running = False
        if self._job:
            self.after_cancel(self._job)
        super().destroy()
