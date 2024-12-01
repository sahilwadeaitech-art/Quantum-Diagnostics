"""
Network diagnostics panel — connection status, ping, speed test.
"""

import customtkinter as ctk
import threading

from src.ui.theme import COLORS, FONT, SPACING, CARD_STYLE, BUTTON_PRIMARY, INPUT_STYLE
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
            font=ctk.CTkFont(size=FONT["heading_lg"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=SPACING["xl"], pady=(SPACING["xl"], 2), sticky="w")

        ctk.CTkLabel(
            self, text="Connectivity status, ping test, and speed diagnostics",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        ).grid(row=1, column=0, padx=SPACING["xl"], pady=(0, SPACING["lg"]), sticky="w")

        # -- connection status card --
        status_card = ctk.CTkFrame(self, **CARD_STYLE)
        status_card.grid(row=2, column=0, padx=SPACING["xl"], pady=(0, SPACING["sm"]), sticky="ew")
        status_card.grid_columnconfigure(1, weight=1)

        self.indicator = ctk.CTkLabel(
            status_card, text="●",
            font=ctk.CTkFont(size=16), text_color=COLORS["text_muted"]
        )
        self.indicator.grid(row=0, column=0, padx=(16, 6), pady=14)

        self.conn_lbl = ctk.CTkLabel(
            status_card, text="Checking connectivity...",
            font=ctk.CTkFont(size=FONT["heading_sm"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        )
        self.conn_lbl.grid(row=0, column=1, padx=4, pady=14, sticky="w")

        # -- IP info card --
        info_card = ctk.CTkFrame(self, **CARD_STYLE)
        info_card.grid(row=3, column=0, padx=SPACING["xl"], pady=(0, SPACING["md"]), sticky="ew")
        info_card.grid_columnconfigure(1, weight=1)

        self.ip_lbl = ctk.CTkLabel(
            info_card, text="--",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        )
        self.host_lbl = ctk.CTkLabel(
            info_card, text="--",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        )

        ctk.CTkLabel(
            info_card, text="Local IP",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_muted"], anchor="w"
        ).grid(row=0, column=0, padx=16, pady=(12, 2), sticky="w")
        self.ip_lbl.grid(row=0, column=1, padx=10, pady=(12, 2), sticky="w")

        ctk.CTkLabel(
            info_card, text="Hostname",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_muted"], anchor="w"
        ).grid(row=1, column=0, padx=16, pady=(2, 12), sticky="w")
        self.host_lbl.grid(row=1, column=1, padx=10, pady=(2, 12), sticky="w")

        # -- tools row --
        tools = ctk.CTkFrame(self, fg_color="transparent")
        tools.grid(row=4, column=0, padx=SPACING["lg"], pady=0, sticky="new")
        tools.grid_columnconfigure(0, weight=1)

        # ping row
        ping_row = ctk.CTkFrame(tools, fg_color="transparent")
        ping_row.grid(row=0, column=0, sticky="ew")
        ping_row.grid_columnconfigure(0, weight=1)

        self.ping_entry = ctk.CTkEntry(
            ping_row, placeholder_text="Host to ping (e.g. 8.8.8.8)",
            font=ctk.CTkFont(size=FONT["body_sm"]), **INPUT_STYLE
        )
        self.ping_entry.grid(row=0, column=0, padx=(SPACING["xs"], SPACING["sm"]), pady=SPACING["xs"], sticky="ew")

        self.ping_btn = ctk.CTkButton(
            ping_row, text="Ping", width=70,
            font=ctk.CTkFont(size=FONT["body_sm"]),
            command=self._ping, **BUTTON_PRIMARY
        )
        self.ping_btn.grid(row=0, column=1, padx=SPACING["xs"], pady=SPACING["xs"])

        # speed test button
        self.speed_btn = ctk.CTkButton(
            tools, text="▶  Run Speed Test",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            command=self._speed_test, **BUTTON_PRIMARY
        )
        self.speed_btn.grid(row=1, column=0, padx=SPACING["xs"], pady=SPACING["xs"], sticky="ew")

        # -- output area --
        self.output = ctk.CTkTextbox(
            self, height=140,
            font=ctk.CTkFont(family="Consolas", size=FONT["caption"]),
            fg_color=COLORS["bg_input"], corner_radius=8,
            text_color=COLORS["text_secondary"],
            scrollbar_button_color=COLORS["border"],
        )
        self.output.grid(row=5, column=0, padx=SPACING["xl"], pady=(SPACING["sm"], SPACING["lg"]), sticky="ew")

    # ------------------------------------------------------------------ logic

    def _check_conn(self):
        def task():
            r = check_internet_connection()
            ip = get_local_ip()
            host = get_hostname()
            self.after(0, self._show_conn, r, ip, host)
        threading.Thread(target=task, daemon=True).start()

    def _show_conn(self, r, ip, host):
        if r["connected"]:
            self.indicator.configure(text_color=COLORS["success"])
            self.conn_lbl.configure(text="Connected to Internet", text_color=COLORS["success"])
        else:
            self.indicator.configure(text_color=COLORS["danger"])
            self.conn_lbl.configure(text="No Connection", text_color=COLORS["danger"])
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
        self.speed_btn.configure(state="normal", text="▶  Run Speed Test")
        if r["success"]:
            self._out(
                f"  ↓ Download: {r['download_mbps']} Mbps\n"
                f"  ↑ Upload:   {r['upload_mbps']} Mbps\n"
                f"  ⏱ Ping:     {r['ping_ms']} ms\n"
            )
        else:
            self._out(f"Failed: {r['message']}\n")

    def _out(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.configure(state="disabled")
        self.output.see("end")
