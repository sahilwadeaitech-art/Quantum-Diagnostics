# PC Health Diagnosis Tool

A lightweight desktop utility built with Python and CustomTkinter that helps you monitor system health, diagnose performance issues, and perform basic PC maintenance tasks.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)

---

## Overview

PC Health Diagnosis Tool is a personal system utility that provides real-time performance monitoring, hardware information, network diagnostics, and cleanup tools — all in a clean, modern dark-mode interface.

I built this to have a quick way to check system health without opening multiple Windows tools or installing heavy bloatware. It's designed to be practical, fast, and easy to use.

---

## Features

- **System Dashboard** — Overall health score with quick stats at a glance
- **Hardware Information** — CPU, RAM, storage, and OS details in one place
- **Live Performance Monitoring** — Real-time CPU, RAM, disk, battery, and network usage
- **Health Score Calculator** — Weighted scoring system (Excellent / Good / Moderate / Poor)
- **Temp File Cleaner** — Remove temporary files, empty recycle bin, clear browser cache
- **Network Diagnostics** — Connectivity check, local IP, ping test, speed test
- **CMD Utilities** — Quick buttons for Flush DNS, ipconfig, systeminfo, tasklist
- **Report Export** — Generate a complete system health report as a text file

---

## Screenshots

> Screenshots will be added after initial testing on Windows.

| Dashboard | Performance | System Info |
|-----------|-------------|-------------|
| *coming soon* | *coming soon* | *coming soon* |

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.8+ | Core language |
| CustomTkinter | Modern UI framework |
| psutil | System/hardware monitoring |
| subprocess | CMD utility execution |
| socket | Network diagnostics |
| threading | Non-blocking UI operations |
| matplotlib | Charts (optional) |
| speedtest-cli | Internet speed testing (optional) |

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sahilwadeaitech-art/pc-health-diagnosis-tool.git
cd pc-health-diagnosis-tool
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

---

## Usage

Launch the app and use the sidebar to navigate between panels:

- **Dashboard** — Check your overall system health score and quick stats
- **System Info** — View detailed hardware and OS information
- **Performance** — Monitor live resource usage (updates every 2 seconds)
- **Cleanup** — Scan and remove temp files, empty recycle bin
- **Network** — Test connectivity, run ping, check speed
- **CMD Tools** — Run common diagnostic commands with one click
- **Export Report** — Generate a text report of your system's current state

---

## Project Structure

```
pc-health-diagnosis-tool/
├── assets/
│   ├── icons/
│   ├── screenshots/
│   └── themes/
├── docs/
├── reports/              # Generated reports saved here
├── src/
│   ├── ui/
│   │   ├── app.py       # Main window and navigation
│   │   └── panels/      # Individual UI panels
│   ├── services/
│   │   ├── system_info.py
│   │   └── health_score.py
│   ├── monitoring/
│   │   └── performance.py
│   ├── diagnostics/
│   │   ├── network.py
│   │   └── cmd_utilities.py
│   ├── cleanup/
│   │   └── temp_cleaner.py
│   └── utils/
│       ├── report_export.py
│       └── helpers.py
├── main.py              # Entry point
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Building an Executable

You can package the app as a standalone `.exe` using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PCHealthTool" main.py
```

The executable will be in the `dist/` folder.

---

## Future Improvements

- [ ] Per-core CPU usage graphs with matplotlib
- [ ] System startup time tracking
- [ ] Scheduled health checks
- [ ] Plugin architecture for custom diagnostics
- [ ] Export reports as PDF
- [ ] Dark/light theme toggle
- [ ] System optimization suggestions
- [ ] Process manager (kill high-resource tasks)
- [ ] Notification alerts for high resource usage

---

## Contributing

This is a personal project, but suggestions and feedback are welcome. Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
