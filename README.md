<div align="center">

# Quantum Diagnostics

**Modern PC health monitoring and diagnostics utility**

Built with Python & CustomTkinter — Dark Theme — Real-time Analytics

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-1a1a2e?style=flat-square)](https://github.com/TomSchimansky/CustomTkinter)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux-94a3b8?style=flat-square)]()
[![Release](https://img.shields.io/badge/Release-v1.2.0-3b82f6?style=flat-square)]()

</div>

---

## Overview

Quantum Diagnostics is a desktop system utility that gives you a quick, visual overview of your PC's health without digging through Windows settings panels. It monitors CPU, RAM, disk, battery, and network — provides a weighted health score — and includes cleanup tools and network diagnostics in one dark-mode interface.

I built this because I wanted a single dashboard that tells me how my machine is actually doing, with cleanup utilities I'd normally run through 3 different apps.

---

## Features

| Module | Description |
|--------|-------------|
| **Dashboard** | Weighted health score (0–100), resource cards with live progress bars, system overview |
| **System Info** | CPU specs, RAM details, OS info, storage partitions, boot time |
| **Performance** | Real-time CPU/RAM/disk/battery/network monitoring with 2s refresh |
| **Cleanup** | Temp file scanner, recycle bin cleaner, browser cache removal |
| **Network** | Connectivity check, ping diagnostics, internet speed test |
| **CMD Tools** | One-click wrappers for ipconfig, systeminfo, tasklist, DNS flush |
| **Report Export** | Generate timestamped .txt report with full system snapshot |

---

## Screenshots

<div align="center">

| Dashboard | Performance |
|:---------:|:-----------:|
| <img src="assets/screenshots/dashboard.png" width="420"> | <img src="assets/screenshots/performance.png" width="420"> |

| Network Diagnostics | Cleanup Tools |
|:-------------------:|:-------------:|
| <img src="assets/screenshots/network.png" width="420"> | <img src="assets/screenshots/cleanup.png" width="420"> |

</div>

> Screenshots from v1.2.0 on Windows 11. UI renders consistently across supported platforms.

---

## Getting Started

### Requirements

- Python 3.8+
- Windows 10/11 (primary) or Linux (partial support)

### Installation

```bash
git clone https://github.com/sahilwadeaitech-art/Quantum-Diagnostics.git
cd Quantum-Diagnostics

# virtual environment (recommended)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux

# install dependencies
pip install -r requirements.txt
```

### Running

```bash
python main.py
```

### Building Standalone .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "QuantumDiagnostics" main.py
```

See [docs/BUILD.md](docs/BUILD.md) for full packaging instructions.

---

## Architecture

```
Quantum-Diagnostics/
├── src/
│   ├── ui/
│   │   ├── theme.py              # design system (colors, typography, spacing)
│   │   ├── app.py                # main window + sidebar navigation
│   │   └── panels/               # each tab as a separate module
│   │       ├── dashboard.py
│   │       ├── system_info.py
│   │       ├── performance.py
│   │       ├── cleanup.py
│   │       ├── network.py
│   │       ├── cmd_tools.py
│   │       └── report.py
│   ├── services/
│   │   ├── system_info.py        # hardware/OS data via psutil
│   │   └── health_score.py       # weighted scoring algorithm
│   ├── monitoring/
│   │   └── performance.py        # live metrics + network speed delta
│   ├── diagnostics/
│   │   ├── network.py            # connectivity + speed test
│   │   └── cmd_utilities.py      # safe subprocess wrappers
│   ├── cleanup/
│   │   └── temp_cleaner.py       # temp/cache/recycle bin operations
│   └── utils/
│       ├── helpers.py
│       └── report_export.py
├── assets/
│   ├── icons/
│   ├── screenshots/
│   └── themes/
├── reports/                       # generated reports (gitignored)
├── docs/
│   └── BUILD.md
├── main.py                        # entry point
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.8+ |
| UI | CustomTkinter (dark mode) |
| System Data | psutil |
| Networking | socket, subprocess, speedtest-cli |
| Packaging | PyInstaller |

---

## Design System

The UI uses a custom theme defined in `src/ui/theme.py`:

- **Carbon-black base** with sapphire blue accent
- Layered depth system (base → sidebar → surface → card → elevated)
- Color-coded progress bars (green → amber → red based on load)
- Reusable component style dicts (`CARD_STYLE`, `BUTTON_PRIMARY`, etc.)
- Consistent typography scale and spacing rhythm

---

## Limitations

- Windows-focused — most features work on Linux, but recycle bin and CMD tools are Windows-specific
- Speed test uses `speedtest-cli` which can be slow or unreliable
- Health score is heuristic-based, not a comprehensive diagnostic
- Monitors and reports only — does not modify system settings or "optimize" anything
- No persistent storage between sessions

---

## Roadmap

- [ ] Per-core CPU usage graphs (matplotlib integration)
- [ ] PDF report export
- [ ] Light / dark theme toggle
- [ ] Process manager panel (view + kill high-resource tasks)
- [ ] Startup time tracking
- [ ] System notifications for sustained high usage
- [ ] Settings persistence (JSON config)
- [ ] Plugin architecture for custom diagnostics

---

## Contributing

This is a personal project, but feedback is welcome. Open an issue if you find a bug or have a feature suggestion.

---

## Author

**Sahil Wade** — building practical desktop utilities and system tools.

---

## License

MIT — see [LICENSE](LICENSE) for details.
