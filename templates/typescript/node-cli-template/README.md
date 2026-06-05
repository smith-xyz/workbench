# Node CLI Template

CLI scaffold using Node.js — `parseArgs` from node:util, config-file-first with CLI overrides, zero runtime deps.

## Quick Start

```bash
npm install
npm run dev -- --verbose
```

## Build

```bash
npm run build
node dist/main.js --help
```

## Architecture

```
src/
  main.ts           → parseArgs, config load, dispatch
  config.ts         → JSON config loader + CLI override merge
  commands/
    run.ts          → Main logic with signal handling
```

## Config

Config file (`~/.yourcli.json`) with CLI overrides on top. Precedence: CLI flags > config file > defaults.

```json
{ "verbose": true, "logLevel": "debug" }
```

## Testing

```bash
npm test
```

## Publishing / Global Install

```bash
npm run build
npm link            # makes `yourcli` available globally
```
