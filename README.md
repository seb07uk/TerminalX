# TerminalX

**A lightweight, extensible cross-platform shell written in pure Python.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-35.2-green.svg)](CHANGELOG)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

TerminalX is a fully-featured, cross-platform interactive shell implemented in a **single Python file** with zero external dependencies (stdlib only). It provides a built-in text editor, plugin system, package manager, developer tools, session management, and over 100 built-in commands — all portable and self-contained.

> **Author:** Sebastian Januchowski — [github.com/polsoft](https://github.com/polsoft)  
> **Homepage:** [github.com/polsoft/TerminalX](https://github.com/polsoft/TerminalX)  
> **License:** MIT

---

## Table of Contents

- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Installation Modes](#installation-modes)
- [Environment Variables](#environment-variables)
- [Built-in Commands](#built-in-commands)
- [Plugin System](#plugin-system)
- [Package Manager](#package-manager)
- [Configuration](#configuration)
- [Themes and Profiles](#themes-and-profiles)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Changelog](#changelog)
- [License](#license)

---

## Requirements

| Requirement | Details |
|---|---|
| Python | 3.10 or later |
| OS | Windows, Linux, macOS |
| Dependencies | None (stdlib only) |
| Optional | `windows-curses` for the nano-lite editor on Windows |

To install the optional curses support on Windows:

```
pip install windows-curses
```

---

## Quick Start

```bash
# Run directly
python TerminalX.py

# Run in safe/recovery mode
python TerminalX.py --safe

# Run in portable mode (all data stored next to the script)
python TerminalX.py --portable

# Specify a custom data directory
python TerminalX.py --data /path/to/data
```

Once started, type `help` to see all available commands, or `about` for shell information.

---

## Installation Modes

TerminalX supports multiple deployment scenarios:

### Standard Mode
All data (history, aliases, plugins, packages, config) is stored in your home directory (`~/.terminalx_*`).

### Portable Mode
Activated by one of the following:
- Passing `--portable` flag on startup
- Setting the `TERMINALX_DATA` environment variable
- Passing `--data <path>` on startup
- Creating a `.terminalx_data/` folder next to the script

In portable mode all data is stored inside `.terminalx_data/` next to the script. This enables running TerminalX from a USB drive, network share, or container with no host-side configuration.

### Frozen / Compiled Mode
TerminalX detects when it runs as a PyInstaller bundle or `.pyz` archive and adjusts paths automatically.

---

## Environment Variables

| Variable | Description |
|---|---|
| `TERMINALX_DATA` | Override the data directory path |
| `TERMINALX_RC` | Path to a custom RC file (startup script) |
| `TERMINALX_CONFIG` | Path to a custom config file (JSON/YAML/INI) |
| `TERMINALX_PROFILE` | Profile to activate on startup |
| `TERMINALX_THEME` | Theme to activate on startup |
| `TERMINALX_OFFLINE` | Force offline mode (`1`) |
| `TERMINALX_OFFLINE_FORCE` | Alias for `TERMINALX_OFFLINE` |
| `TERMINALX_NO_COLOR` | Disable ANSI colors (`1`) |
| `NO_COLOR` | Disable ANSI colors (respects [no-color.org](https://no-color.org)) |
| `TERMINALX_VERBOSE` | Enable verbose output (`1`) |
| `TERMINALX_DEBUG` | Enable debug mode (`1`) |
| `TERMINALX_LOG` | Set to `0` to disable logging |

---

## Built-in Commands

TerminalX ships with over 100 built-in commands organized into functional categories.

### File System

| Command | Aliases | Description |
|---|---|---|
| `ls` | | List directory contents with colors and icons |
| `cd` | | Change working directory |
| `pwd` | | Print current working directory |
| `cat` | | Display file contents with syntax highlighting |
| `touch` | | Create a file or update its modification time |
| `mkdir` | `md` | Create directory (including parent directories with `-p`) |
| `rm` | `del` | Delete a file |
| `rmdir` | `rd` | Recursively remove a directory |
| `cp` | `copy` | Copy file or directory (`-r`, `-v`, `-f`, `-n`) |
| `mv` | `move` | Move or rename a file/directory |
| `rename` | | Rename a file |
| `find` | | Search for files by pattern |
| `grep` | | Search for text patterns in files |
| `diff` | | Compare two files line by line |
| `stat` | | Display file metadata |
| `du` | | Show disk usage of a path |
| `tree` | | Display directory tree |
| `tail` | | Show last N lines of a file |
| `head` | | Show first N lines of a file |
| `chmod` | | Change file permissions |
| `chown` | | Change file owner |
| `attrib` | | Display or change file attributes |
| `fman` | | File manager: copy, move, rename, preview, info, tree, find, size |

### Text & Data Processing

| Command | Description |
|---|---|
| `echo` | Print text to output |
| `json` | Parse, format, and colorize JSON |
| `yaml` | Parse and format YAML |
| `jq` | Query JSON with a jq-like syntax |
| `base64` / `b64` | Encode and decode Base64 |
| `hexdump` | Show file contents as hex |
| `hash` | Compute file/string hashes (MD5, SHA-1, SHA-256, etc.) |
| `encode` | Encode/decode text (Base64, URL, HTML, ROT13, hex) |
| `clip` | Copy text to the clipboard |
| `diff` | Compare files |
| `diffview` | Interactive side-by-side diff viewer |
| `jsonview` | Interactive JSON tree viewer |

### Shell & Environment

| Command | Aliases | Description |
|---|---|---|
| `alias` | | Create a command alias |
| `unalias` | | Remove an alias |
| `export` | | Set an environment variable |
| `unset` | | Remove a shell variable |
| `set` | | List or toggle shell options |
| `env` | | Display environment variables |
| `printenv` | | Print a specific environment variable |
| `source` | | Execute a shell script in the current session |
| `which` | | Show the path of a command |
| `history` | | View and search command history |
| `clear` | | Clear the terminal screen |
| `for-loop` | | Simple loop construct |
| `date` | | Show or format the current date/time |
| `echo` | | Print text |
| `call` | | Execute an external script |

### System Information

| Command | Description |
|---|---|
| `whoami` | Show current user |
| `hostname` | Show system hostname |
| `uname` | Display OS and kernel information |
| `uptime` / `uptime2` | Show system uptime |
| `sysinfo` / `systeminfo` | Display system information |
| `id` | Show current user and group IDs |
| `ps` / `ps2` | List running processes |
| `free` | Show memory usage |
| `df` | Show disk free space |
| `cpugraph` | Show CPU usage graph |
| `sysmon` | Real-time system monitor |
| `procmon` | Process monitor |
| `envdetect` | Detect and display current environment details |
| `envs` | List shell environment variables |

### Networking

| Command | Description |
|---|---|
| `ping` | Ping a host |
| `traceroute` | Trace network route to a host |
| `netstat` | Show active network connections |
| `wget` | Download a file from a URL |
| `curl` | Transfer data from a URL |
| `http` | Simple HTTP request tool |
| `ipconfig` | Show network interface configuration |
| `netmon` | Network traffic monitor |
| `portscan` | Scan TCP ports on a host |
| `dns` | DNS lookup |
| `ssh` | SSH client wrapper |
| `serve` | Start a simple HTTP file server |
| `wss` | WebSocket server tool |

### Developer Tools

| Command | Description |
|---|---|
| `pyrepl` | Embedded Python REPL |
| `pysh` | Python expression evaluator in the shell |
| `timeit` | Time command or Python expression execution |
| `debug` | Toggle or inspect debug mode |
| `verbose` | Toggle verbose output |
| `diag` | Run diagnostics |
| `selfcheck` | Verify shell integrity |
| `build` | Build/package the shell |
| `finfo` | File information and analysis |
| `integrate` | Shell integration utilities |

### Plugins & Packages

| Command | Description |
|---|---|
| `plugin` | Manage plugins: install, remove, list, enable, disable, trust |
| `pkg` | Package manager: install, remove, list, update (`.minipkg` format) |
| `newcmd` | Create a new built-in command interactively |
| `pip` | Wrapper for pip with shell integration |

### Sessions & Multiplexing

| Command | Description |
|---|---|
| `session` | Save, restore, and manage shell sessions |
| `split` | Split the terminal into panes |
| `tmux` | tmux-like pane management |
| `sched` | Schedule commands to run at intervals |
| `watch` | Watch and repeat a command on a timer |
| `macro` | Record, replay, and manage command macros |

### UI & Display

| Command | Aliases | Description |
|---|---|---|
| `theme` | | Switch color themes |
| `profile` | | Switch shell profiles |
| `status` | | Show/hide the status bar |
| `boxstyle` | | Change the box-drawing style |
| `tui` | | Text-based UI widgets |
| `nav` | | Interactive directory navigator |
| `gui` | | Launch a Tkinter GUI window |
| `shortcuts` | | Show keyboard shortcuts |
| `mode` | | Switch online/offline mode |
| `clock` | | Display a live clock |

### Utilities

| Command | Description |
|---|---|
| `calc` | Calculator with expression evaluation |
| `timer` | Countdown timer |
| `note` | Quick note manager |
| `todo` | To-do list manager |
| `weather` | Show weather forecast for a location |
| `wset` | Configure default weather location |
| `qr` | Generate QR codes |
| `uuid` | Generate UUIDs |
| `passgen` | Password generator |
| `about` | Show shell information |
| `version` | Show version details |
| `changelog` | Show version history |
| `logs` | View and manage shell logs |
| `logview` | Log viewer with filtering |
| `logtail` | Tail the shell log file |
| `logscan` | Scan logs for patterns |
| `logrotate` | Rotate log files |
| `crashlog` | View and manage crash reports |
| `wizard` | First-time setup wizard |
| `recovery` | Enter or exit recovery/safe mode |
| `help` | Show help for commands |

### Windows-Specific

| Command | Description |
|---|---|
| `tasklist` | List Windows processes |
| `taskkill` | Kill a Windows process |
| `sc` | Windows Service Control |
| `shutdown` | Shut down or restart Windows |
| `powercfg` | Power configuration |
| `compact` | NTFS compression |
| `net` | Windows network commands |
| `netsh` | Network shell |
| `arp` | ARP table |
| `pathping` | PathPing tool |
| `sfc` | System File Checker |
| `dism` | DISM tool |
| `chkdsk` | Check disk |
| `bcdedit` | Boot configuration editor |
| `gpupdate` | Group Policy update |
| `reg` | Registry editor |
| `diskpart` | Disk partitioning |
| `format` | Format a volume |
| `cipher` | EFS encryption utility |
| `schtasks` | Task Scheduler |
| `fsutil` | File System Utility |
| `setx` | Set persistent environment variables |
| `start` | Start a program or command |
| `eventvwr` | Event Viewer |
| `perfmon` | Performance Monitor |
| `resmon` | Resource Monitor |
| `dxdiag` | DirectX Diagnostic |
| `wmic` | Windows Management Instrumentation |

---

## Plugin System

TerminalX supports loading external Python plugins from the `.terminalx_plugins/` directory.

```bash
# List loaded plugins
plugin list

# Install a plugin from a file
plugin install /path/to/myplugin.py

# Install a plugin from a URL (online mode)
plugin install --url https://example.com/myplugin.py

# Enable or disable a plugin
plugin enable myplugin
plugin disable myplugin

# Trust a plugin (required before execution)
plugin trust myplugin

# Remove a plugin
plugin remove myplugin
```

Plugins are sandboxed with a trust system — each plugin must be explicitly trusted before it can run. Trust data is stored in `.terminalx_plugin_trust.json`.

### Writing a Plugin

A plugin is a standard Python file that registers commands via the `@command` decorator:

```python
# TERMINALX_PLUGIN
# "version": "1.0"
# "description": "My example plugin"
# "author": "Your Name"

@command("hello", "Say hello")
def cmd_hello(args):
    print("Hello from plugin!")
```

---

## Package Manager

TerminalX includes a built-in package manager for `.minipkg` packages.

```bash
# List available packages
pkg list

# Install a package
pkg install mypackage

# Install from URL (online mode)
pkg install --url https://example.com/mypackage.minipkg

# Remove a package
pkg remove mypackage

# Update all packages
pkg update
```

Packages are stored in `.terminalx_packages/`.

---

## Configuration

The configuration file is located at `~/.terminalx.json` (or `.terminalx_data/.terminalx.json` in portable mode). It supports **JSON**, **YAML**, and **INI** formats.

```bash
# View current configuration
config show

# Set a configuration value
config set theme dark
config set log_commands true
config set log_max_mb 10

# Reset to defaults
config reset
```

### Key Configuration Options

| Key | Default | Description |
|---|---|---|
| `theme` | `dark` | Active color theme |
| `profile` | `default` | Active profile |
| `log_commands` | `true` | Log executed commands |
| `log_max_mb` | `5` | Maximum log file size (MB) |
| `status_bar` | `true` | Show status bar |
| `box_style` | `rounded` | Box-drawing style |

### RC File (Startup Script)

Commands in `~/.terminalxrc` (or `.terminalx_data/.terminalxrc`) are executed automatically at startup — similar to `.bashrc`.

---

## Themes and Profiles

### Themes

```bash
# List available themes
theme list

# Switch theme
theme dark
theme light
theme monokai
```

### Profiles

Profiles let you save and switch between complete shell configurations.

```bash
# List profiles
profile list

# Create a profile
profile save myprofile

# Load a profile
profile load myprofile

# Delete a profile
profile delete myprofile
```

---

## Advanced Features

### Bash-like Syntax

TerminalX supports standard shell syntax:

```bash
# Pipelines
ls | grep .py

# Redirection
cat file.txt > output.txt
cat file.txt >> log.txt

# Logical operators
mkdir newdir && cd newdir
cd nonexistent || echo "Directory not found"

# Command chaining
clear; ls; date

# Subshell substitution
echo "Today is $(date)"

# Variables
export NAME=World
echo "Hello $NAME"
echo "${NAME:-default}"

# Loops
for-loop i 1 5; echo "Item $i"; done
```

### Macros

```bash
# Start recording
macro record mymacro

# ... run commands ...

# Stop recording
macro stop

# Replay
macro play mymacro

# List macros
macro list
```

### Scheduler

```bash
# Run a command every 60 seconds
sched add "date" 60

# List scheduled jobs
sched list

# Remove a job
sched remove 1
```

### Sessions

```bash
# Save the current session
session save mysession

# Restore a session
session load mysession

# List sessions
session list
```

### Split Panes

```bash
# Split horizontally
split h

# Split vertically
split v

# Switch between panes
split next
```

### Python REPL

```bash
# Launch the embedded Python REPL
pyrepl

# Evaluate a Python expression inline
pysh 2 + 2
pysh import os; os.getcwd()
```

### Recovery Mode

If the shell encounters a fatal error it automatically enters recovery mode. You can also force it manually:

```bash
python TerminalX.py --safe
```

Inside recovery mode:
```bash
recovery diagnose    # Run diagnostics
recovery exit        # Exit recovery and resume normal operation
```

---

## Troubleshooting

### Shell fails to start

- Verify Python 3.10 or later: `python --version`
- If colors show garbage characters, set `NO_COLOR=1` or `TERMINALX_NO_COLOR=1`
- Try safe mode: `python TerminalX.py --safe`

### Crash reports

```bash
# View the latest crash report
crashlog

# View all reports
crashlog list

# Clear crash reports
crashlog clear
```

Crash reports are saved to `.terminalx_crashlog.txt`.

### Logs

```bash
# Tail the live log
logtail

# View log with filtering
logview

# Disable logging
export TERMINALX_LOG=0
```

### nano-lite editor not working on Windows

Install the optional curses library:
```
pip install windows-curses
```

---

## Changelog

See the full history with:
```bash
changelog
```

Selected milestones:

| Version | Highlights |
|---|---|
| 35.2 | File manager (`fman`), weather config (`wset`) |
| 34.0 | Current stable release |
| 16.0 | Online/offline mode, crash log system |
| 15.0 | Full bash-like parser: pipes, redirects, subshell, logical operators |
| 9.0 | nano-lite editor, mini-pkg package manager |

---

## License

TerminalX is released under the **MIT License**.  
© 2024–2025 Sebastian Januchowski (polsoft.ITS™)

See [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT) for the full license text.
