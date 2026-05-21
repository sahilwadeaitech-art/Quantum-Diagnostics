"""
Performance panel — live-updating resource meters.
Refreshes every 2 seconds. Shows CPU, RAM, disk, battery, and network.
"""

import customtkinter as ctk

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
            font=ctk.CTkFont(size=22, weight="bold"), anchor="w"
        ).grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        ctk.CTkLabel(
            self, text="Real-time resource usage (updates every 2s)",
            font=ctk.CTkFont(size=12), text_color="#888888", anchor="w"
        ).grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # metrics grid
        metrics = ctk.CTkFrame(self, fg_color="transparent")
        metrics.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")
        metrics.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.cpu_bar, self.cpu_lbl = self._metric_card(metrics, "CPU Usage", 0, 0)
        self.ram_bar, self.ram_lbl = self._metric_card(metrics, "RAM Usage", 0, 1)
        self.disk_bar, self.disk_lbl = self._metric_card(metrics, "Disk Usage", 1, 0)
        self.batt_bar, self.batt_lbl = self._metric_card(metrics, "Battery", 1, 1)

        # network card
        net_card = ctk.CTkFrame(metrics, corner_radius=10, fg_color="#252540")
        net_card.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        net_card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            net_card, text="Network Activity",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4A9EFF", anchor="w"
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=(12, 5), sticky="w")

        self.dl_label = ctk.CTkLabel(net_card, text="Down: --", font=ctk.CTkFont(size=12), anchor="w")
        self.dl_label.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="w")
        self.ul_label = ctk.CTkLabel(net_card, text="Up: --", font=ctk.CTkFont(size=12), anchor="w")
        self.ul_label.grid(row=1, column=1, padx=15, pady=(0, 12), sticky="w")

        # status dot
        ctk.CTkLabel(
            self, text="● Live", font=ctk.CTkFont(size=11),
            text_color="#00E676", anchor="w"
        ).grid(row=3, column=0, padx=20, pady=10, sticky="w")

    def _metric_card(self, parent, title, row, col):
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color="#252540")
        card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=title, font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4A9EFF", anchor="w"
        ).grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

        val = ctk.CTkLabel(card, text="--%", font=ctk.CTkFont(size=20, weight="bold"), anchor="w")
        val.grid(row=1, column=0, padx=15, pady=0, sticky="w")

        bar = ctk.CTkProgressBar(card, height=8, corner_radius=4)
        bar.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="ew")
        bar.set(0)

        return bar, val

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

            ram = self._monitor.get_ram_usage()
            self.ram_lbl.configure(text=f"{ram['percent']:.1f}%")
            self.ram_bar.set(ram["percent"] / 100)

            disk = self._monitor.get_disk_usage()
            self.disk_lbl.configure(text=f"{disk['percent']:.1f}%")
            self.disk_bar.set(disk["percent"] / 100)

            batt = self._monitor.get_battery_status()
            if batt["available"]:
                plug = " ⚡" if batt["plugged_in"] else ""
                self.batt_lbl.configure(text=f"{batt['percent']}%{plug}")
                self.batt_bar.set(batt["percent"] / 100)
            else:
                self.batt_lbl.configure(text="No battery")
                self.batt_bar.set(0)

            net = self._monitor.get_network_speed()
            self.dl_label.configure(text=f"Down: {net['download']}")
            self.ul_label.configure(text=f"Up: {net['upload']}")
        except Exception:
            pass

        self._job = self.after(2000, self._tick)

    def destroy(self):
        self._running = False
        if self._job:
            self.after_cancel(self._job)
        super().destroy()
