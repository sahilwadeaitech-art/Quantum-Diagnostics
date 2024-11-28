"""
System Info panel — scrollable hardware and OS details.
"""

import customtkinter as ctk
import threading

from src.ui.theme import COLORS, FONT, SPACING, CARD_STYLE
from src.services.system_info import get_full_system_info


class SystemInfoPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._build_ui()
        self._load()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="System Information",
            font=ctk.CTkFont(size=FONT["heading_lg"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=SPACING["xl"], pady=(SPACING["xl"], 2), sticky="w")

        ctk.CTkLabel(
            self, text="Hardware and operating system details",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        ).grid(row=1, column=0, padx=SPACING["xl"], pady=(0, SPACING["lg"]), sticky="w")

        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0,
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent_subtle"],
        )
        self.scroll.grid(row=2, column=0, padx=SPACING["md"], pady=(0, SPACING["md"]), sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.loading = ctk.CTkLabel(
            self.scroll, text="Loading system data...",
            font=ctk.CTkFont(size=FONT["body"]),
            text_color=COLORS["text_muted"]
        )
        self.loading.grid(row=0, column=0, pady=30)

    def _load(self):
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            data = get_full_system_info()
            self.after(0, self._display, data)
        except Exception as e:
            self.after(0, lambda: self.loading.configure(text=f"Error: {e}"))

    def _display(self, info):
        self.loading.destroy()
        row = 0

        os_d = info["os"]
        row = self._section(row, "Operating System", [
            ("System", f"{os_d['system']} {os_d['release']}"),
            ("Version", os_d["version"]),
            ("Hostname", os_d["hostname"]),
            ("User", os_d["username"]),
        ])

        cpu = info["cpu"]
        row = self._section(row, "Processor", [
            ("Name", cpu["processor"]),
            ("Architecture", cpu["architecture"]),
            ("Physical cores", str(cpu["physical_cores"])),
            ("Logical cores", str(cpu["logical_cores"])),
            ("Max frequency", cpu["max_frequency"]),
        ])

        ram = info["ram"]
        row = self._section(row, "Memory", [
            ("Total", ram["total"]),
            ("Used", ram["used"]),
            ("Available", ram["available"]),
            ("Usage", f"{ram['percent_used']}%"),
        ])

        storage_items = []
        for d in info["storage"]:
            storage_items.append(("Device", d["device"]))
            storage_items.append(("Mount", d["mountpoint"]))
            storage_items.append(("Size", f"{d['total']} (Free: {d['free']})"))
            storage_items.append(("Usage", f"{d['percent_used']}%"))
            storage_items.append(("", ""))
        row = self._section(row, "Storage", storage_items)

        self._section(row, "Uptime", [("Last boot", info["boot_time"])])

    def _section(self, start_row, title, items):
        card = ctk.CTkFrame(self.scroll, **CARD_STYLE)
        card.grid(row=start_row, column=0, padx=SPACING["xs"], pady=SPACING["xs"], sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=FONT["heading_sm"], weight="bold"),
            text_color=COLORS["accent"], anchor="w"
        ).grid(row=0, column=0, columnspan=2, padx=16, pady=(14, 8), sticky="w")

        for i, (k, v) in enumerate(items):
            if not k and not v:
                continue
            ctk.CTkLabel(
                card, text=k,
                font=ctk.CTkFont(size=FONT["body_sm"]),
                text_color=COLORS["text_muted"], anchor="w", width=120
            ).grid(row=i + 1, column=0, padx=(16, 4), pady=2, sticky="w")
            ctk.CTkLabel(
                card, text=str(v),
                font=ctk.CTkFont(size=FONT["body_sm"]),
                text_color=COLORS["text_secondary"], anchor="w", wraplength=380
            ).grid(row=i + 1, column=1, padx=4, pady=2, sticky="w")

        ctk.CTkLabel(card, text="", height=6).grid(row=len(items) + 1, column=0)
        return start_row + 1
