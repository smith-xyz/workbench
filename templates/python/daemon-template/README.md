# Python Daemon Template

Long-running process with TOML config, env overrides, structured logging, health file, and graceful shutdown. Platform-agnostic — deploy configs provided for Linux, macOS, and Windows.

## Architecture

- `src/main.py` — entry point, signal handlers, tick loop
- `src/config.py` — TOML file + `DAEMON_*` env overrides
- `src/logging.py` — structured logging (plain or JSON)
- `src/health.py` — atomic JSON health file for probes

## Quick Start

```bash
cp config.example.toml config.toml
python -m src.main
```

Or with UV:

```bash
uv run python -m src.main
```

## Config

See `config.example.toml`:

| Field | Default | Description |
|-------|---------|-------------|
| `tick_interval_secs` | `30.0` | Seconds between ticks (min 1) |
| `health_file` | `/tmp/daemon-template-health.json` | Health probe path |
| `log_json` | `false` | JSON log output |
| `log_level` | `INFO` | Log level |

## Environment Variables

| Variable | Effect |
|----------|--------|
| `DAEMON_CONFIG` | Path to TOML config (default: `config.toml`) |
| `DAEMON_TICK_INTERVAL_SECS` | Override tick interval |
| `DAEMON_HEALTH_FILE` | Override health file path |
| `DAEMON_LOG_JSON` | `true`/`false` |
| `DAEMON_LOG_LEVEL` | `DEBUG`/`INFO`/`WARNING`/`ERROR` |

## Installation

### Linux (systemd)

```bash
sudo make install-linux
sudo systemctl daemon-reload
sudo systemctl enable --now yourservice.service
```

### macOS (launchd)

```bash
make install-macos
```

### Windows (NSSM)

```powershell
.\deploy\windows\install.ps1
nssm start daemon-template
```

## Docker

```bash
docker build -t daemon-template .
docker run --rm daemon-template
```
