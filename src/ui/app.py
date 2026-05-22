"""
Main window — sidebar + content area.
"""

import customtkinter as ctk

from src.ui.theme import COLORS, FONT, SPACING, NAV_BUTTON, NAV_BUTTON_ACTIVE
from src.ui.panels.dashboard import DashboardPanel
from src.ui.panels.system_info import SystemInfoPanel
from src.ui.panels.performance import PerformancePanel
from src.ui.panels.cleanup import CleanupPanel
from src.ui.panels.network import NetworkPanel
from src.ui.panels.cmd_tools import CmdToolsPanel
from src.ui.panels.report import ReportPanel


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Quantum Diagnostics")
        self.geometry("1100x700")
        self.minsize(960, 600)
        self.configure(fg_color=COLORS["bg_base"])

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._active_panel = None
        self._nav_buttons = {}
        self._panels = {}

        self._setup_grid()
        self._create_sidebar()
        self._create_content_area()
        self._switch_panel("dashboard")

    def _setup_grid(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=220, corner_radius=0,
            fg_color=COLORS["bg_sidebar"],
            border_width=0,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(11, weight=1)
        self.sidebar.grid_propagate(False)

        # -- branding --
        ctk.CTkLabel(
            self.sidebar, text="⬡  Quantum",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS["text_primary"],
        ).grid(row=0, column=0, padx=SPACING["xl"], pady=(24, 0), sticky="w")

        ctk.CTkLabel(
            self.sidebar, text="     Diagnostics",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_muted"],
        ).grid(row=1, column=0, padx=SPACING["xl"], pady=(0, 4), sticky="w")

        # version badge
        ctk.CTkLabel(
            self.sidebar, text="     v1.2.0",
            font=ctk.CTkFont(size=FONT["tiny"]),
            text_color=COLORS["text_muted"],
        ).grid(row=2, column=0, padx=SPACING["xl"], pady=(0, 8), sticky="w")

        # divider
        ctk.CTkFrame(
            self.sidebar, height=1, fg_color=COLORS["border"]
        ).grid(row=3, column=0, padx=SPACING["lg"], pady=(4, 14), sticky="ew")

        # -- navigation --
        nav = [
            ("dashboard",    "◉  Dashboard"),
            ("system_info",  "▣  System Info"),
            ("performance",  "◈  Performance"),
            ("cleanup",      "◇  Cleanup"),
            ("network",      "◎  Network"),
            ("cmd_tools",    "▤  CMD Tools"),
            ("report",       "◫  Export Report"),
        ]

        for i, (key, label) in enumerate(nav):
            btn = ctk.CTkButton(
                self.sidebar, text=f" {label}",
                font=ctk.CTkFont(size=FONT["body"]),
                command=lambda k=key: self._switch_panel(k),
                **NAV_BUTTON,
            )
            btn.grid(row=i + 4, column=0, padx=10, pady=2, sticky="ew")
            self._nav_buttons[key] = btn

        # -- footer --
        ctk.CTkFrame(
            self.sidebar, height=1, fg_color=COLORS["border"]
        ).grid(row=12, column=0, padx=SPACING["lg"], pady=(8, 8), sticky="ew")

        ctk.CTkLabel(
            self.sidebar, text="  Built by Sahil Wade",
            font=ctk.CTkFont(size=FONT["tiny"]),
            text_color=COLORS["text_muted"],
        ).grid(row=13, column=0, padx=SPACING["lg"], pady=(0, 14), sticky="w")

    def _create_content_area(self):
        self.content = ctk.CTkFrame(
            self, corner_radius=14,
            fg_color=COLORS["bg_surface"],
            border_width=1,
            border_color=COLORS["border"],
        )
        self.content.grid(row=0, column=1, padx=(0, 8), pady=8, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    # --------------------------------------------------------------- nav logic

    def _switch_panel(self, panel_id):
        if self._active_panel and self._active_panel in self._panels:
            self._panels[self._active_panel].grid_forget()

        if panel_id not in self._panels:
            self._panels[panel_id] = self._make_panel(panel_id)

        self._panels[panel_id].grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

        for key, btn in self._nav_buttons.items():
            if key == panel_id:
                btn.configure(**NAV_BUTTON_ACTIVE)
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["text_secondary"])

        self._active_panel = panel_id

    def _make_panel(self, panel_id):
        panels = {
            "dashboard": DashboardPanel,
            "system_info": SystemInfoPanel,
            "performance": PerformancePanel,
            "cleanup": CleanupPanel,
            "network": NetworkPanel,
            "cmd_tools": CmdToolsPanel,
            "report": ReportPanel,
        }
        cls = panels.get(panel_id)
        if cls:
            return cls(self.content)
        return ctk.CTkFrame(self.content)
