# Security

## What this app does and doesn't do

This is a local desktop tool. It reads system info through psutil and runs a few safe subprocess commands (ipconfig, systeminfo, etc). It doesn't:

- Connect to any server (except the optional speed test)
- Collect or send any personal data
- Modify system settings or registry
- Need admin privileges for most features
- Run anything in the background

The cleanup module only deletes temp files, recycle bin contents, and browser cache — and shows you what it's going to remove before doing it.

## Reporting issues

If you find a security problem, open a GitHub issue or reach out directly. I'll look into it.

## Dependencies

- `customtkinter` — UI only, no network
- `psutil` — reads system metrics (read-only)
- `speedtest-cli` — optional, makes outbound connections for speed test
- `matplotlib` — charts, no network
