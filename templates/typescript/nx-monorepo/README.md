# Nx Monorepo Starter

> **Starter kit** — Nx + pnpm + Vite (React frontend) + tsc (Node backend) + TypeORM + Vitest.

## Architecture

```
apps/
  web/         → React SPA (Vite, Tailwind, port 3000)
  api/         → Express 5 backend (tsx watch, port 4000)
libs/
  shared/      → Types, Result, branded IDs (no runtime deps)
  db/          → TypeORM entities + DataSource factory
```

Frontend proxies `/api` to the backend in dev. Libs share code via TypeScript path aliases + pnpm workspace protocol.

## Quick Start

```bash
pnpm install
pnpm dev          # starts web + api in parallel
```

## Commands

| Command | Description |
|---------|-------------|
| `pnpm dev` | Serve all apps |
| `pnpm build` | Build all projects |
| `pnpm test` | Run Vitest across workspace |
| `pnpm typecheck` | Type-check all projects |
| `pnpm lint` | ESLint flat config |

## Adding a Library

```bash
mkdir -p libs/mylib/src
# Add package.json, tsconfig.json, tsconfig.lib.json
# Add path alias to tsconfig.base.json
# Add reference to root tsconfig.json
```

## Adding an App

```bash
mkdir -p apps/myapp/src
# Add package.json, tsconfig.json, project.json
# Add reference to root tsconfig.json
```

## Docker

```bash
docker compose up        # postgres + api
docker compose up --build
```

## Env

Copy `.env.example` to `.env` and adjust values.
