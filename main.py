"""
PC Health Diagnosis Tool - Entry Point
Run this to launch the application.
"""

import sys
import os

# make sure we can import from src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.app import App


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
