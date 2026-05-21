"""
Report export panel — generates a full system report as .txt file.
"""

import customtkinter as ctk
import threading

from src.utils.report_export import generate_txt_report


class ReportPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="Export Report",
            font=ctk.CTkFont(size=22, weight="bold"), anchor="w"
        ).grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        ctk.CTkLabel(
            self, text="Generate a text report of your system's current state",
            font=ctk.CTkFont(size=12), text_color="#888888", anchor="w"
        ).grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # what's included
        card = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        card.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(
            card, text="Report includes:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4A9EFF", anchor="w"
        ).grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

        items = [
            "Health score + rating",
            "CPU, RAM, storage details",
            "OS and hostname info",
            "Network status",
            "Recommendations (if any)",
        ]
        for i, item in enumerate(items):
            ctk.CTkLabel(
                card, text=f"  •  {item}",
                font=ctk.CTkFont(size=12), text_color="#CCCCCC", anchor="w"
            ).grid(row=i+1, column=0, padx=15, pady=1, sticky="w")
        ctk.CTkLabel(card, text="").grid(row=len(items)+1, column=0, pady=5)

        # generate button
        self.gen_btn = ctk.CTkButton(
            self, text="Generate Report", height=45,
            font=ctk.CTkFont(size=14, weight="bold"), corner_radius=10,
            fg_color="#3D5AFE", hover_color="#304FFE",
            command=self._generate
        )
        self.gen_btn.grid(row=3, column=0, padx=20, pady=15, sticky="ew")

        # status
        status_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        status_card.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.status_lbl = ctk.CTkLabel(
            status_card, text="Ready.", font=ctk.CTkFont(size=12),
            text_color="#888888", anchor="w"
        )
        self.status_lbl.grid(row=0, column=0, padx=15, pady=12, sticky="w")

        self.path_lbl = ctk.CTkLabel(
            status_card, text="", font=ctk.CTkFont(size=11),
            text_color="#4A9EFF", anchor="w", wraplength=500
        )
        self.path_lbl.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="w")

    def _generate(self):
        self.gen_btn.configure(state="disabled", text="Generating...")
        self.status_lbl.configure(text="Collecting data...", text_color="#FFA726")
        self.path_lbl.configure(text="")

        def task():
            try:
                r = generate_txt_report()
                self.after(0, self._done, r)
            except Exception as e:
                self.after(0, self._error, str(e))
        threading.Thread(target=task, daemon=True).start()

    def _done(self, r):
        self.gen_btn.configure(state="normal", text="Generate Report")
        if r["success"]:
            self.status_lbl.configure(text="Report saved!", text_color="#00E676")
            self.path_lbl.configure(text=f"→ {r['filepath']}")
        else:
            self.status_lbl.configure(text=f"Error: {r.get('message', '?')}", text_color="#EF5350")

    def _error(self, msg):
        self.gen_btn.configure(state="normal", text="Generate Report")
        self.status_lbl.configure(text=f"Error: {msg}", text_color="#EF5350")
