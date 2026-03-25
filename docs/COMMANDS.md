# TerminalX — Command Reference (EN)

> Version 35.2 · 130+ built-in commands

---

## File System

| Command | Aliases | Description |
|---|---|---|
| `ls` | | List directory contents with colors and icons |
| `cd` | | Change current directory |
| `pwd` | | Print current working directory |
| `cat` | | Display file contents with syntax highlighting |
| `touch` | | Create a file or update its modification time |
| `mkdir` | `md` | Create directory, including parent dirs (`-p`) |
| `rm` | `del` | Delete a file |
| `rmdir` | `rd` | Recursively remove a directory |
| `cp` | `copy` | Copy file or directory (`-r`, `-v`, `-f`, `-n`) |
| `mv` | `move` | Move or rename a file or directory |
| `rename` | `ren` | Rename a file or directory |
| `find` | | Search directory tree by pattern |
| `grep` | | Search file contents by regex pattern |
| `diff` | | Compare two files (unified diff) |
| `stat` | | Show detailed file or directory metadata |
| `du` | `diskusage` | Show disk usage of a path |
| `tree` | | Display directory tree |
| `tail` | | Show end of a file (supports live `-f` follow) |
| `head` | | Show beginning of a file |
| `chmod` | | Change file permissions (Linux/macOS) |
| `chown` | | Change file owner (Linux/macOS) |
| `attrib` | | Show or change file attributes (Windows / Linux stat) |
| `fman` | | File manager: copy, move, rename, preview, info, tree, find, size |

## Text & Data Processing

| Command | Aliases | Description |
|---|---|---|
| `echo` | | Print text to output |
| `json` | | Parse, format and validate JSON |
| `yaml` | | Parse and format YAML (stdlib, no pyyaml needed) |
| `jq` | | Query JSON with a jq-like syntax (stdlib, no binary needed) |
| `base64` | | Encode or decode Base64 |
| `b64` | | Alias for base64 encode/decode |
| `hexdump` | | Display binary file contents as hex + ASCII |
| `diff` | | Compare two files with colored output |
| `diffview` | | Side-by-side file comparison with colors |
| `jsonview` | | Interactive JSON tree browser and filter |
| `hash` | | Compute MD5, SHA-1, SHA-256, SHA-512 checksums |
| `encode` | | Encode/decode text: Unicode, ANSI, UTF-8, cp1250 |
| `clip` | | Copy stdin or file to the system clipboard |

## Shell & Environment

