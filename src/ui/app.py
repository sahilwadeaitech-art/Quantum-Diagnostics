"""
Main application window.
Sets up the sidebar nav + content area layout.
"""

import customtkinter as ctk

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

        self.title("PC Health Diagnosis Tool")
        self.geometry("1000x650")
        self.minsize(900, 550)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._active_panel = None
        self._nav_buttons = {}
        self._panels = {}

        self._setup_grid()
        self._create_sidebar()
        self._create_content_area()

        # open on dashboard
        self._switch_panel("dashboard")

    def _setup_grid(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        # branding
        ctk.CTkLabel(
            self.sidebar, text="PC Health\nDiagnosis",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4A9EFF"
        ).grid(row=0, column=0, padx=20, pady=(25, 5))

        ctk.CTkLabel(
            self.sidebar, text="v1.0.0",
            font=ctk.CTkFont(size=11), text_color="#888888"
        ).grid(row=1, column=0, padx=20, pady=(0, 20))

        # nav items
        nav = [
            ("dashboard", "Dashboard"),
            ("system_info", "System Info"),
            ("performance", "Performance"),
            ("cleanup", "Cleanup"),
            ("network", "Network"),
            ("cmd_tools", "CMD Tools"),
            ("report", "Export Report"),
        ]

        for i, (key, label) in enumerate(nav):
            btn = ctk.CTkButton(
                self.sidebar, text=f"  {label}",
                font=ctk.CTkFont(size=13), height=38, anchor="w",
                corner_radius=8, fg_color="transparent",
                text_color="#CCCCCC", hover_color="#2B2B3D",
                command=lambda k=key: self._switch_panel(k)
            )
            btn.grid(row=i + 2, column=0, padx=12, pady=2, sticky="ew")
            self._nav_buttons[key] = btn

        # footer
        ctk.CTkLabel(
            self.sidebar, text="Built with Python & CustomTkinter",
            font=ctk.CTkFont(size=10), text_color="#555555"
        ).grid(row=9, column=0, padx=20, pady=(0, 15))

    def _create_content_area(self):
        self.content = ctk.CTkFrame(self, corner_radius=12, fg_color="#1A1A2E")
        self.content.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    def _switch_panel(self, panel_id):
        """Switch the visible panel in the content area."""
        if self._active_panel and self._active_panel in self._panels:
            self._panels[self._active_panel].grid_forget()

        # lazy-create panels on first access
        if panel_id not in self._panels:
            self._panels[panel_id] = self._make_panel(panel_id)

        self._panels[panel_id].grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # highlight active nav button
        for key, btn in self._nav_buttons.items():
            if key == panel_id:
                btn.configure(fg_color="#2B2B3D", text_color="#4A9EFF")
            else:
                btn.configure(fg_color="transparent", text_color="#CCCCCC")

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
