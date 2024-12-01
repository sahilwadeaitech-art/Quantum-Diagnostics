"""
CMD Tools panel — quick-access buttons for common system commands.
"""

import customtkinter as ctk
import threading

from src.ui.theme import COLORS, FONT, SPACING, CARD_STYLE, BUTTON_PRIMARY, BUTTON_SECONDARY
from src.diagnostics.cmd_utilities import (
    flush_dns, get_ipconfig, get_system_info_cmd, get_tasklist,
)


class CmdToolsPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="Quick Utilities",
            font=ctk.CTkFont(size=FONT["heading_lg"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=SPACING["xl"], pady=(SPACING["xl"], 2), sticky="w")

        ctk.CTkLabel(
            self, text="Run common diagnostic commands with one click",
            font=ctk.CTkFont(size=FONT["body_sm"]),
            text_color=COLORS["text_secondary"], anchor="w"
        ).grid(row=1, column=0, padx=SPACING["xl"], pady=(0, SPACING["lg"]), sticky="w")

        # command buttons row
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.grid(row=2, column=0, padx=SPACING["lg"], pady=(0, SPACING["md"]), sticky="ew")
        btn_row.grid_columnconfigure((0, 1, 2, 3), weight=1)

        cmds = [
            ("Flush DNS", self._flush_dns),
            ("IP Config", self._ipconfig),
            ("System Info", self._sysinfo),
            ("Task List", self._tasklist),
        ]
        self._buttons = {}
        for i, (label, handler) in enumerate(cmds):
            style = BUTTON_PRIMARY if i == 0 else BUTTON_SECONDARY
            btn = ctk.CTkButton(
                btn_row, text=label,
                font=ctk.CTkFont(size=FONT["body_sm"]),
                command=handler, **style
            )
            btn.grid(row=0, column=i, padx=SPACING["xs"], pady=SPACING["xs"], sticky="ew")
            self._buttons[label] = btn

        # output card
        out_card = ctk.CTkFrame(self, **CARD_STYLE)
        out_card.grid(row=3, column=0, padx=SPACING["xl"], pady=0, sticky="nsew")
        out_card.grid_columnconfigure(0, weight=1)
        out_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            out_card, text="Command Output",
            font=ctk.CTkFont(size=FONT["heading_sm"], weight="bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, padx=16, pady=(14, 6), sticky="w")

        self.output = ctk.CTkTextbox(
            out_card,
            font=ctk.CTkFont(family="Consolas", size=FONT["caption"]),
            fg_color=COLORS["bg_input"], corner_radius=8,
            text_color=COLORS["text_secondary"],
            scrollbar_button_color=COLORS["border"],
        )
        self.output.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")

        # clear button
        ctk.CTkButton(
            self, text="Clear Output", width=90,
            font=ctk.CTkFont(size=FONT["caption"]),
            fg_color=COLORS["bg_card"], hover_color=COLORS["bg_card_hover"],
            border_width=1, border_color=COLORS["border"],
            text_color=COLORS["text_muted"], height=28, corner_radius=6,
            command=self._clear
        ).grid(row=4, column=0, padx=SPACING["xl"], pady=(SPACING["sm"], SPACING["lg"]), sticky="w")

    # ------------------------------------------------------------------ logic

    def _exec(self, label, func):
        btn = self._buttons.get(label)
        if btn:
            btn.configure(state="disabled")
        self._write(f"\n{'─' * 44}\n  {label}\n{'─' * 44}\n\n")
        def task():
            r = func()
            self.after(0, self._done, label, r)
        threading.Thread(target=task, daemon=True).start()

    def _done(self, label, r):
        btn = self._buttons.get(label)
        if btn:
            btn.configure(state="normal")
        self._write(r["output"] + "\n" if r["success"] else f"Error: {r['output']}\n")

    def _flush_dns(self):
        self._exec("Flush DNS", flush_dns)

    def _ipconfig(self):
        self._exec("IP Config", get_ipconfig)

    def _sysinfo(self):
        self._exec("System Info", get_system_info_cmd)

    def _tasklist(self):
        self._exec("Task List", get_tasklist)

    def _write(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.configure(state="disabled")
        self.output.see("end")

    def _clear(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")
