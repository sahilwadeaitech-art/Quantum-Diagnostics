"""
CMD Tools panel — quick-access buttons for common system commands.
"""

import customtkinter as ctk
import threading

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
            self, text="CMD Utilities",
            font=ctk.CTkFont(size=22, weight="bold"), anchor="w"
        ).grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        ctk.CTkLabel(
            self, text="Run common diagnostic commands with one click",
            font=ctk.CTkFont(size=12), text_color="#888888", anchor="w"
        ).grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        cmds = [
            ("Flush DNS", self._flush_dns),
            ("IP Config", self._ipconfig),
            ("System Info", self._sysinfo),
            ("Task List", self._tasklist),
        ]
        self._buttons = {}
        for i, (label, handler) in enumerate(cmds):
            btn = ctk.CTkButton(
                btn_frame, text=label, height=40, corner_radius=8,
                fg_color="#3D5AFE", hover_color="#304FFE", command=handler
            )
            btn.grid(row=0, column=i, padx=4, pady=5, sticky="ew")
            self._buttons[label] = btn

        # output
        out_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        out_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        out_frame.grid_columnconfigure(0, weight=1)
        out_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            out_frame, text="Output",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4A9EFF", anchor="w"
        ).grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

        self.output = ctk.CTkTextbox(
            out_frame, font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#1E1E30", corner_radius=8
        )
        self.output.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="nsew")

        ctk.CTkButton(
            self, text="Clear", width=80, height=30, corner_radius=8,
            fg_color="#444444", hover_color="#555555", command=self._clear
        ).grid(row=4, column=0, padx=20, pady=(0, 10), sticky="w")

    def _exec(self, label, func):
        btn = self._buttons.get(label)
        if btn:
            btn.configure(state="disabled")
        self._write(f"\n{'='*40}\n> {label}\n{'='*40}\n\n")
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
