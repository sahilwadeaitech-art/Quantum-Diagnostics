# PC Health Diagnosis Tool

A lightweight desktop utility for checking system health, monitoring resources, and doing basic PC maintenance. Built with Python and CustomTkinter.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)

---

## What it does

This tool gives you a quick overview of your PC's condition without needing to dig through multiple Windows settings panels. It's meant to be a simple "open it up and see how things are" utility.

**Main use cases:**
- Check if your system is healthy at a glance (health score)
- Monitor CPU, RAM, and disk usage in real-time
- Run quick network checks (ping, connectivity, speed test)
- Clean up temp files to free disk space
- Export a system report for troubleshooting

---

## Features

| Feature | Description |
|---------|-------------|
| **Dashboard** | Health score (0-100) with quick resource stats |
| **System Info** | CPU, RAM, OS, storage details in one view |
| **Performance Monitor** | Live-updating resource meters (2s refresh) |
| **Cleanup** | Delete temp files, empty recycle bin, clear browser cache |
| **Network** | Connection check, local IP, ping test, speed test |
| **CMD Tools** | One-click buttons for ipconfig, systeminfo, tasklist, flush DNS |
| **Report Export** | Save a .txt report with all system data |

---

## Screenshots

> Screenshots will be added once the UI is tested across different resolutions.

---

## Installation

**Requirements:** Python 3.8+

```bash
# clone the repo
git clone https://github.com/sahilwadeaitech-art/pc-health-diagnosis-tool.git
cd pc-health-diagnosis-tool

# (optional) create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# install dependencies
pip install -r requirements.txt

# run
python main.py
```

---

## Building an executable

If you want a standalone .exe (no Python needed):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PCHealthTool" main.py
```

Output goes to `dist/`. Note: antivirus software sometimes flags PyInstaller executables as false positives.

---

## Project structure

```
pc-health-diagnosis-tool/
├── src/
│   ├── ui/
│   │   ├── app.py            # main window + sidebar
│   │   └── panels/           # each tab is a separate panel
│   ├── services/
│   │   ├── system_info.py    # hardware/OS data
│   │   └── health_score.py   # score calculation
│   ├── monitoring/
│   │   └── performance.py    # live metrics tracking
│   ├── diagnostics/
│   │   ├── network.py        # connectivity + speed
│   │   └── cmd_utilities.py  # safe command wrappers
│   ├── cleanup/
│   │   └── temp_cleaner.py   # temp file operations
│   └── utils/
│       ├── helpers.py         # misc utility functions
│       └── report_export.py   # report generation
├── assets/                    # icons, screenshots, themes
├── reports/                   # generated reports go here
├── main.py                    # entry point
├── requirements.txt
└── README.md
```

---

## Tech stack

- **Python 3.8+** — core language
- **CustomTkinter** — modern-looking tkinter wrapper (dark mode)
- **psutil** — cross-platform system monitoring
- **subprocess** — for running system commands
- **socket** — network diagnostics
- **speedtest-cli** — internet speed testing (optional)

---

## Known limitations

- Primarily built for Windows. Linux works for most features but some CMD tools and recycle bin features are Windows-specific.
- Speed test depends on `speedtest-cli` which can occasionally fail or give inconsistent results.
- Browser cache clearing requires browsers to be closed first.
- Health score is a rough heuristic, not a comprehensive system diagnostic.
- This is a monitoring/diagnostic tool — it doesn't modify system settings or optimize anything.

---

## Roadmap

Things I'd like to add eventually:

- [ ] Per-core CPU graphs (matplotlib)
- [ ] Startup time tracking
- [ ] Scheduled/automatic health checks
- [ ] PDF report export
- [ ] Dark/light theme toggle
- [ ] Process manager (kill high-resource tasks)
- [ ] System optimization suggestions
- [ ] Notification alerts for high usage

---

## Contributing

This is a personal project but feedback and suggestions are welcome. Feel free to open an issue.

---

## License

MIT — see [LICENSE](LICENSE)
