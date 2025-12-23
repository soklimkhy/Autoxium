# Autoxium

Autoxium is a tool that bridges the gap between a standard app and a hardware-interfacing tool, wrapping external binaries like ADB and scrcpy.

## Structure

- `assets/`: Binaries and static files. Place `adb.exe` and `scrcpy.exe` in `assets/bin/`.
- `src/autoxium/`: Main package.
- `src/autoxium/core/`: The "Engine" interacting with subprocesses.
- `src/autoxium/ui/`: UI components.

## Usage

Run the module:
```bash
python -m src.autoxium
```
Or install and run:
```bash
pip install .
autoxium
```
