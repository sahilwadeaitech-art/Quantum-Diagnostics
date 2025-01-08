# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.2.x   | ✅ Current |
| 1.0.x   | ⚠️ Limited |
| < 1.0   | ❌ No      |

## Scope

Quantum Diagnostics is a **local desktop utility** that reads system information through standard OS APIs (psutil, platform, subprocess). It does not:

- Connect to external servers or APIs (except optional speedtest)
- Collect, store, or transmit personal data
- Modify system configuration or registry
- Require elevated/admin privileges for core functionality
- Install background services or daemons

The cleanup module deletes only:
- Temporary files from standard temp directories
- Recycle bin contents (with user confirmation)
- Browser cache files from known locations

## Reporting a Vulnerability

If you discover a security concern in this project:

1. **Do not open a public issue** for security vulnerabilities
2. Reach out via GitHub Security Advisory or private message
3. Include steps to reproduce, potential impact, and suggested fix if possible

### Response timeline:
- Acknowledgment within 48 hours
- Assessment and fix within 7 days for critical issues
- Public disclosure after a patch is available

## Design Principles

- **Read-only by default** — the app monitors and reports, it doesn't "optimize" or modify system settings
- **Transparent operations** — cleanup actions show exactly what will be deleted before proceeding
- **No network required** — core functionality works entirely offline
- **Safe subprocess usage** — CMD tool wrappers use fixed commands only, no user-supplied input in shell calls

## Dependencies

| Package | Purpose | Risk Notes |
|---------|---------|-----------|
| customtkinter | UI framework | No network, display only |
| psutil | System metrics | Read-only OS API calls |
| speedtest-cli | Internet speed test | Optional, makes outbound connections |
| matplotlib | Charts (planned) | No network |

All dependencies are pinned in `requirements.txt` and should be reviewed before installation.
