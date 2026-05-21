"""
CMD Tools Panel
Quick access to common system command-line utilities.
"""

import customtkinter as ctk
import threading

from src.diagnostics.cmd_utilities import (
    flush_dns,
    get_ipconfig,
    get_system_info_cmd,
    get_tasklist,
)


class CmdToolsPanel(ctk.CTkFrame):
    """Panel for quick CMD utility access."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._build_ui()

    def _build_ui(self):
        """Build the CMD tools layout."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="CMD Utilities",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Quick access to common system commands",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w",
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Buttons grid
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Command buttons
        commands = [
            ("Flush DNS", self._cmd_flush_dns, "#3D5AFE"),
            ("IP Config", self._cmd_ipconfig, "#3D5AFE"),
            ("System Info", self._cmd_sysinfo, "#3D5AFE"),
            ("Task List", self._cmd_tasklist, "#3D5AFE"),
        ]

        self._cmd_buttons = {}
        for idx, (label, command, color) in enumerate(commands):
            btn = ctk.CTkButton(
                btn_frame,
                text=label,
                height=40,
                corner_radius=8,
                fg_color=color,
                hover_color="#304FFE",
                command=command,
            )
            btn.grid(row=0, column=idx, padx=4, pady=5, sticky="ew")
            self._cmd_buttons[label] = btn

        # Output area
        output_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#252540")
        output_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)

        output_title = ctk.CTkLabel(
            output_frame,
            text="Command Output",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4A9EFF",
            anchor="w",
        )
        output_title.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

        self.output_text = ctk.CTkTextbox(
            output_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#1E1E30",
            corner_radius=8,
        )
        self.output_text.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="nsew")

        # Clear button
        clear_btn = ctk.CTkButton(
            self,
            text="Clear Output",
            width=100,
            height=30,
            corner_radius=8,
            fg_color="#444444",
            hover_color="#555555",
            command=self._clear_output,
        )
        clear_btn.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="w")

    def _run_command(self, label, func):
        """Run a command in background and display output."""
        btn = self._cmd_buttons.get(label)
        if btn:
            btn.configure(state="disabled")

        self._append_output(f"\n{'='*50}\n> Running: {label}\n{'='*50}\n\n")

        def task():
            result = func()
            self.after(0, self._command_done, label, result)

        threading.Thread(target=task, daemon=True).start()

    def _command_done(self, label, result):
        """Handle command completion."""
        btn = self._cmd_buttons.get(label)
        if btn:
            btn.configure(state="normal")

        if result["success"]:
            self._append_output(result["output"] + "\n")
        else:
            self._append_output(f"Error: {result['output']}\n")

    def _cmd_flush_dns(self):
        self._run_command("Flush DNS", flush_dns)

    def _cmd_ipconfig(self):
        self._run_command("IP Config", get_ipconfig)

    def _cmd_sysinfo(self):
        self._run_command("System Info", get_system_info_cmd)

    def _cmd_tasklist(self):
        self._run_command("Task List", get_tasklist)

    def _append_output(self, text):
        """Append text to output area."""
        self.output_text.configure(state="normal")
        self.output_text.insert("end", text)
        self.output_text.configure(state="disabled")
        self.output_text.see("end")

    def _clear_output(self):
        """Clear the output text area."""
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
