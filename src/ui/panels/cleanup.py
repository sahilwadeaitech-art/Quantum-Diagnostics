"""
Cleanup Panel
Temp file cleaning, recycle bin, and cache cleanup utilities.
"""

import customtkinter as ctk
import threading

from src.cleanup.temp_cleaner import (
    calculate_temp_size,
    clean_temp_files,
    clean_recycle_bin,
    clean_browser_cache,
)


class CleanupPanel(ctk.CTkFrame):
    """Panel for system cleanup operations."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()
        self._scan_temp_files()

    def _build_ui(self):
        """Build the cleanup panel layout."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="System Cleanup",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Clean temporary files and free up disk space",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w",
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Temp files info card
        self.info_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        self.info_card.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.temp_size_label = ctk.CTkLabel(
            self.info_card,
            text="Scanning temporary files...",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )
        self.temp_size_label.grid(row=0, column=0, padx=15, pady=(12, 3), sticky="w")

        self.temp_count_label = ctk.CTkLabel(
            self.info_card,
            text="Please wait...",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w",
        )
        self.temp_count_label.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="w")

        # Action buttons
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        self.actions_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Clean Temp Files button
        self.clean_temp_btn = ctk.CTkButton(
            self.actions_frame,
            text="Clean Temp Files",
            height=40,
            corner_radius=8,
            fg_color="#3D5AFE",
            hover_color="#304FFE",
            command=self._run_temp_cleanup,
        )
        self.clean_temp_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Empty Recycle Bin button
        self.recycle_btn = ctk.CTkButton(
            self.actions_frame,
            text="Empty Recycle Bin",
            height=40,
            corner_radius=8,
            fg_color="#3D5AFE",
            hover_color="#304FFE",
            command=self._run_recycle_cleanup,
        )
        self.recycle_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Clear Browser Cache button
        self.cache_btn = ctk.CTkButton(
            self.actions_frame,
            text="Clear Browser Cache",
            height=40,
            corner_radius=8,
            fg_color="#3D5AFE",
            hover_color="#304FFE",
            command=self._run_cache_cleanup,
        )
        self.cache_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Results area
        self.result_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        self.result_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        result_title = ctk.CTkLabel(
            self.result_frame,
            text="Activity Log",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4A9EFF",
            anchor="w",
        )
        result_title.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

        self.result_text = ctk.CTkTextbox(
            self.result_frame,
            height=150,
            font=ctk.CTkFont(size=11),
            fg_color="#1E1E30",
            corner_radius=8,
        )
        self.result_text.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="ew")
        self.result_frame.grid_columnconfigure(0, weight=1)
        self._log_message("Ready. Click a button to start cleanup.")

        # Warning note
        warning = ctk.CTkLabel(
            self,
            text="Note: Close browsers before clearing cache. Some files may be in use.",
            font=ctk.CTkFont(size=11),
            text_color="#FFA726",
            anchor="w",
        )
        warning.grid(row=5, column=0, padx=20, pady=(5, 10), sticky="w")

    def _scan_temp_files(self):
        """Scan temp files in background."""
        thread = threading.Thread(target=self._do_scan, daemon=True)
        thread.start()

    def _do_scan(self):
        """Perform temp file scan."""
        try:
            result = calculate_temp_size()
            self.after(0, self._update_scan_result, result)
        except Exception as e:
            self.after(0, lambda: self.temp_size_label.configure(text=f"Scan error: {e}"))

    def _update_scan_result(self, result):
        """Update UI with scan results."""
        self.temp_size_label.configure(
            text=f"Temporary files: {result['size_formatted']}"
        )
        self.temp_count_label.configure(
            text=f"{result['file_count']} files found in temp directories"
        )

    def _run_temp_cleanup(self):
        """Run temp file cleanup."""
        self.clean_temp_btn.configure(state="disabled", text="Cleaning...")
        self._log_message("Starting temp file cleanup...")

        def task():
            result = clean_temp_files()
            self.after(0, self._temp_cleanup_done, result)

        threading.Thread(target=task, daemon=True).start()

    def _temp_cleanup_done(self, result):
        """Handle temp cleanup completion."""
        self.clean_temp_btn.configure(state="normal", text="Clean Temp Files")
        msg = f"Deleted {result['deleted']} items, freed {result['freed']}"
        if result["failed"] > 0:
            msg += f" ({result['failed']} items skipped - in use)"
        self._log_message(msg)
        self._scan_temp_files()  # Refresh size

    def _run_recycle_cleanup(self):
        """Run recycle bin cleanup."""
        self.recycle_btn.configure(state="disabled", text="Emptying...")
        self._log_message("Emptying recycle bin...")

        def task():
            result = clean_recycle_bin()
            self.after(0, self._generic_cleanup_done, result, self.recycle_btn,
                       "Empty Recycle Bin")

        threading.Thread(target=task, daemon=True).start()

    def _run_cache_cleanup(self):
        """Run browser cache cleanup."""
        self.cache_btn.configure(state="disabled", text="Clearing...")
        self._log_message("Clearing browser cache...")

        def task():
            result = clean_browser_cache()
            self.after(0, self._generic_cleanup_done, result, self.cache_btn,
                       "Clear Browser Cache")

        threading.Thread(target=task, daemon=True).start()

    def _generic_cleanup_done(self, result, button, button_text):
        """Handle generic cleanup completion."""
        button.configure(state="normal", text=button_text)
        self._log_message(result["message"])

    def _log_message(self, message):
        """Add a message to the activity log."""
        self.result_text.configure(state="normal")
        self.result_text.insert("end", f"  > {message}\n")
        self.result_text.configure(state="disabled")
        self.result_text.see("end")
