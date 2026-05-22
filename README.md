# Quantum Diagnostics

Quick system health checker + diagnostics tool for Windows. Gives you a health score, live resource monitoring, network checks, and cleanup tools in one dark-themed UI.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-1A1A2E?style=flat)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Windows%20%7C%20Linux-supported-lightgrey.svg)

---

## Why I made this

I got tired of opening Task Manager, checking disk space in Settings, running `ipconfig` manually, and using three different apps to clean temp files. So I built a single dashboard that shows me everything at a glance.

It's not trying to be a full-blown system optimizer — it just monitors, reports, and cleans up the obvious stuff.

---

## What it does

- **Dashboard** — health score (0–100) based on CPU/RAM/disk usage, with quick resource cards
- **System Info** — CPU, RAM, OS, storage partitions, boot time
- **Performance** — live monitoring (refreshes every 2s), color-coded bars
- **Cleanup** — scan + delete temp files, empty recycle bin, clear browser caches
- **Network** — connectivity check, ping test, speed test
- **CMD Tools** — one-click ipconfig, systeminfo, tasklist, flush DNS
- **Report** — export a .txt snapshot of your system state

---

## Screenshots

| Dashboard | Performance |
|:---------:|:-----------:|
| ![](assets/screenshots/dashboard.png) | ![](assets/screenshots/performance.png) |

| Network | Cleanup |
|:-------:|:-------:|
| ![](assets/screenshots/network.png) | ![](assets/screenshots/cleanup.png) |

---

## Setup

Needs Python 3.8+. Tested mainly on Windows 10/11.

```bash
git clone https://github.com/sahilwadeaitech-art/Quantum-Diagnostics.git
cd Quantum-Diagnostics

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
python main.py
```

### Building an .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "QuantumDiagnostics" main.py
```

More details in [docs/BUILD.md](docs/BUILD.md).

---

## Project structure

```
src/
├── ui/
│   ├── theme.py           # colors, fonts, component styles
│   ├── app.py             # main window + sidebar
│   └── panels/            # one file per tab
├── services/
│   ├── system_info.py     # hardware/OS data (psutil + platform)
│   └── health_score.py    # weighted scoring logic
├── monitoring/
│   └── performance.py     # live metrics, network speed calc
├── diagnostics/
│   ├── network.py         # ping, connectivity, speed test
│   └── cmd_utilities.py   # subprocess wrappers for common commands
├── cleanup/
│   └── temp_cleaner.py    # temp files, recycle bin, browser cache
└── utils/
    ├── helpers.py
    └── report_export.py   # .txt report generation
```

---

## Stack

- **Python 3.8+**
- **CustomTkinter** — dark mode UI
- **psutil** — system monitoring
- **speedtest-cli** — internet speed (optional, can be slow)

---

## Limitations

- Primarily Windows. Linux works for most things but recycle bin + CMD tools are Windows-only.
- Speed test can take a while or fail on unstable connections.
- Health score is a rough heuristic — not a replacement for proper diagnostics.
- Doesn't modify any system settings. Read-only monitoring + cleanup only.

---

## What's next

- [ ] Per-core CPU graphs
- [ ] PDF export option
- [ ] Process manager (view + kill tasks)
- [ ] Light theme option
- [ ] System notifications for high resource usage
- [ ] Settings file (remember preferences between runs)

---

## License

MIT
