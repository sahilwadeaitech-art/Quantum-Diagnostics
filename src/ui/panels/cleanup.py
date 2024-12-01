"""
Cleanup panel — scan and remove temp files, recycle bin, browser cache.
"""

import customtkinter as ctk
import threading

from src.ui.theme import COLORS, FONT, SPACING, CARD_STYLE, BUTTON_PRIMARY, BUTTON_SECONDARY
from src.cleanup.temp_cleaner import (
    calculate_temp_size, clean_temp_files,
    clean_recycle_bin, clean_browser_cache,
)


class CleanupPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._build_ui()
        self._scan()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="System Cleanup",
            font=ctk.CTkFont(size=FONT["heading_lg"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=SPACING["xl"], pady=(SPACING["xl"], 2), sticky="w")

        ctk.CTkLabel(
            self, text="Free up disk space by removing temporary files and cache",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        ).grid(row=1, column=0, padx=SPACING["xl"], pady=(0, SPACING["lg"]), sticky="w")

        # scan results card
        scan_card = ctk.CTkFrame(self, **CARD_STYLE)
        scan_card.grid(row=2, column=0, padx=SPACING["xl"], pady=(0, SPACING["md"]), sticky="ew")

        self.size_lbl = ctk.CTkLabel(
            scan_card, text="Scanning...",
            font=ctk.CTkFont(size=FONT["heading_sm"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        )
        self.size_lbl.grid(row=0, column=0, padx=16, pady=(14, 2), sticky="w")

        self.count_lbl = ctk.CTkLabel(
            scan_card, text="",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_muted"], anchor="w"
        )
        self.count_lbl.grid(row=1, column=0, padx=16, pady=(0, 14), sticky="w")

        # action buttons row
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=3, column=0, padx=SPACING["lg"], pady=(0, SPACING["md"]), sticky="ew")
        btns.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_temp = ctk.CTkButton(
            btns, text="Clean Temp Files",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            command=self._do_temp, **BUTTON_PRIMARY
        )
        self.btn_temp.grid(row=0, column=0, padx=SPACING["xs"], pady=SPACING["xs"], sticky="ew")

        self.btn_recycle = ctk.CTkButton(
            btns, text="Empty Recycle Bin",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            command=self._do_recycle, **BUTTON_SECONDARY
        )
        self.btn_recycle.grid(row=0, column=1, padx=SPACING["xs"], pady=SPACING["xs"], sticky="ew")

        self.btn_cache = ctk.CTkButton(
            btns, text="Clear Browser Cache",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            command=self._do_cache, **BUTTON_SECONDARY
        )
        self.btn_cache.grid(row=0, column=2, padx=SPACING["xs"], pady=SPACING["xs"], sticky="ew")

        # activity log
        log_card = ctk.CTkFrame(self, **CARD_STYLE)
        log_card.grid(row=4, column=0, padx=SPACING["xl"], pady=(0, SPACING["md"]), sticky="ew")
        log_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            log_card, text="Activity Log",
            font=ctk.CTkFont(size=FONT["heading_sm"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=16, pady=(14, 6), sticky="w")

        self.log = ctk.CTkTextbox(
            log_card, height=130,
            font=ctk.CTkFont(family="Consolas", size=FONT["caption"]),
            fg_color=COLORS["bg_input"], corner_radius=8,
            text_color=COLORS["text_secondary"],
            scrollbar_button_color=COLORS["border"],
        )
        self.log.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="ew")
        self._log("Ready.")

        # warning tip
        ctk.CTkLabel(
            self, text="⚠  Close browsers before clearing cache for best results.",
            font=ctk.CTkFont(size=FONT["caption"]),
            text_color=COLORS["warning"], anchor="w"
        ).grid(row=5, column=0, padx=SPACING["xl"], pady=(0, SPACING["lg"]), sticky="w")

    # ------------------------------------------------------------------ logic

    def _scan(self):
        def task():
            try:
                r = calculate_temp_size()
                self.after(0, lambda: self._show_scan(r))
            except Exception as e:
                self.after(0, lambda: self.size_lbl.configure(text=f"Error: {e}"))
        threading.Thread(target=task, daemon=True).start()

    def _show_scan(self, r):
        self.size_lbl.configure(text=f"Temp files: {r['size_formatted']}")
        self.count_lbl.configure(text=f"{r['file_count']} files found in temp directories")

    def _do_temp(self):
        self.btn_temp.configure(state="disabled", text="Cleaning...")
        self._log("Cleaning temp files...")
        def task():
            r = clean_temp_files()
            self.after(0, lambda: self._temp_done(r))
        threading.Thread(target=task, daemon=True).start()

    def _temp_done(self, r):
        self.btn_temp.configure(state="normal", text="Clean Temp Files")
        msg = f"Removed {r['deleted']} items, freed {r['freed']}"
        if r["failed"] > 0:
            msg += f" ({r['failed']} skipped — in use)"
        self._log(msg)
        self._scan()

    def _do_recycle(self):
        self.btn_recycle.configure(state="disabled", text="Emptying...")
        self._log("Emptying recycle bin...")
        def task():
            r = clean_recycle_bin()
            self.after(0, lambda: self._done(r, self.btn_recycle, "Empty Recycle Bin"))
        threading.Thread(target=task, daemon=True).start()

    def _do_cache(self):
        self.btn_cache.configure(state="disabled", text="Clearing...")
        self._log("Clearing browser cache...")
        def task():
            r = clean_browser_cache()
            self.after(0, lambda: self._done(r, self.btn_cache, "Clear Browser Cache"))
        threading.Thread(target=task, daemon=True).start()

    def _done(self, r, btn, text):
        btn.configure(state="normal", text=text)
        self._log(r["message"])

    def _log(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", f" {msg}\n")
        self.log.configure(state="disabled")
        self.log.see("end")
