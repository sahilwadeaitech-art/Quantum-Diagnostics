"""
System Information Panel
Displays detailed hardware and OS information.
"""

import customtkinter as ctk
import threading

from src.services.system_info import get_full_system_info


class SystemInfoPanel(ctk.CTkFrame):
    """Panel showing detailed system information."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()
        self._load_data()

    def _build_ui(self):
        """Build the system info layout."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="System Information",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Detailed hardware and operating system details",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w",
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Scrollable content area
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.scroll_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Loading indicator
        self.loading_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Loading system information...",
            font=ctk.CTkFont(size=13),
            text_color="#888888",
        )
        self.loading_label.grid(row=0, column=0, pady=20)

    def _load_data(self):
        """Load system info in background."""
        thread = threading.Thread(target=self._fetch_data, daemon=True)
        thread.start()

    def _fetch_data(self):
        """Fetch system info and update UI."""
        try:
            info = get_full_system_info()
            self.after(0, self._display_info, info)
        except Exception as e:
            self.after(0, lambda: self.loading_label.configure(text=f"Error: {e}"))

    def _display_info(self, info):
        """Display all system information in cards."""
        self.loading_label.destroy()
        row = 0

        # OS Info
        os_data = info["os"]
        row = self._add_section(row, "Operating System", [
            ("System", f"{os_data['system']} {os_data['release']}"),
            ("Version", os_data["version"]),
            ("Hostname", os_data["hostname"]),
            ("Username", os_data["username"]),
        ])

        # CPU Info
        cpu_data = info["cpu"]
        row = self._add_section(row, "Processor (CPU)", [
            ("Processor", cpu_data["processor"]),
            ("Architecture", cpu_data["architecture"]),
            ("Physical Cores", str(cpu_data["physical_cores"])),
            ("Logical Cores", str(cpu_data["logical_cores"])),
            ("Max Frequency", cpu_data["max_frequency"]),
            ("Current Frequency", cpu_data["current_frequency"]),
        ])

        # RAM Info
        ram_data = info["ram"]
        row = self._add_section(row, "Memory (RAM)", [
            ("Total", ram_data["total"]),
            ("Used", ram_data["used"]),
            ("Available", ram_data["available"]),
            ("Usage", f"{ram_data['percent_used']}%"),
        ])

        # Storage Info
        storage_items = []
        for disk in info["storage"]:
            storage_items.append(("Device", disk["device"]))
            storage_items.append(("Mount", disk["mountpoint"]))
            storage_items.append(("Total", disk["total"]))
            storage_items.append(("Free", disk["free"]))
            storage_items.append(("Usage", f"{disk['percent_used']}%"))
            storage_items.append(("", ""))  # Spacer between drives
        row = self._add_section(row, "Storage", storage_items)

        # Boot Time
        row = self._add_section(row, "System Uptime", [
            ("Last Boot", info["boot_time"]),
        ])

    def _add_section(self, start_row, title, items):
        """Add a section card with title and key-value pairs."""
        card = ctk.CTkFrame(self.scroll_frame, corner_radius=10, fg_color="#252540")
        card.grid(row=start_row, column=0, padx=5, pady=5, sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        # Section title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4A9EFF",
            anchor="w",
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(12, 8), sticky="w")

        # Key-value pairs
        for idx, (key, value) in enumerate(items):
            if not key and not value:
                continue  # Skip spacers

            key_lbl = ctk.CTkLabel(
                card,
                text=f"{key}:",
                font=ctk.CTkFont(size=12),
                text_color="#999999",
                anchor="w",
                width=130,
            )
            key_lbl.grid(row=idx + 1, column=0, padx=(15, 5), pady=2, sticky="w")

            val_lbl = ctk.CTkLabel(
                card,
                text=str(value),
                font=ctk.CTkFont(size=12),
                anchor="w",
                wraplength=400,
            )
            val_lbl.grid(row=idx + 1, column=1, padx=5, pady=2, sticky="w")

        # Bottom padding
        spacer = ctk.CTkLabel(card, text="")
        spacer.grid(row=len(items) + 1, column=0, pady=3)

        return start_row + 1
