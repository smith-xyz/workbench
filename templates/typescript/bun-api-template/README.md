# Bun API Template

Lightweight HTTP API scaffold using Bun + Hono — fast startup, single-binary deploys.

## Quick Start

```bash
bun install
bun run dev         # watch mode on :3000
```

## Build

```bash
bun run build       # → bin/yourservice (standalone binary)
```

## Architecture

```
src/
  main.ts           → Hono app, middleware, server export
  routes/
    health.ts       → Liveness + readiness probes
    items.ts        → Example CRUD (in-memory store)
```

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness |
| GET | `/health/ready` | Readiness |
| GET | `/api/v1/items` | List items |
| GET | `/api/v1/items/:id` | Get item |
| POST | `/api/v1/items` | Create item |
| DELETE | `/api/v1/items/:id` | Delete item |

## Testing

```bash
bun test
```

## Docker

```bash
docker build -t yourservice .
docker run -p 3000:3000 yourservice
```

## Adding Routes

1. Create `src/routes/myroute.ts` with a `new Hono()` instance
2. Mount in `src/main.ts`: `app.route('/api/v1/myroute', myRoutes)`
