"""
Cleanup panel — scan temp files and run cleanup operations.
"""

import customtkinter as ctk
import threading

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
            font=ctk.CTkFont(size=22, weight="bold"), anchor="w"
        ).grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        ctk.CTkLabel(
            self, text="Free up disk space by removing temp files and cache",
            font=ctk.CTkFont(size=12), text_color="#888888", anchor="w"
        ).grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # scan results card
        info = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        info.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.size_lbl = ctk.CTkLabel(
            info, text="Scanning...", font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
        )
        self.size_lbl.grid(row=0, column=0, padx=15, pady=(12, 3), sticky="w")
        self.count_lbl = ctk.CTkLabel(
            info, text="", font=ctk.CTkFont(size=12), text_color="#888888", anchor="w"
        )
        self.count_lbl.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="w")

        # action buttons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        btns.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_temp = ctk.CTkButton(
            btns, text="Clean Temp Files", height=40, corner_radius=8,
            fg_color="#3D5AFE", hover_color="#304FFE", command=self._do_temp
        )
        self.btn_temp.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_recycle = ctk.CTkButton(
            btns, text="Empty Recycle Bin", height=40, corner_radius=8,
            fg_color="#3D5AFE", hover_color="#304FFE", command=self._do_recycle
        )
        self.btn_recycle.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.btn_cache = ctk.CTkButton(
            btns, text="Clear Browser Cache", height=40, corner_radius=8,
            fg_color="#3D5AFE", hover_color="#304FFE", command=self._do_cache
        )
        self.btn_cache.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # activity log
        log_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        log_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        log_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            log_frame, text="Activity Log",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4A9EFF", anchor="w"
        ).grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

        self.log = ctk.CTkTextbox(
            log_frame, height=150, font=ctk.CTkFont(size=11),
            fg_color="#1E1E30", corner_radius=8
        )
        self.log.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="ew")
        self._log("Ready.")

        ctk.CTkLabel(
            self, text="Tip: Close browsers before clearing cache.",
            font=ctk.CTkFont(size=11), text_color="#FFA726", anchor="w"
        ).grid(row=5, column=0, padx=20, pady=(5, 10), sticky="w")

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
        self.count_lbl.configure(text=f"{r['file_count']} files in temp directories")

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
            self.after(0, lambda: self._simple_done(r, self.btn_recycle, "Empty Recycle Bin"))
        threading.Thread(target=task, daemon=True).start()

    def _do_cache(self):
        self.btn_cache.configure(state="disabled", text="Clearing...")
        self._log("Clearing browser cache...")
        def task():
            r = clean_browser_cache()
            self.after(0, lambda: self._simple_done(r, self.btn_cache, "Clear Browser Cache"))
        threading.Thread(target=task, daemon=True).start()

    def _simple_done(self, r, btn, text):
        btn.configure(state="normal", text=text)
        self._log(r["message"])

    def _log(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", f"  > {msg}\n")
        self.log.configure(state="disabled")
        self.log.see("end")
