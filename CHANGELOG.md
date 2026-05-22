# Changelog

## v1.2.0 (2025-01-12)

- Renamed project to "Quantum Diagnostics" (was "PC Health Diagnosis Tool")
- Updated sidebar branding and window title
- Rewrote README properly
- Added SECURITY.md
- Fixed nav button alignment on smaller screens
- Fixed footer padding issue in sidebar

## v1.1.0 (2024-12-28)

- Added real-time network speed (download/upload delta calculation)
- Battery card now shows estimated time remaining
- Dashboard hero card shows CPU/RAM/Disk score breakdown chips
- Report export includes storage partition details now
- Tweaked health score weights (CPU 35%, RAM 35%, Disk 30%)
- Performance panel refreshes every 2s instead of 5s
- Cleanup panel shows file count before you confirm deletion
- Fixed crash when psutil can't read certain partitions
- Fixed network panel hanging with no internet
- Fixed uptime going negative after sleep/hibernate

## v1.0.0 (2024-12-15)

Initial working version.

- Dashboard with health score
- System info panel (CPU, RAM, OS, storage)
- Live performance monitoring
- Temp file cleanup + recycle bin + browser cache
- Network diagnostics (ping, connectivity, speed test)
- CMD tools (ipconfig, systeminfo, tasklist, DNS flush)
- Report export (.txt)
- Dark mode UI with sidebar nav

Known issues:
- Speed test is slow/unreliable sometimes
- Some temp files can't be deleted if they're locked by other processes
