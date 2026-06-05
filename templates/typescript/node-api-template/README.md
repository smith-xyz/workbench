# Node API Template

HTTP API scaffold using Node.js + Fastify + TypeScript.

## Quick Start

```bash
npm install
npm run dev         # watch mode on :3000
```

## Build & Run

```bash
npm run build
npm start
```

## Architecture

```
src/
  main.ts           → Fastify app, plugin registration, graceful shutdown
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
npm test
```

## Docker

```bash
docker build -t yourservice .
docker run -p 3000:3000 yourservice
```

## Adding Routes

1. Create `src/routes/myroute.ts` as a `FastifyPluginAsync`
2. Register in `src/main.ts`: `app.register(myRoutes, { prefix: '/api/v1/myroute' })`
