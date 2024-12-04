"""
Report export panel — generates a .txt system health report.
"""

import customtkinter as ctk
import threading

from src.ui.theme import COLORS, FONT, SPACING, CARD_STYLE, BUTTON_PRIMARY
from src.utils.report_export import generate_txt_report


class ReportPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="Export Report",
            font=ctk.CTkFont(size=FONT["heading_lg"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=SPACING["xl"], pady=(SPACING["xl"], 2), sticky="w")

        ctk.CTkLabel(
            self, text="Generate a full system diagnostics report as a text file",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        ).grid(row=1, column=0, padx=SPACING["xl"], pady=(0, SPACING["xl"]), sticky="w")

        # what's included card
        card = ctk.CTkFrame(self, **CARD_STYLE)
        card.grid(row=2, column=0, padx=SPACING["xl"], pady=(0, SPACING["lg"]), sticky="ew")

        ctk.CTkLabel(
            card, text="Report Contents",
            font=ctk.CTkFont(size=FONT["heading_sm"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=16, pady=(14, 6), sticky="w")

        items = [
            "Health score and rating breakdown",
            "CPU, RAM, and storage diagnostics",
            "OS information and hostname",
            "Network connectivity status",
            "Performance recommendations",
        ]
        for i, item in enumerate(items):
            ctk.CTkLabel(
                card, text=f"  •  {item}",
                font=ctk.CTkFont(size=FONT["body_sm"]),
                text_color=COLORS["text_secondary"], anchor="w"
            ).grid(row=i + 1, column=0, padx=16, pady=1, sticky="w")

        ctk.CTkLabel(card, text="", height=8).grid(row=len(items) + 1, column=0)

        # generate button
        self.gen_btn = ctk.CTkButton(
            self, text="▶  Generate Report",
            font=ctk.CTkFont(size=FONT["body"], weight="bold"),
            command=self._generate, **BUTTON_PRIMARY, height=44
        )
        self.gen_btn.grid(row=3, column=0, padx=SPACING["xl"], pady=(0, SPACING["lg"]), sticky="ew")

        # status card
        status_card = ctk.CTkFrame(self, **CARD_STYLE)
        status_card.grid(row=4, column=0, padx=SPACING["xl"], pady=0, sticky="ew")

        self.status_lbl = ctk.CTkLabel(
            status_card, text="Ready to generate.",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_muted"], anchor="w"
        )
        self.status_lbl.grid(row=0, column=0, padx=16, pady=(14, 4), sticky="w")

        self.path_lbl = ctk.CTkLabel(
            status_card, text="",
            font=ctk.CTkFont(size=FONT["caption"]),
            text_color=COLORS["accent"], anchor="w", wraplength=480
        )
        self.path_lbl.grid(row=1, column=0, padx=16, pady=(0, 14), sticky="w")

    # ------------------------------------------------------------------ logic

    def _generate(self):
        self.gen_btn.configure(state="disabled", text="Generating...")
        self.status_lbl.configure(text="Collecting system data...", text_color=COLORS["warning"])
        self.path_lbl.configure(text="")

        def task():
            try:
                r = generate_txt_report()
                self.after(0, self._done, r)
            except Exception as e:
                self.after(0, self._error, str(e))
        threading.Thread(target=task, daemon=True).start()

    def _done(self, r):
        self.gen_btn.configure(state="normal", text="▶  Generate Report")
        if r["success"]:
            self.status_lbl.configure(text="✓  Report saved successfully!", text_color=COLORS["success"])
            self.path_lbl.configure(text=r["filepath"])
        else:
            self.status_lbl.configure(text=f"Error: {r.get('message', '?')}", text_color=COLORS["danger"])

    def _error(self, msg):
        self.gen_btn.configure(state="normal", text="▶  Generate Report")
        self.status_lbl.configure(text=f"Error: {msg}", text_color=COLORS["danger"])
