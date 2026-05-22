"""
Entry point. Run this to launch the app.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.app import App


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
