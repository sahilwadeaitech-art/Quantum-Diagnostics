"""
Network Diagnostics Panel
Network connectivity checks, IP info, and ping tests.
"""

import customtkinter as ctk
import threading

from src.diagnostics.network import (
    check_internet_connection,
    get_local_ip,
    get_hostname,
    ping_host,
    run_speed_test,
)


class NetworkPanel(ctk.CTkFrame):
    """Panel for network diagnostics."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self._build_ui()
        self._check_connection()

    def _build_ui(self):
        """Build the network panel layout."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="Network Diagnostics",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Check connectivity, IP configuration, and network performance",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w",
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Connection Status Card
        self.status_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        self.status_card.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.status_card.grid_columnconfigure(1, weight=1)

        self.conn_indicator = ctk.CTkLabel(
            self.status_card,
            text="●",
            font=ctk.CTkFont(size=24),
            text_color="#888888",
        )
        self.conn_indicator.grid(row=0, column=0, padx=(15, 5), pady=12)

        self.conn_status = ctk.CTkLabel(
            self.status_card,
            text="Checking connection...",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )
        self.conn_status.grid(row=0, column=1, padx=5, pady=12, sticky="w")

        # Network Info
        self.info_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        self.info_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.info_frame.grid_columnconfigure(1, weight=1)

        info_items = ["Local IP", "Hostname"]
        self.info_labels = {}

        for idx, item in enumerate(info_items):
            key_lbl = ctk.CTkLabel(
                self.info_frame,
                text=f"{item}:",
                font=ctk.CTkFont(size=12),
                text_color="#888888",
                anchor="w",
            )
            key_lbl.grid(row=idx, column=0, padx=15, pady=5, sticky="w")

            val_lbl = ctk.CTkLabel(
                self.info_frame,
                text="--",
                font=ctk.CTkFont(size=12),
                anchor="w",
            )
            val_lbl.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            self.info_labels[item] = val_lbl

        # Tools section
        tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame.grid(row=4, column=0, padx=15, pady=10, sticky="new")
        tools_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Ping test
        self.ping_entry = ctk.CTkEntry(
            tools_frame,
            placeholder_text="Host to ping (e.g. 8.8.8.8)",
            height=35,
            corner_radius=8,
        )
        self.ping_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.ping_btn = ctk.CTkButton(
            tools_frame,
            text="Ping",
            width=80,
            height=35,
            corner_radius=8,
            command=self._run_ping,
        )
        self.ping_btn.grid(row=0, column=2, padx=5, pady=5)

        # Speed test button
        self.speed_btn = ctk.CTkButton(
            tools_frame,
            text="Run Speed Test",
            height=35,
            corner_radius=8,
            fg_color="#3D5AFE",
            hover_color="#304FFE",
            command=self._run_speed_test,
        )
        self.speed_btn.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # Results area
        self.result_text = ctk.CTkTextbox(
            self,
            height=150,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#1E1E30",
            corner_radius=8,
        )
        self.result_text.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

    def _check_connection(self):
        """Check internet connection in background."""
        def task():
            result = check_internet_connection()
            local_ip = get_local_ip()
            hostname = get_hostname()
            self.after(0, self._update_connection, result, local_ip, hostname)

        threading.Thread(target=task, daemon=True).start()

    def _update_connection(self, result, local_ip, hostname):
        """Update connection status display."""
        if result["connected"]:
            self.conn_indicator.configure(text_color="#00E676")
            self.conn_status.configure(text="Connected to Internet")
        else:
            self.conn_indicator.configure(text_color="#EF5350")
            self.conn_status.configure(text="No Internet Connection")

        self.info_labels["Local IP"].configure(text=local_ip)
        self.info_labels["Hostname"].configure(text=hostname)

    def _run_ping(self):
        """Run ping test."""
        host = self.ping_entry.get().strip() or "8.8.8.8"
        self.ping_btn.configure(state="disabled", text="...")
        self._append_result(f"Pinging {host}...\n")

        def task():
            result = ping_host(host, count=4)
            self.after(0, self._ping_done, result)

        threading.Thread(target=task, daemon=True).start()

    def _ping_done(self, result):
        """Handle ping completion."""
        self.ping_btn.configure(state="normal", text="Ping")
        if result["success"]:
            self._append_result(result["output"] + "\n")
        else:
            self._append_result(f"Ping failed: {result['message']}\n")

    def _run_speed_test(self):
        """Run internet speed test."""
        self.speed_btn.configure(state="disabled", text="Testing... (may take 30s)")
        self._append_result("Running speed test...\n")

        def task():
            result = run_speed_test()
            self.after(0, self._speed_done, result)

        threading.Thread(target=task, daemon=True).start()

    def _speed_done(self, result):
        """Handle speed test completion."""
        self.speed_btn.configure(state="normal", text="Run Speed Test")
        if result["success"]:
            text = (
                f"Speed Test Results:\n"
                f"  Download: {result['download_mbps']} Mbps\n"
                f"  Upload:   {result['upload_mbps']} Mbps\n"
                f"  Ping:     {result['ping_ms']} ms\n"
                f"  Server:   {result['server']}\n"
            )
        else:
            text = f"Speed test failed: {result['message']}\n"
        self._append_result(text)

    def _append_result(self, text):
        """Append text to results area."""
        self.result_text.configure(state="normal")
        self.result_text.insert("end", text)
        self.result_text.configure(state="disabled")
        self.result_text.see("end")
