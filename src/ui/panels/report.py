"""
Report Export Panel
Generate and export system health reports.
"""

import customtkinter as ctk
import threading
import os

from src.utils.report_export import generate_txt_report


class ReportPanel(ctk.CTkFrame):
    """Panel for generating system health reports."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        """Build the report export layout."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="Export Report",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Generate a comprehensive system health report",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w",
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Report info card
        info_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        info_card.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        info_title = ctk.CTkLabel(
            info_card,
            text="Report Contents",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4A9EFF",
            anchor="w",
        )
        info_title.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

        contents = [
            "System health score and rating",
            "CPU, RAM, and storage details",
            "Operating system information",
            "Network connectivity status",
            "Performance recommendations",
        ]

        for idx, item in enumerate(contents):
            lbl = ctk.CTkLabel(
                info_card,
                text=f"  •  {item}",
                font=ctk.CTkFont(size=12),
                text_color="#CCCCCC",
                anchor="w",
            )
            lbl.grid(row=idx + 1, column=0, padx=15, pady=1, sticky="w")

        spacer = ctk.CTkLabel(info_card, text="")
        spacer.grid(row=len(contents) + 1, column=0, pady=5)

        # Export options
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.grid(row=3, column=0, padx=15, pady=15, sticky="ew")
        options_frame.grid_columnconfigure(0, weight=1)

        # Format selection
        format_label = ctk.CTkLabel(
            options_frame,
            text="Export Format:",
            font=ctk.CTkFont(size=12),
            anchor="w",
        )
        format_label.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

        self.format_var = ctk.StringVar(value="txt")
        format_menu = ctk.CTkSegmentedButton(
            options_frame,
            values=["TXT"],
            variable=self.format_var,
            height=35,
            corner_radius=8,
        )
        format_menu.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        format_menu.set("TXT")

        # Generate button
        self.generate_btn = ctk.CTkButton(
            options_frame,
            text="Generate Report",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            fg_color="#3D5AFE",
            hover_color="#304FFE",
            command=self._generate_report,
        )
        self.generate_btn.grid(row=2, column=0, padx=5, pady=15, sticky="ew")

        # Status area
        self.status_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        self.status_frame.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready to generate report.",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w",
        )
        self.status_label.grid(row=0, column=0, padx=15, pady=12, sticky="w")

        self.filepath_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#4A9EFF",
            anchor="w",
            wraplength=500,
        )
        self.filepath_label.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="w")

    def _generate_report(self):
        """Generate the system health report."""
        self.generate_btn.configure(state="disabled", text="Generating...")
        self.status_label.configure(text="Gathering system data...", text_color="#FFA726")
        self.filepath_label.configure(text="")

        thread = threading.Thread(target=self._do_generate, daemon=True)
        thread.start()

    def _do_generate(self):
        """Generate report in background thread."""
        try:
            result = generate_txt_report()
            self.after(0, self._generation_done, result)
        except Exception as e:
            self.after(0, self._generation_error, str(e))

    def _generation_done(self, result):
        """Handle successful report generation."""
        self.generate_btn.configure(state="normal", text="Generate Report")

        if result["success"]:
            self.status_label.configure(
                text=f"Report generated successfully!",
                text_color="#00E676",
            )
            self.filepath_label.configure(text=f"Saved to: {result['filepath']}")
        else:
            self.status_label.configure(
                text=f"Error: {result.get('message', 'Unknown error')}",
                text_color="#EF5350",
            )

    def _generation_error(self, error_msg):
        """Handle report generation error."""
        self.generate_btn.configure(state="normal", text="Generate Report")
        self.status_label.configure(
            text=f"Error: {error_msg}",
            text_color="#EF5350",
        )
