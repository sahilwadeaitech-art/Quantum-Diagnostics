"""
Network diagnostics panel — connection status, ping, speed test.
"""

import customtkinter as ctk
import threading

from src.diagnostics.network import (
    check_internet_connection, get_local_ip,
    get_hostname, ping_host, run_speed_test,
)


class NetworkPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._build_ui()
        self._check_conn()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="Network Diagnostics",
            font=ctk.CTkFont(size=22, weight="bold"), anchor="w"
        ).grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        ctk.CTkLabel(
            self, text="Connectivity, IP info, and speed testing",
            font=ctk.CTkFont(size=12), text_color="#888888", anchor="w"
        ).grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # status card
        status = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        status.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        status.grid_columnconfigure(1, weight=1)

        self.indicator = ctk.CTkLabel(status, text="●", font=ctk.CTkFont(size=24), text_color="#888888")
        self.indicator.grid(row=0, column=0, padx=(15, 5), pady=12)
        self.conn_lbl = ctk.CTkLabel(
            status, text="Checking...",
            font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
        )
        self.conn_lbl.grid(row=0, column=1, padx=5, pady=12, sticky="w")

        # IP info
        info = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        info.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        info.grid_columnconfigure(1, weight=1)

        self.ip_lbl = ctk.CTkLabel(info, text="--", font=ctk.CTkFont(size=12), anchor="w")
        self.host_lbl = ctk.CTkLabel(info, text="--", font=ctk.CTkFont(size=12), anchor="w")

        ctk.CTkLabel(info, text="Local IP:", font=ctk.CTkFont(size=12), text_color="#888888", anchor="w").grid(row=0, column=0, padx=15, pady=5, sticky="w")
        self.ip_lbl.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(info, text="Hostname:", font=ctk.CTkFont(size=12), text_color="#888888", anchor="w").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.host_lbl.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # tools
        tools = ctk.CTkFrame(self, fg_color="transparent")
        tools.grid(row=4, column=0, padx=15, pady=10, sticky="new")
        tools.grid_columnconfigure((0, 1, 2), weight=1)

        self.ping_entry = ctk.CTkEntry(tools, placeholder_text="Host (e.g. 8.8.8.8)", height=35, corner_radius=8)
        self.ping_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.ping_btn = ctk.CTkButton(tools, text="Ping", width=80, height=35, corner_radius=8, command=self._ping)
        self.ping_btn.grid(row=0, column=2, padx=5, pady=5)

        self.speed_btn = ctk.CTkButton(
            tools, text="Speed Test", height=35, corner_radius=8,
            fg_color="#3D5AFE", hover_color="#304FFE", command=self._speed_test
        )
        self.speed_btn.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # output
        self.output = ctk.CTkTextbox(
            self, height=150, font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#1E1E30", corner_radius=8
        )
        self.output.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

    def _check_conn(self):
        def task():
            r = check_internet_connection()
            ip = get_local_ip()
            host = get_hostname()
            self.after(0, self._show_conn, r, ip, host)
        threading.Thread(target=task, daemon=True).start()

    def _show_conn(self, r, ip, host):
        if r["connected"]:
            self.indicator.configure(text_color="#00E676")
            self.conn_lbl.configure(text="Connected")
        else:
            self.indicator.configure(text_color="#EF5350")
            self.conn_lbl.configure(text="No Connection")
        self.ip_lbl.configure(text=ip)
        self.host_lbl.configure(text=host)

    def _ping(self):
        host = self.ping_entry.get().strip() or "8.8.8.8"
        self.ping_btn.configure(state="disabled", text="...")
        self._out(f"Pinging {host}...\n")
        def task():
            r = ping_host(host)
            self.after(0, self._ping_done, r)
        threading.Thread(target=task, daemon=True).start()

    def _ping_done(self, r):
        self.ping_btn.configure(state="normal", text="Ping")
        self._out(r["output"] + "\n" if r["success"] else f"Failed: {r['message']}\n")

    def _speed_test(self):
        self.speed_btn.configure(state="disabled", text="Testing (~30s)...")
        self._out("Running speed test...\n")
        def task():
            r = run_speed_test()
            self.after(0, self._speed_done, r)
        threading.Thread(target=task, daemon=True).start()

    def _speed_done(self, r):
        self.speed_btn.configure(state="normal", text="Speed Test")
        if r["success"]:
            self._out(f"  Download: {r['download_mbps']} Mbps\n  Upload: {r['upload_mbps']} Mbps\n  Ping: {r['ping_ms']} ms\n")
        else:
            self._out(f"Failed: {r['message']}\n")

    def _out(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.configure(state="disabled")
        self.output.see("end")
