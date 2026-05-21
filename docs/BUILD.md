# Build Instructions

## Running from source

```bash
python main.py
```

## Creating a Windows executable

Uses PyInstaller to bundle everything into a single `.exe`:

```bash
pip install pyinstaller

# build
pyinstaller --onefile --windowed --name "PCHealthTool" main.py
```

The executable will be in the `dist/` folder.

### Notes
- First build takes a while (1-2 min) — subsequent builds are faster.
- Windows Defender or other AV might flag the exe. This is a [known PyInstaller issue](https://pyinstaller.org/en/stable/when-things-go-wrong.html).
- The exe is self-contained — no Python installation needed on the target machine.
- File size will be ~30-50MB depending on installed packages.

## Creating a portable version

Same as above, but you can zip the `dist/` folder and distribute it:

```
PCHealthTool-portable/
├── PCHealthTool.exe
└── reports/          (create this folder alongside the exe)
```
