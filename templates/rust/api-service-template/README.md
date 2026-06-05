# Web Service Template (Rust)

A modern, production-ready web service template built with Rust and the Axum framework.

## Features

- Axum 0.8 async web framework
- RESTful JSON API with standard endpoints
- CORS support
- Structured logging via tracing
- In-memory storage (easily replaceable)

## API Endpoints

| Method | Endpoint    | Description           |
|--------|-------------|-----------------------|
| GET    | `/`         | Health check          |
| GET    | `/health`   | Health check          |
| GET    | `/items`    | Get all items         |
| POST   | `/items`    | Create a new item     |
| GET    | `/items/{id}`| Get item by ID       |

## Quick Start

### Prerequisites

- Rust 1.85+ (edition 2024)
- Cargo package manager

### Installation

1. Clone or copy this template:
```bash
git clone <repository-url>
cd api-service-template
```

2. Build and run:
```bash
make run
```

The service will start on `http://localhost:3000`

### Development

```bash
# Run in development mode with auto-reload
make dev

# Run tests
make test

# Format code
make fmt

# Run linter
make lint

# Build for production
make build
```

## Usage Examples

### Health Check
```bash
curl http://localhost:3000/health
```

### Create an Item
```bash
curl -X POST http://localhost:3000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example Item",
    "description": "This is an example item"
  }'
```

### Get All Items
```bash
curl http://localhost:3000/items
```

### Get Item by ID
```bash
curl http://localhost:3000/items/1
```

## API Response Format

All API responses follow this structure:

```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation completed successfully"
}
```

## Configuration

The service runs on port 3000 by default. You can modify the port in `src/main.rs`:

```rust
let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
```

## Production Deployment

### Docker

A Dockerfile is included for containerized deployment:

```bash
make docker-build
make docker-run
```

### Manual Deployment

1. Build optimized binary:
```bash
make build-release
```

2. Copy the binary from `target/release/api-service-template` to your server

3. Run with environment variables:
```bash
RUST_LOG=info ./api-service-template
```

## Project Structure

```
.
├── Cargo.toml          # Project dependencies and metadata
├── src/
│   └── main.rs         # Main application code
├── Makefile            # Build and development commands
└── README.md           # This file
```

## Dependencies

- axum — async web framework
- tokio — async runtime
- serde — serialization
- tracing — structured logging
- tower-http — HTTP middleware
