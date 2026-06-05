# Go Daemon Template

Long-running process with env-based config, structured logging, health file, and graceful SIGTERM/SIGINT shutdown. Platform-agnostic with deploy configs for Linux, macOS, and Windows.

## Architecture

```
main.go              → Entry point, signal handling, tick loop
internal/
  config/            → Env-based configuration
  health/            → Atomic JSON health file writer
deploy/
  linux/             → systemd unit
  macos/             → launchd plist
  windows/           → NSSM install/uninstall scripts
```

## Quick Start

```bash
go run .
```

With config:

```bash
DAEMON_TICK_INTERVAL_SECS=5 DAEMON_LOG_JSON=true go run .
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DAEMON_TICK_INTERVAL_SECS` | `30` | Seconds between ticks (min 1) |
| `DAEMON_HEALTH_FILE` | `/tmp/yourdaemon-health.json` | Health probe path |
| `DAEMON_LOG_JSON` | `false` | JSON log output |

## Installation

### Linux (systemd)

```bash
sudo make install-linux
sudo systemctl daemon-reload
sudo systemctl enable --now yourdaemon.service
```

Env file: `/etc/default/yourdaemon` (loaded by the unit automatically).

### macOS (launchd)

```bash
make install-macos
```

### Windows (NSSM)

```powershell
go build -o bin\yourdaemon.exe .
.\deploy\windows\install.ps1
nssm start yourdaemon
```

## Docker

```bash
make docker-build
docker run --rm yourdaemon
```
