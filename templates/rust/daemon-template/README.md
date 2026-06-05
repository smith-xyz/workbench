# Rust daemon template

Production-oriented Tokio daemon: TOML configuration with environment overrides, `tracing` JSON or plain logs, SIGTERM/SIGINT shutdown, a tick loop, and a JSON health file for probes.

## Architecture

- `main` parses configuration, wires tracing, then runs the async entrypoint.
- `config` merges `config.toml` (when present) with `DAEMON_*` overrides.
- `run` runs `tokio::time::interval` work and listens for SIGTERM/SIGINT (Unix) or Ctrl+C (elsewhere).
- `health` writes JSON to the configured path each tick for probes and orchestrators.

## Quick start

```bash
cp config.example.toml config.toml
cargo run
```

Tune log noise:

```bash
RUST_LOG=debug cargo run
```

## Config file

Fields (see `config.example.toml`):

| Field | Meaning |
|-------|---------|
| `tick_interval_secs` | Seconds between ticks (minimum 1 at runtime) |
| `health_file` | Path for the JSON health snapshot |
| `log_json` | Emit logs as JSON when true |

Default path is `config.toml`. Set `DAEMON_CONFIG` to use another file. If the file is missing, defaults apply and env vars still override.

## Environment variables

| Variable | Effect |
|----------|--------|
| `DAEMON_CONFIG` | Path to TOML config |
| `DAEMON_TICK_INTERVAL_SECS` | Override tick interval |
| `DAEMON_HEALTH_FILE` | Override health file path |
| `DAEMON_LOG_JSON` | Boolean: `1`/`0`, `true`/`false`, `on`/`off`, etc. |
| `RUST_LOG` | `tracing-subscriber` filter (e.g. `info`, `daemon_template=debug`) |

## Installation

The binary is platform-agnostic. Service definitions live under `deploy/` per OS.

### Linux (systemd)

```bash
make build-release
sudo make install-linux
sudo systemctl daemon-reload
sudo systemctl enable --now yourservice.service
```

Uninstall:

```bash
sudo systemctl disable --now yourservice.service
sudo make uninstall-linux
sudo systemctl daemon-reload
```

Optional env file: `/etc/default/daemon-template` (loaded by the unit automatically).

### macOS (launchd)

```bash
make install-macos
```

This copies the binary and loads `deploy/macos/com.yourorg.yourservice.plist` into `~/Library/LaunchAgents`. Edit the plist to adjust paths/env.

Uninstall:

```bash
make uninstall-macos
```

### Windows (NSSM)

Requires [NSSM](https://nssm.cc) (`choco install nssm`). Run as Administrator:

```powershell
cargo build --release
.\deploy\windows\install.ps1
nssm start daemon-template
```

Uninstall:

```powershell
.\deploy\windows\uninstall.ps1
```

## Docker

```bash
docker build -t daemon-template .
docker run --rm daemon-template
```

The image runs a non-root user, sets `DAEMON_CONFIG=/app/config.toml`, seeds config from `config.example.toml`, and defines a `HEALTHCHECK` on the default health file under `/app/var/health.json`. Mount a volume or your own config when you deploy.
