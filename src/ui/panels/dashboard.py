"""
Dashboard panel — the main home screen.
Shows health score prominently, quick resource stats, and system summary.
Designed to feel like a modern diagnostics overview.
"""

import customtkinter as ctk
import threading
import psutil
import time

from src.ui.theme import COLORS, FONT, SPACING, CARD_STYLE, BUTTON_SECONDARY, rating_color, usage_color
from src.services.health_score import calculate_health_score
from src.services.system_info import get_os_info, get_cpu_info, get_ram_info
from src.monitoring.performance import PerformanceMonitor


class DashboardPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._monitor = PerformanceMonitor()
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        # -- header --
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=SPACING["xl"], pady=(SPACING["xl"], 0), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="Dashboard",
            font=ctk.CTkFont(size=FONT["heading_lg"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header, text="↻  Refresh", width=90,
            font=ctk.CTkFont(size=FONT["body_sm"]),
            command=self._refresh, **BUTTON_SECONDARY,
        ).grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(
            self, text="System health overview and diagnostics summary",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        ).grid(row=1, column=0, padx=SPACING["xl"], pady=(2, SPACING["lg"]), sticky="w")

        # -- health score hero card --
        self.hero_card = ctk.CTkFrame(self, **CARD_STYLE)
        self.hero_card.grid(row=2, column=0, padx=SPACING["xl"], pady=(0, SPACING["md"]), sticky="ew")
        self.hero_card.grid_columnconfigure(1, weight=1)

        # score circle area (left)
        score_frame = ctk.CTkFrame(self.hero_card, fg_color="transparent", width=100)
        score_frame.grid(row=0, column=0, padx=(24, 12), pady=20, rowspan=3)
        score_frame.grid_propagate(False)

        self.score_num = ctk.CTkLabel(
            score_frame, text="--",
            font=ctk.CTkFont(size=44, weight="bold"),
            text_color=COLORS["accent"],
        )
        self.score_num.place(relx=0.5, rely=0.35, anchor="center")

        self.score_unit = ctk.CTkLabel(
            score_frame, text="/100",
            font=ctk.CTkFont(size=FONT["caption"]),
            text_color=COLORS["text_muted"],
        )
        self.score_unit.place(relx=0.5, rely=0.7, anchor="center")

        # rating + detail (center)
        self.rating_lbl = ctk.CTkLabel(
            self.hero_card, text="Analyzing...",
            font=ctk.CTkFont(size=FONT["heading_md"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        )
        self.rating_lbl.grid(row=0, column=1, padx=4, pady=(22, 0), sticky="sw")

        self.detail_lbl = ctk.CTkLabel(
            self.hero_card, text="Running system diagnostics...",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        )
        self.detail_lbl.grid(row=1, column=1, padx=4, pady=(2, 0), sticky="nw")

        # score breakdown bar (bottom of card)
        breakdown = ctk.CTkFrame(self.hero_card, fg_color="transparent")
        breakdown.grid(row=2, column=1, padx=4, pady=(8, 18), sticky="w")

        self.cpu_score_chip = self._score_chip(breakdown, "CPU", 0)
        self.ram_score_chip = self._score_chip(breakdown, "RAM", 1)
        self.disk_score_chip = self._score_chip(breakdown, "Disk", 2)

        # status indicator (right edge)
        self.status_dot = ctk.CTkLabel(
            self.hero_card, text="●",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_muted"],
        )
        self.status_dot.grid(row=0, column=2, padx=(0, 20), pady=(20, 0), sticky="ne")

        # -- resource cards row --
        cards_row = ctk.CTkFrame(self, fg_color="transparent")
        cards_row.grid(row=3, column=0, padx=SPACING["lg"], pady=(0, SPACING["md"]), sticky="ew")
        cards_row.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.cpu_card = self._resource_card(cards_row, "CPU", "--", 0)
        self.ram_card = self._resource_card(cards_row, "Memory", "--", 1)
        self.disk_card = self._resource_card(cards_row, "Storage", "--", 2)
        self.batt_card = self._resource_card(cards_row, "Battery", "--", 3)

        # -- system info summary --
        self.info_card = ctk.CTkFrame(self, **CARD_STYLE)
        self.info_card.grid(row=4, column=0, padx=SPACING["xl"], pady=(0, SPACING["xl"]), sticky="ew")
        self.info_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.info_card, text="System Overview",
            font=ctk.CTkFont(size=FONT["heading_sm"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=16, pady=(14, 8), sticky="w", columnspan=2)

        self.info_values = {}
        fields = ["OS", "Hostname", "Processor", "RAM", "Uptime"]
        for i, key in enumerate(fields):
            ctk.CTkLabel(
                self.info_card, text=key,
                font=ctk.CTkFont(size=FONT["body_sm"]),
                text_color=COLORS["text_muted"], anchor="w", width=80
            ).grid(row=i + 1, column=0, padx=(16, 4), pady=2, sticky="w")

            lbl = ctk.CTkLabel(
                self.info_card, text="...",
                font=ctk.CTkFont(size=FONT["body_sm"]),
                text_color=COLORS["text_secondary"], anchor="w"
            )
            lbl.grid(row=i + 1, column=1, padx=4, pady=2, sticky="w")
            self.info_values[key] = lbl

        ctk.CTkLabel(self.info_card, text="", height=8).grid(row=len(fields) + 1, column=0)

    # ---------------------------------------------------------- helper widgets

    def _score_chip(self, parent, label, col):
        """Small pill showing individual component score."""
        chip = ctk.CTkFrame(parent, corner_radius=6, fg_color=COLORS["bg_input"], height=26)
        chip.grid(row=0, column=col, padx=(0, 8), sticky="w")

        name = ctk.CTkLabel(
            chip, text=f"{label}:",
            font=ctk.CTkFont(size=FONT["caption"]),
            text_color=COLORS["text_muted"]
        )
        name.grid(row=0, column=0, padx=(8, 2), pady=4)

        val = ctk.CTkLabel(
            chip, text="--",
            font=ctk.CTkFont(size=FONT["caption"], weight="bold"),
            text_color=COLORS["text_secondary"]
        )
        val.grid(row=0, column=1, padx=(0, 8), pady=4)
        return val

    def _resource_card(self, parent, title, value, col):
        """Small resource usage card with title + percentage."""
        card = ctk.CTkFrame(parent, **CARD_STYLE)
        card.grid(row=0, column=col, padx=SPACING["xs"], pady=SPACING["xs"], sticky="ew")

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=FONT["caption"]),
            text_color=COLORS["text_muted"]
        ).grid(row=0, column=0, padx=14, pady=(12, 0))

        val_lbl = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        val_lbl.grid(row=1, column=0, padx=14, pady=(2, 4))

        # thin progress bar
        bar = ctk.CTkProgressBar(
            card, height=4, corner_radius=2,
            fg_color=COLORS["progress_bg"],
            progress_color=COLORS["accent"],
        )
        bar.grid(row=2, column=0, padx=14, pady=(0, 12), sticky="ew")
        bar.set(0)

        return {"label": val_lbl, "bar": bar}

    # ------------------------------------------------------------------- data

    def _refresh(self):
        threading.Thread(target=self._load, daemon=True).start()

    def _load(self):
        try:
            health = calculate_health_score()
            self.after(0, self._show_health, health)

            metrics = self._monitor.get_all_metrics()
            self.after(0, self._show_resources, metrics)

            os_info = get_os_info()
            cpu_info = get_cpu_info()
            ram_info = get_ram_info()
            self.after(0, self._show_system, os_info, cpu_info, ram_info)
        except Exception as e:
            self.after(0, lambda: self.rating_lbl.configure(text=f"Error: {e}"))

    def _show_health(self, h):
        score = h["overall_score"]
        rating = h["rating"]
        color = rating_color(rating)

        self.score_num.configure(text=str(int(score)), text_color=color)
        self.rating_lbl.configure(text=f"System Health: {rating}", text_color=color)
        self.detail_lbl.configure(text=h["details"][0] if h["details"] else "")
        self.status_dot.configure(text_color=color)

        self.cpu_score_chip.configure(text=f"{h['cpu_score']:.0f}")
        self.ram_score_chip.configure(text=f"{h['ram_score']:.0f}")
        self.disk_score_chip.configure(text=f"{h['disk_score']:.0f}")

    def _show_resources(self, m):
        # CPU
        cpu_pct = m["cpu"]
        self.cpu_card["label"].configure(text=f"{cpu_pct:.0f}%")
        self.cpu_card["bar"].set(cpu_pct / 100)
        self.cpu_card["bar"].configure(progress_color=usage_color(cpu_pct))

        # RAM
        ram_pct = m["ram"]["percent"]
        self.ram_card["label"].configure(text=f"{ram_pct:.0f}%")
        self.ram_card["bar"].set(ram_pct / 100)
        self.ram_card["bar"].configure(progress_color=usage_color(ram_pct))

        # Disk
        disk_pct = m["disk"]["percent"]
        self.disk_card["label"].configure(text=f"{disk_pct:.0f}%")
        self.disk_card["bar"].set(disk_pct / 100)
        self.disk_card["bar"].configure(progress_color=usage_color(disk_pct))

        # Battery
        batt = m["battery"]
        if batt["available"]:
            batt_pct = batt["percent"]
            plug = " ⚡" if batt["plugged_in"] else ""
            self.batt_card["label"].configure(text=f"{batt_pct}%{plug}")
            self.batt_card["bar"].set(batt_pct / 100)
            self.batt_card["bar"].configure(progress_color=COLORS["success"] if batt_pct > 20 else COLORS["danger"])
        else:
            self.batt_card["label"].configure(text="N/A")
            self.batt_card["bar"].set(0)

    def _show_system(self, os_info, cpu_info, ram_info):
        self.info_values["OS"].configure(text=f"{os_info['system']} {os_info['release']}")
        self.info_values["Hostname"].configure(text=os_info["hostname"])
        self.info_values["Processor"].configure(text=cpu_info["processor"][:40])
        self.info_values["RAM"].configure(text=ram_info["total"])

        # uptime
        try:
            boot = psutil.boot_time()
            uptime_sec = time.time() - boot
            hours = int(uptime_sec // 3600)
            mins = int((uptime_sec % 3600) // 60)
            self.info_values["Uptime"].configure(text=f"{hours}h {mins}m")
        except Exception:
            self.info_values["Uptime"].configure(text="--")
