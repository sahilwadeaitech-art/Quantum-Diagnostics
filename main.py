"""
PC Health Diagnosis Tool
========================
A modern desktop utility for monitoring system health,
diagnosing performance issues, and performing basic maintenance.

Run this file to start the application:
    python main.py
"""

import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.app import App


def main():
    """Launch the PC Health Diagnosis Tool."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
