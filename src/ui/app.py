"""
Main Application Window
Central UI controller with sidebar navigation and panel management.
"""

import customtkinter as ctk

from src.ui.panels.dashboard import DashboardPanel
from src.ui.panels.system_info import SystemInfoPanel
from src.ui.panels.performance import PerformancePanel
from src.ui.panels.cleanup import CleanupPanel
from src.ui.panels.network import NetworkPanel
from src.ui.panels.cmd_tools import CmdToolsPanel
from src.ui.panels.report import ReportPanel


# App configuration
APP_TITLE = "PC Health Diagnosis Tool"
APP_WIDTH = 1000
APP_HEIGHT = 650
MIN_WIDTH = 900
MIN_HEIGHT = 550


class App(ctk.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        # Configure window
        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(MIN_WIDTH, MIN_HEIGHT)

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Track active panel
        self._active_panel = None
        self._nav_buttons = {}

        # Build layout
        self._setup_layout()
        self._build_sidebar()
        self._build_content_area()

        # Show dashboard by default
        self._show_panel("dashboard")

    def _setup_layout(self):
        """Configure grid layout for sidebar + content."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _build_sidebar(self):
        """Build the navigation sidebar."""
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)  # Push footer down

        # App title in sidebar
        title_label = ctk.CTkLabel(
            self.sidebar,
            text="PC Health\nDiagnosis",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4A9EFF",
        )
        title_label.grid(row=0, column=0, padx=20, pady=(25, 5))

        version_label = ctk.CTkLabel(
            self.sidebar,
            text="v1.0.0",
            font=ctk.CTkFont(size=11),
            text_color="#888888",
        )
        version_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Navigation buttons
        nav_items = [
            ("dashboard", "Dashboard"),
            ("system_info", "System Info"),
            ("performance", "Performance"),
            ("cleanup", "Cleanup"),
            ("network", "Network"),
            ("cmd_tools", "CMD Tools"),
            ("report", "Export Report"),
        ]

        for idx, (panel_id, label) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {label}",
                font=ctk.CTkFont(size=13),
                height=38,
                anchor="w",
                corner_radius=8,
                fg_color="transparent",
                text_color="#CCCCCC",
                hover_color="#2B2B3D",
                command=lambda p=panel_id: self._show_panel(p),
            )
            btn.grid(row=idx + 2, column=0, padx=12, pady=2, sticky="ew")
            self._nav_buttons[panel_id] = btn

        # Footer
        footer = ctk.CTkLabel(
            self.sidebar,
            text="Built with Python",
            font=ctk.CTkFont(size=10),
            text_color="#666666",
        )
        footer.grid(row=9, column=0, padx=20, pady=(0, 15))

    def _build_content_area(self):
        """Build the main content area where panels are displayed."""
        self.content_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1A1A2E")
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Initialize panels (lazy loading)
        self._panels = {}

    def _show_panel(self, panel_id):
        """Switch to a different panel."""
        # Hide current panel
        if self._active_panel and self._active_panel in self._panels:
            self._panels[self._active_panel].grid_forget()

        # Create panel if not already created
        if panel_id not in self._panels:
            self._panels[panel_id] = self._create_panel(panel_id)

        # Show new panel
        self._panels[panel_id].grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Update sidebar button states
        for btn_id, btn in self._nav_buttons.items():
            if btn_id == panel_id:
                btn.configure(fg_color="#2B2B3D", text_color="#4A9EFF")
            else:
                btn.configure(fg_color="transparent", text_color="#CCCCCC")

        self._active_panel = panel_id

    def _create_panel(self, panel_id):
        """Create a panel instance by ID."""
        panel_map = {
            "dashboard": DashboardPanel,
            "system_info": SystemInfoPanel,
            "performance": PerformancePanel,
            "cleanup": CleanupPanel,
            "network": NetworkPanel,
            "cmd_tools": CmdToolsPanel,
            "report": ReportPanel,
        }

        panel_class = panel_map.get(panel_id)
        if panel_class:
            return panel_class(self.content_frame)
        return ctk.CTkFrame(self.content_frame)
