# Bun CLI Template

CLI scaffold using Bun — `parseArgs` from util, config-file-first with CLI overrides, single-binary builds.

## Quick Start

```bash
bun install
bun run dev --verbose
```

## Build

```bash
bun run build       # → bin/yourcli (standalone binary)
./bin/yourcli --help
```

## Architecture

```
src/
  main.ts           → parseArgs, config load, dispatch
  config.ts         → JSON config loader + CLI override merge
  commands/
    run.ts          → Main logic with signal handling
    version.ts      → Print version from package.json
```

## Config

Config file (`~/.yourcli.json`) with CLI overrides on top. Precedence: CLI flags > config file > defaults.

```json
{ "verbose": true, "logLevel": "debug" }
```

## Testing

```bash
bun test
```