| Command | Aliases | Description |
|---|---|---|
| `alias` | | Create a command alias |
| `unalias` | | Remove an alias |
| `export` | | Set and export an environment variable to child processes |
| `unset` | | Remove a shell or environment variable |
| `set` | | List or toggle shell options and variables |
| `env` | | Show environment or run a command with a modified environment |
| `printenv` | | Print the value of an environment variable |
| `envs` | | List environment variables with filtering and sorting |
| `source` | | Load and execute a TerminalX script (`.msh` / `.rc`) |
| `call` | | Execute a batch file or shell script |
| `which` | `where` | Find the path of a program in PATH |
| `history` | | View and search command history |
| `clear` | `cls` | Clear the terminal screen |
| `for-loop` | | FOR loop construct (equivalent to CMD's FOR) |
| `date` | `time` | Display or set the system date and time |
| `deactivate` | | Deactivate a Python virtual environment (venv) |
| `setx` | | Set a persistent environment variable (Windows setx / export Linux) |

## System Information

| Command | Aliases | Description |
|---|---|---|
| `whoami` | | Display the current user |
| `hostname` | | Show or change the system hostname |
| `uname` | | Display OS and kernel information |
| `uptime` | | Show system uptime and average load |
| `uptime2` | | System uptime + load average + local time |
| `sysinfo` | | Full diagnostics: OS, CPU, RAM, disk, network, Python |
| `systeminfo` | | Detailed OS information (Windows systeminfo / uname Linux) |
| `id` | | Show current user and group IDs (Linux/macOS) |
| `ps` | | List system processes |
| `ps2` | | Process list with filtering by name / PID / user |
| `free` | | Show RAM usage (cross-platform) |
| `df` | | Show disk space (cross-platform) |
| `du` | `diskusage` | Show directory and file sizes |
| `cpugraph` | | Live CPU and RAM graph in the terminal (refreshes every 1s) |
| `sysmon` | | Real-time system resource monitor (CPU, RAM, disk, processes) |
| `procmon` | | Process monitor — mini Task Manager TUI |
| `envdetect` | | Auto-detect the current environment and suggest a profile |

## Networking

| Command | Aliases | Description |
|---|---|---|
| `ping` | | Test connectivity (system ping or TCP fallback) |
| `traceroute` | `tracert`, `trace` | Trace packet route to a host |
| `netstat` | | Show network statistics and active connections |
| `wget` | | Download a file from a URL (stdlib urllib) |
| `curl` | | Transfer data via HTTP/HTTPS (stdlib urllib) |
| `http` | | HTTP client (curl-like): GET / POST / HEAD / PUT / DELETE |
| `ipconfig` | | Network interface configuration (Windows / ip addr Linux) |
| `netmon` | | Monitor network connections and interfaces |
| `portscan` | | Multi-threaded TCP port scanner |
| `dns` | | DNS lookup: A, AAAA, PTR, MX, NS, ALL |
| `arp` | | ARP table — MAC/IP addresses on the local network |
| `pathping` | | Combined ping + traceroute (Windows pathping / mtr Linux) |
| `ssh` | | Connect to a host via SSH or manage connection profiles |
| `serve` | | Start a local REST API / HTTP file server |
| `wss` | | Start a local WebSocket server (RFC 6455) |

## Developer Tools

| Command | Aliases | Description |
|---|---|---|
| `pyrepl` | | Embedded interactive Python REPL |
| `pysh` | | Manage `.pysh` modules (dynamic shell extensions) |
| `timeit` | | Measure execution time of a shell command |
| `debug` | | Enable/disable debug mode (full execution trace) |
| `verbose` | | Enable/disable verbose mode (echo commands before execution) |
| `diag` | | System diagnostics: CPU, RAM, disk, network, processes |
| `finfo` | | Full file metadata: type, MIME, encoding, hash, statistics |
| `selfcheck` | | Verify shell integrity and internal consistency |
| `integrate` | | Shell integration utilities (PATH, rc files, desktop) |
| `build` | | Build a standalone EXE with PyInstaller |
| `builder` | | Builder mode — generate and manage custom shell modules |
| `project` | | Create and manage terminal projects (polsoft.ITS™) |
| `ai` | | AI integration — questions, suggestions, command explanations |

## Plugins & Packages

| Command | Aliases | Description |
|---|---|---|
| `plugin` | | Manage plugins: install, remove, list, enable, disable, trust |
| `pkg` | | Mini package manager: install, remove, list, update (`.minipkg`) |
| `pip` | | Wrapper for system pip / shell mini-pip |
| `newcmd` | | Wizard: create a new command without editing the shell source |

## Sessions & Multiplexing

| Command | Aliases | Description |
|---|---|---|
| `session` | | Save, restore and manage shell sessions (tmux-style) |
| `split` | | Pseudo split-screen — divide the terminal into panes |
| `tmux` | | tmux-style shortcuts for session and split management |
| `sched` | | Built-in task scheduler (cross-platform) |
| `watch` | | Trigger automatic tasks on system events |
| `macro` | | Record, replay and manage command macros |

## UI & Display

| Command | Aliases | Description |
|---|---|---|
| `theme` | | Switch, create and manage color themes |
| `profile` | | Manage TerminalX configuration profiles |
| `status` | | Toggle or show the status bar |
| `boxstyle` | | Change UI box-drawing style (single/round/double/heavy/ascii) |
| `tui` | | Interactive TUI menu (text-based interface) |
| `nav` | | Interactive TUI file browser |
| `gui` | | GUI backend via IPC socket (NDJSON) |
| `shortcuts` | | Show all keyboard shortcuts |
| `mode` | | Switch online/offline mode |
| `clock` | | Live digital clock in the terminal |

## Utilities

| Command | Aliases | Description |
|---|---|---|
| `calc` | | Calculator for mathematical expressions |
| `timer` | | Stopwatch, countdown and alarm |
| `note` | | Quick notes — add, browse, search, delete |
| `todo` | | TODO list with priorities and status |
| `weather` | | ASCII weather forecast via wttr.in |
| `wset` | `weather-set` | Set the default location for the weather command |
| `qr` | | Generate a QR code in the terminal (Unicode blocks or ASCII art) |
| `uuid` | | Generate UUID v1/v4/v5 and short IDs |
| `passgen` | | Strong password, passphrase and PIN generator |
| `archive` | | Create and extract archives |
| `about` | | Show author, version and license info |
| `version` | | Display TerminalX version |
| `changelog` | `changes`, `history-log` | Show TerminalX version history |
| `help` | `?` | Show help for commands |

## Logging & Diagnostics

| Command | Aliases | Description |
|---|---|---|
| `logs` | | Advanced shell log viewer and exporter |
| `logview` | | View the local shell log with filtering |
| `logtail` | | Live log tail (real-time view) |
| `logscan` | | Scan log file for errors or patterns |
| `logrotate` | `rotatelog` | Rotate the shell log file |
| `crashlog` | | View and manage crash reports |
| `recovery` | | Enter or exit safe/recovery mode |
| `wizard` | | Interactive configuration setup wizard |
| `portable` | | Manage TerminalX portable mode |

## Access & Security

| Command | Aliases | Description |
|---|---|---|
| `sudo` | | Run a command as root or switch to root mode |
| `elevate` | | Elevate privileges to administrator (UAC/sudo) |
| `cipher` | | EFS encryption (Windows) / secure free-space wipe |

## Windows-Specific

| Command | Description |
|---|---|
| `tasklist` | List system processes (Windows tasklist / ps) |
| `taskkill` | Kill a process by PID or name |
| `pkill2` | Kill a process by name or PID (with confirmation prompt) |
| `sc` | Manage system services (Windows sc / systemctl) |
| `shutdown` | Shut down, restart or log off the system |
| `powercfg` | Power configuration and reports (Windows) |
| `compact` | NTFS compression (Windows) or compression info (Linux) |
| `net` | Windows NET commands (users, groups, services, shares) |
| `netsh` | Windows network configuration (netsh) or ip/nmcli (Linux) |
| `sfc` | System File Checker (Windows sfc / debsums Linux) |
| `dism` | DISM — Windows image servicing |
| `chkdsk` | Check disk for errors (Windows chkdsk / fsck Linux) |
| `bcdedit` | Windows BCD bootloader configuration |
| `gpupdate` | Group Policy update (Windows) |
| `reg` | Windows Registry editor |
| `diskpart` | Disk and partition management |
| `format` | Format a drive or partition |
| `schtasks` | Windows Task Scheduler (schtasks / cron Linux) |
| `fsutil` | File System Utility (Windows fsutil / stat Linux) |
| `start` | Start a program or file in a new window or process |
| `eventvwr` | System Event Viewer (Windows Event Viewer / journalctl Linux) |
| `perfmon` | Performance Monitor (Windows perfmon / vmstat-top Linux) |
| `resmon` | Resource Monitor (Windows resmon / htop Linux) |
| `dxdiag` | DirectX Diagnostic (Windows) / OpenGL/GPU info (Linux) |
| `wmic` | Windows Management Instrumentation (WMI) interface |
