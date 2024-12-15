# Changelog

All notable changes to Quantum Diagnostics.

---

## [1.2.0] - 2025-01-12

### Added
- SECURITY.md with dependency audit and reporting guidelines
- Screenshot placeholders in assets/screenshots/
- Repository topics and description metadata

### Changed
- Rebranded from "PC Health Diagnosis Tool" to "Quantum Diagnostics"
- Updated sidebar branding and window title
- README fully redesigned with feature table, architecture diagram, screenshot grid
- Bumped version display across UI

### Fixed
- Sidebar nav button alignment on smaller resolutions
- Footer label padding inconsistency

---

## [1.1.0] - 2024-12-28

### Added
- Network speed delta calculation (shows real-time download/upload)
- Battery time remaining estimate in dashboard
- Score breakdown chips (CPU/RAM/Disk) on hero card
- Export report now includes storage partition details

### Changed
- Improved health score weighting (CPU 35%, RAM 35%, Disk 30%)
- Performance panel refresh interval reduced to 2s
- Cleanup panel shows file count before deletion
- Better error handling in speed test fallback

### Fixed
- Crash when psutil can't access certain disk partitions
- Network panel hanging when no internet connection
- Uptime display showing negative values after sleep/hibernate

---

## [1.0.0] - 2024-12-15

### Added
- System dashboard with weighted health score (Excellent/Good/Moderate/Poor)
- Detailed hardware info panel (CPU, RAM, storage, OS)
- Live performance monitoring with 2-second refresh
- Temp file scanner and cleaner
- Recycle bin and browser cache cleanup
- Network diagnostics (connectivity check, ping, speed test)
- CMD utilities (ipconfig, systeminfo, tasklist, flush DNS)
- Export system report as .txt file
- Dark mode UI with sidebar navigation
- Custom theme system (src/ui/theme.py)

### Known Issues
- Speed test can be slow depending on network conditions
- Some temp files may be locked by running processes
- Recycle bin cleanup is Windows-only
