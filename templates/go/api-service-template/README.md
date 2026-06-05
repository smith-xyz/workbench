# Go API Service Template

Production-shaped Go HTTP API scaffold using Chi router and GORM.

## Architecture

```
cmd/
  api/          → HTTP server entry point
  migrate/      → Database migration CLI
internal/
  server/       → HTTP lifecycle (listen, graceful shutdown)
  api/          → Router composition, deps wiring, config
  api/v1/       → Versioned route mounting
  api/middleware/ → Request logging, CORS, recovery
  apiutil/      → JSON helpers, pagination, error responses
  apierr/       → Typed API errors (not_found, validation, etc.)
  env/          → Environment variable helpers
  health/       → Readiness check interface
  store/db/     → GORM wrapper, connection pool, migrations engine
  items/        → Example domain (handler → service → repository)
```

## Patterns

- Thin `main.go` delegates to a composition root (`api.ServerConfig`)
- Explicit DI via `APIDeps` struct — no framework, just constructor wiring
- Domain slices: each feature gets its own package with `handler.go`, `service.go`, `repository.go`, `model.go`
- Handlers expose `Mount(chi.Router)` and register their own sub-routes
- Code-first migrations with version registry, advisory locks, separate CLI binary
- Typed errors flow from domain → handler → consistent JSON

## Quick Start

```bash
# Set required env
export DATABASE_URL="postgres://user:pass@localhost:5432/yourdb?sslmode=disable"

# Run migrations
make migrate

# Start server
make run

# Create a new migration
make migrate-create NAME=add_users
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | (required) | PostgreSQL connection string |
| `LISTEN_ADDR` | `:8080` | Server listen address |
| `DB_MAX_OPEN_CONNS` | `10` | Max open DB connections |
| `DB_MAX_IDLE_CONNS` | `5` | Max idle DB connections |
| `DB_LOG_LEVEL` | `warn` | GORM log level (silent/error/warn/info) |
| `CORS_ALLOW_ORIGIN` | (disabled) | CORS origin header |
| `DEBUG` | `false` | Expose error details in responses |

## Adding a New Domain

1. Create `internal/yourdomain/` with handler, service, repository, model files
2. Add `MountYourDomain` to `internal/api/v1/routes.go`
3. Wire service/handler in `internal/api/config.go` → `buildDeps`
4. Mount conditionally in `internal/api/routes.go` → `Routes`

